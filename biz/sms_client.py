"""
验证码：
不用业务场景可能有不同的短信验证码发送规则，可以使用不同view来处理，但不同的view均需加入短信接口的保护措施。
如果其他业务场景可以复用view，需要将业务场景加入docstring。
"""

import uuid
import random
from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from biz.models import SmsLog
from biz.redis_client import redis_client
from biz.redis_const import SEND_VERIFY_CODE, SENDING_VERIFY_CODE, SEND_VERIFY_CODE_INTERVAL,\
    VERIFY_CODE_EXPIRED_INTERVAL


# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.ALI_SMS_ACCESS_KEY_ID, settings.ALI_SMS_ACCESS_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


SMS_TEMPLATES = {
    "verifyCode": {
        "code": "SMS_134110376",
        "text": "您的验证码：{code}，您正进行身份验证，打死不告诉别人！",
    }
}


def _send_sms(business_id, mobile, template_code, template_param):
    sms_request = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    sms_request.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        sms_request.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    sms_request.set_OutId(business_id)

    # 短信签名
    sms_request.set_SignName("拳城出击")

    # 短信发送的号码列表，必填。
    sms_request.set_PhoneNumbers(mobile)

    # 调用短信发送接口，返回json
    sms_response = acs_client.do_action_with_exception(sms_request)

    return sms_response


def _send_template_sms(template, mobile, content, params):

    business_id = uuid.uuid1()

    if settings.ENVIRONMENT == settings.PRODUCTION:
        result = _send_sms(business_id, mobile, template['code'], params)
    else:
        result = 'fake result'

    _sms_send_log(mobile, template, content, business_id, result)

    return True


def _sms_send_log(mobile, template, content, business_id, result):
    return SmsLog.objects.create(
        mobile=mobile,
        template_code=template['code'],
        content=content,
        business_id=business_id,
        result=result
    )


def send_verify_code(mobile, interval=SEND_VERIFY_CODE_INTERVAL):
    template = SMS_TEMPLATES['verifyCode']
    verify_code = random.randint(100000, 999999)
    redis_pipeline = redis_client.pipeline()
    redis_pipeline.setex(SENDING_VERIFY_CODE.format(mobile=mobile), interval, verify_code)
    redis_pipeline.setex(SEND_VERIFY_CODE.format(mobile=mobile), VERIFY_CODE_EXPIRED_INTERVAL, verify_code)
    redis_pipeline.execute()
    return _send_template_sms(template, mobile, template['text'].format(code=verify_code), {"code": verify_code})
