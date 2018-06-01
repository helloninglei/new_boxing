# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from django.db.transaction import atomic
from django.conf import settings
from weixin.pay import WeixinPay, WeixinPayError
from alipay import AliPay, AliPayException
from biz.models import PayOrder, User, HotVideo, Course
from biz.redis_client import get_order_no_serial
from biz.constants import PAYMENT_TYPE_ALIPAY, PAYMENT_TYPE_WECHAT, PAYMENT_STATUS_WAIT_USE, \
    MONEY_CHANGE_TYPE_INCREASE_RECHARGE, PAYMENT_STATUS_UNPAID, OFFICIAL_ACCOUNT_CHANGE_TYPE_RECHARGE, \
    OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_COURSE, OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_VIDEO
from biz.services import money_balance_service, official_account_service

alipay = AliPay(**settings.ALIPAY)
wechat_pay = WeixinPay(**settings.WECHAT_PAY)
datetime_format = settings.REST_FRAMEWORK['DATETIME_FORMAT']
logger = logging.getLogger()


class PayService:
    # 订单号规则：xxxx年xx月xx日xxxxx，案例：2018020500001。获取下单日期和当天的订单排序，从1开始，自然数
    @classmethod
    def generate_out_trade_no(cls):
        return f"{datetime.now().strftime('%Y%m%d')}{get_order_no_serial()}"

    @classmethod
    def generate_name(cls, obj):
        return f'{obj.__class__._meta.verbose_name} {obj.id}'

    @classmethod
    def generate_data(cls, out_trade_no, amount, name):
        return dict(out_trade_no=out_trade_no, amount=amount, name=name)

    @classmethod
    def create_order(cls, user, obj, payment_type, device, ip, amount=None):
        order = cls.perform_create_order(user, obj, device, amount, payment_type)
        name = cls.generate_name(obj)
        data = cls.generate_data(
            order.out_trade_no,
            amount if amount else obj.price,
            name
        )
        return {
            'order_id': order.out_trade_no,
            'pay_info': cls.get_payment_info(payment_type, data, ip),
        }

    @classmethod
    def perform_create_order(cls, user, obj, device, amount=None, payment_type=None):
        return PayOrder.objects.create(
            user=user,
            content_object=obj,
            payment_type=payment_type,
            amount=amount * 100 if amount else obj.price * 100,
            device=device,
            out_trade_no=cls.generate_out_trade_no()
        )

    @classmethod
    def get_payment_info(cls, payment_type, data, ip):
        if payment_type == PAYMENT_TYPE_ALIPAY:
            return cls.get_alipay_payment_info(**data)
        elif payment_type == PAYMENT_TYPE_WECHAT:
            return cls.get_wechat_payment_info(ip=ip, **data)
        else:
            cls.do_wallet_payment()

    @classmethod
    def get_alipay_payment_info(cls, out_trade_no, amount, name):
        return alipay.api_alipay_trade_app_pay(
            out_trade_no=out_trade_no,
            total_amount=amount,
            subject=name,
            notify_url=''
        )

    @classmethod
    def get_wechat_payment_info(cls, out_trade_no, amount, name, ip):
        return wechat_pay.unified_order(
            trade_type='APP',
            out_trade_no=out_trade_no,
            body=name,
            total_fee=amount * 100,
            spbill_create_ip=ip,
        )

    @classmethod
    def do_wallet_payment(cls):  # TODO 钱包支付
        pass

    @classmethod
    def on_wechat_callback(cls, data):
        logger.info(
            "[wechat_pay:] calback:{}".format('&'.join('{}={}'.format(key, val) for key, val in sorted(data.items())))
        )
        try:
            if wechat_pay.check(data):
                cls.success_callback(data)
                return wechat_pay.reply('OK', True)
        except (WeixinPayError, KeyError) as e:
            logger.error(e)
            return wechat_pay.reply("签名验证失败", False)

    @classmethod
    def on_alipay_callback(cls, data):
        logger.info(
            "[alipay:] calback:{}".format('&'.join('{}={}'.format(key, val) for key, val in sorted(data.items())))
        )
        try:
            signature = data.pop("sign")
            if alipay.verify(data, signature) and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
                cls.success_callback(data)
                return 'success'
        except (AliPayException, KeyError) as e:
            logger.error(e)
            return '签名验证失败'

    @classmethod
    @atomic
    def success_callback(cls, data):
        pay_order = PayOrder.objects.get(out_trade_no=data['out_trade_no'])
        if pay_order.status == PAYMENT_STATUS_UNPAID:
            if isinstance(pay_order.content_object, User):
                change_type = OFFICIAL_ACCOUNT_CHANGE_TYPE_RECHARGE
                money_balance_service.change_money(user=pay_order.content_object, amount=pay_order.amount,
                                                   change_type=MONEY_CHANGE_TYPE_INCREASE_RECHARGE,
                                                   remarks=pay_order.out_trade_no)
            elif isinstance(pay_order.content_object, Course):
                change_type = OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_COURSE
            else:
                change_type = OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_VIDEO

            official_account_service.create_official_account_change_log(
                pay_order.amount, pay_order.user, change_type, remarks=pay_order.out_trade_no)

        pay_order.status = PAYMENT_STATUS_WAIT_USE
        pay_order.save()

    @classmethod
    def get_payment_status_info(cls, out_trade_no, request_user):
        pay_order = PayOrder.objects.filter(out_trade_no=out_trade_no, user=request_user).first()
        if pay_order:
            content = pay_order.content_object
            return {
                'status': 'paid' if pay_order.status > PAYMENT_STATUS_UNPAID else 'unpaid',
                'name': f'视频（{content.name}）' if isinstance(content, HotVideo) else content.get_course_name_display(),
                'amount': pay_order.amount / 100,
                'pay_time': pay_order.pay_time.strftime(datetime_format) if pay_order.pay_time else None,
            }
