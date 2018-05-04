import uuid
from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from biz.models import SmsLog
from biz import redis_keys_const
from biz.redis_client import redis_client


# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.ALI_SMS_ACCESS_KEY_ID, settings.ALI_SMS_ACCESS_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


SMS_TEMPLATES = {
    "verifyCode": {
        "code": "SMS_133964012",
        "text": "尊敬的用户，您的验证码是：{code}。请勿泄露给他人！",
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


class SmsSendTooFrequentException(Exception):
    pass


def _check_ip_frequency(ip):
    if ip:
        redis_check_key = redis_keys_const.SMS_SENDING.format(ip=ip)
        if redis_client.exists(redis_check_key):
            raise SmsSendTooFrequentException
        return redis_check_key


def _send_template_sms(template, mobile, content, params, ip):
    try:
        redis_check_key = _check_ip_frequency(ip)
    except SmsSendTooFrequentException:
        return False

    business_id = uuid.uuid1()

    if settings.ENVIRONMENT == settings.PRODUCTION:
        result = _send_sms(business_id, mobile, template['code'], params)
    else:
        result = 'fake result'

    if redis_check_key:
        redis_client.setex(redis_check_key, settings.ALI_SMS_INTERVAL, "1")

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


def send_verify_code(mobile, verify_code, ip=None):
    template = SMS_TEMPLATES['verifyCode']
    return _send_template_sms(template, mobile, template['text'].format(code=verify_code), {"code": verify_code}, ip=ip)
