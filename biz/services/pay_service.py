# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from django.conf import settings
from weixin.pay import WeixinPay
from alipay import AliPay
from biz.models import PayOrder
from biz.constants import PAYMENT_TYPE_ALIPAY, PAYMENT_TYPE_WALLET, PAYMENT_TYPE_WECHAT, PAYMENT_STATUS_PAID

alipay = AliPay(**settings.ALIPAY)
wechat_pay = WeixinPay(**settings.WECHAT_PAY)
logger = logging.getLogger()


class PayService:

    @classmethod
    def generate_out_trade_no(cls):
        return datetime.now().strftime('%y%m%d%H%M%S%f')

    @classmethod
    def create_order(cls, user, obj, payment_type, amount, device, ip):
        order = PayOrder.objects.create(
            user=user,
            content_object=obj,
            payment_type=payment_type,
            amount=obj.price * 100,
            device=device,
            out_trade_no=cls.generate_out_trade_no()
        )
        name = f'{obj.__class__._meta.verbose_name} {obj.id}'
        data = dict(out_trade_no=order.out_trade_no, amount=amount, name=name)
        if payment_type == PAYMENT_TYPE_ALIPAY:
            return cls.get_alipay_payment_info(**data)
        elif payment_type == PAYMENT_TYPE_WECHAT:
            return cls.get_wechat_payment_info(ip=ip, **data)
        else:
            cls.get_wallet_payment_info()

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
    def get_wallet_payment_info(cls, out_trade_no, amount, name):
        pass

    @classmethod
    def on_wechat_callback(cls, data):
        logger.info(
            "[wechat_pay:] calback:{}".format('&'.join('{}={}'.format(key, val) for key, val in sorted(data.items())))
        )
        if wechat_pay.check(data):
            cls.success_callback(data)
            return wechat_pay.reply('OK', True)
        return wechat_pay.reply("签名验证失败", False)

    @classmethod
    def on_alipay_callback(cls, data):
        logger.info(
            "[alipay:] calback:{}".format('&'.join('{}={}'.format(key, val) for key, val in sorted(data.items())))
        )
        signature = data.pop("sign")
        if alipay.verify(data, signature) and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            cls.success_callback(data)
            return 'success'
        return '签名验证失败'

    @classmethod
    def success_callback(cls, data):
        order = PayOrder.objects.get(out_trade_no=data['out_trade_no'])
        order.status = PAYMENT_STATUS_PAID
        order.save()
