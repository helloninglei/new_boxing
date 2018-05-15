# -*- coding: utf-8 -*-
from datetime.datetime import now
from django.conf import settings
from alipay import AliPay
from biz.models import PayOrder
from biz.constants import PAYMENT_TYPE_ALIPAY, PAYMENT_TYPE_WALLET, PAYMENT_TYPE_WECHAT


app_private_key_string = """
        -----BEGIN RSA PRIVATE KEY-----
        base64 encoded content
        -----END RSA PRIVATE KEY-----
        """

alipay_public_key_string = """
        -----BEGIN PUBLIC KEY-----
        base64 encoded content
        -----END PUBLIC KEY-----
    """

alipay = AliPay(
    appid="",
    app_notify_url=None,
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",
    debug=False,
)

class PayService:

    @classmethod
    def generate_out_trade_no():
        return now().strftime('%y%m%d%H%M%S%f')

    @classmethod
    def create_order(cls, user, obj, payment_type, amount, device):
        order = PayOrder.create(
            user=user,
            content_object=obj,
            payment_type=payment_type,
            amount=amount,
            device=device,
            out_trade_no=cls.generate_out_trade_no()
        )
        if payment_type == PAYMENT_TYPE_ALIPAY:
            pay_func = cls.get_alipay_payment_info
        elif payment_type == PAYMENT_TYPE_WECHAT:
            pay_func = cls.get_wechat_payment_info
        else:
            pay_func = cls.get_wallet_payment_info
        name = f'{obj.__class__._meta.verbose_name} {obj.id}'
        return pay_func(
            out_trade_no=order.out_trade_no,
            amount=amount,
            name=name,
        )

    @classmethod
    def get_alipay_payment_info(cls, out_trade_no, amount, name):
        return alipay.api_alipay_trade_app_pay(
            out_trade_no=out_trade_no,
            total_amount=amount,
            subject=name,
            notify_url=
        )


    @classmethod
    def get_wechat_payment_info(cls, out_trade_no, amount, name):
        pass


    @classmethod
    def get_wallet_payment_info(cls, out_trade_no, amount, name):
        pass
