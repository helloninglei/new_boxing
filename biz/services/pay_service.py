# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from django.conf import settings
from weixin.pay import WeixinPay, WeixinPayError
from alipay import AliPay, AliPayException
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
    def create_order(cls, user, obj, payment_type, device, ip):
        order = PayOrder.objects.create(
            user=user,
            content_object=obj,
            payment_type=payment_type,
            amount=obj.price * 100,
            device=device,
            out_trade_no=cls.generate_out_trade_no()
        )
        name = f'{obj.__class__._meta.verbose_name} {obj.id}'
        data = dict(out_trade_no=order.out_trade_no, amount=obj.price, name=name)
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
            logging.error(e)
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
            logging.error(e)
            return '签名验证失败'

    @classmethod
    def success_callback(cls, data):
        PayOrder.objects.filter(out_trade_no=data['out_trade_no']).update(status=PAYMENT_STATUS_PAID)
