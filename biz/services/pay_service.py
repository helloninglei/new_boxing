# -*- coding: utf-8 -*-
import logging
from time import time
from datetime import datetime
from django.utils import timezone
from django.db.transaction import atomic
from django.conf import settings
from weixin.pay import WeixinPay, WeixinPayError
from alipay import AliPay, AliPayException
from biz.models import PayOrder, User, HotVideo, CourseOrder
from biz.redis_client import get_order_no_serial
from biz.constants import PAYMENT_TYPE_ALIPAY, PAYMENT_STATUS_PAID, \
    MONEY_CHANGE_TYPE_INCREASE_RECHARGE, PAYMENT_STATUS_UNPAID, OFFICIAL_ACCOUNT_CHANGE_TYPE_RECHARGE, \
    OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_COURSE, OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_VIDEO, PAYMENT_TYPE_WALLET, \
    MONEY_CHANGE_TYPE_REDUCE_ORDER, \
    MONEY_CHANGE_TYPE_REDUCE_PAY_FOR_VIDEO, COURSE_PAYMENT_STATUS_WAIT_USE
from biz.services import official_account_service
from biz.services.money_balance_service import change_money, ChangeMoneyException


def app_order(self, out_trade_no, amount, name, ip):
    result = self.unified_order(
        trade_type='APP',
        out_trade_no=out_trade_no,
        body=name,
        total_fee=amount,
        spbill_create_ip=ip,
    )

    timestamp = str(int(time()))
    raw = dict(
        appid=self.app_id,
        partnerid=self.mch_id,
        prepayid=result['prepay_id'],
        noncestr=self.nonce_str,
        timestamp=timestamp,
        package='Sign=WXPay',
    )
    raw['sign'] = self.sign(raw)
    return raw


WeixinPay.app_order = app_order

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
        if not isinstance(obj, User):
            return f'{obj.__class__._meta.verbose_name}'
        return '充值'

    @classmethod
    def create_order(cls, user, obj, payment_type, device, ip, amount=None):  # amount 单位分
        order = cls.perform_create_order(user, obj, device, amount, payment_type)
        name = cls.generate_name(obj)
        data = dict(out_trade_no=order.out_trade_no, amount=order.amount, name=name)

        if payment_type == PAYMENT_TYPE_WALLET:
            return cls.do_wallet_payment(user, order)
        pay_info = cls.get_payment_info(payment_type, data, ip)
        result = {'order_id': order.out_trade_no}
        if payment_type == PAYMENT_TYPE_ALIPAY:
            result['pay_info_str'] = pay_info
        else:
            result['pay_info'] = pay_info
        return result

    @classmethod
    def perform_create_order(cls, user, obj, device, amount=None, payment_type=None):  # amount 单位分
        if isinstance(obj, CourseOrder):
            amount = obj.course.price
        return PayOrder.objects.create(
            user=user,
            content_object=obj,
            payment_type=payment_type,
            amount=amount if amount else obj.price,
            device=device,
            out_trade_no=cls.generate_out_trade_no()
        )

    @classmethod
    def get_payment_info(cls, payment_type, data, ip):
        if payment_type == PAYMENT_TYPE_ALIPAY:
            return cls.get_alipay_payment_info(**data)
        else:
            return cls.get_wechat_payment_info(ip=ip, **data)

    @classmethod
    def get_alipay_payment_info(cls, out_trade_no, amount, name):
        return alipay.api_alipay_trade_app_pay(
            out_trade_no=out_trade_no,
            total_amount=amount / 100,  # 支付宝要求单位是元
            subject=name,
            notify_url=settings.ALIPAY['app_notify_url']
        )

    @classmethod
    def get_wechat_payment_info(cls, out_trade_no, amount, name, ip):
        return wechat_pay.app_order(
            out_trade_no=out_trade_no,
            name=name,
            amount=amount,
            ip=ip,
        )

    @classmethod
    @atomic
    def do_wallet_payment(cls, user, order):
        if isinstance(order.content_object, HotVideo):
            change_type = MONEY_CHANGE_TYPE_REDUCE_PAY_FOR_VIDEO
        elif isinstance(order.content_object, CourseOrder):
            change_type = MONEY_CHANGE_TYPE_REDUCE_ORDER
            cls.change_course_order_status(order)
        else:
            change_type = MONEY_CHANGE_TYPE_REDUCE_ORDER
        try:
            change_money(user=user, amount=-order.amount, change_type=change_type, remarks=order.out_trade_no)
            order.status = PAYMENT_STATUS_PAID
            order.pay_time = datetime.now()
            order.save()
            return {
                'status': 'success',
                'order_id': order.out_trade_no,
            }
        except ChangeMoneyException:
            return {
                'status': 'failed',
                'message': '余额不足',
                'order_id': order.out_trade_no,
            }

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
        data = data.dict()
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
        try:
            pay_order = PayOrder.objects.get(out_trade_no=data['out_trade_no'])
        except PayOrder.DoesNotExist:
            logger.info(f"支付订单{data['out_trade_no']}不存在")
            return
        if pay_order.status == PAYMENT_STATUS_UNPAID:
            if isinstance(pay_order.content_object, User):
                change_type = OFFICIAL_ACCOUNT_CHANGE_TYPE_RECHARGE
                change_money(user=pay_order.content_object, amount=pay_order.amount,
                             change_type=MONEY_CHANGE_TYPE_INCREASE_RECHARGE,
                             remarks=pay_order.out_trade_no)
            elif isinstance(pay_order.content_object, CourseOrder):
                change_type = OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_COURSE
                cls.change_course_order_status(pay_order)
            else:
                change_type = OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_VIDEO

            official_account_service.create_official_account_change_log(
                pay_order.amount, pay_order.user, change_type, remarks=pay_order.out_trade_no)

        pay_order.status = PAYMENT_STATUS_PAID
        pay_order.pay_time = datetime.now()
        pay_order.save()

    @classmethod
    def get_payment_status_info(cls, out_trade_no, request_user):
        pay_order = PayOrder.objects.filter(out_trade_no=out_trade_no, user=request_user).first()
        if pay_order:
            content = pay_order.content_object
            if isinstance(content, HotVideo):
                name = f'视频（{content.name}）'
            elif isinstance(content, User):
                name = '充值'
            else:
                name = content.course.get_course_name_display()
            return {
                'status': 'paid' if pay_order.status > PAYMENT_STATUS_UNPAID else 'unpaid',
                'name': name,
                "amount": pay_order.amount,
                'pay_type': pay_order.get_payment_type_display(),
                'pay_time': timezone.localtime(pay_order.pay_time).strftime(
                    datetime_format) if pay_order.pay_time else None,
            }

    @classmethod
    def change_course_order_status(cls, pay_order):
        pay_order.content_object.pay_order = pay_order
        pay_order.content_object.pay_time = datetime.now()
        pay_order.content_object.status = COURSE_PAYMENT_STATUS_WAIT_USE
        pay_order.content_object.order_number = pay_order.out_trade_no
        pay_order.content_object.amount = pay_order.amount
        pay_order.content_object.save()
