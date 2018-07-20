from datetime import timedelta

from django.conf import settings

MESSAGE_TYPE_ONLY_TEXT = 'only_text'
MESSAGE_TYPE_HAS_IMAGE = 'has_image'
MESSAGE_TYPE_HAS_VIDEO = 'has_video'

HOT_VIDEO_USER_ID = 10
FRIDAY_USER_ID = 11
BOXING_USER_ID = 12
SERVICE_USER_ID = 13

USER_IDENTITY_DICT = {
    'hot_video': HOT_VIDEO_USER_ID,
    'friday': FRIDAY_USER_ID,
    'boxing': BOXING_USER_ID,
    'service': SERVICE_USER_ID
}

FAMOUS_USER_DICT = {
    13261843166: 14,  # '跑酷'
    17611655266: 15,  # '熊呈呈'
    13501224847: 16,  # '徐晓冬'
    13810578320: 17,  # '吴紫龙'
    18888888888: 18,  # '拳城出击——中华武术大会'
    13636843135: 1082,  # 庞祥
}

BOXER_AUTHENTICATION_STATE_WAITING = "WAITING"
BOXER_AUTHENTICATION_STATE_REFUSE = 'REFUSE'
BOXER_AUTHENTICATION_STATE_APPROVED = 'APPROVED'

BOXER_AUTHENTICATION_STATE_CHOICE = (
    (BOXER_AUTHENTICATION_STATE_WAITING, "待审核"),
    (BOXER_AUTHENTICATION_STATE_REFUSE, "已驳回"),
    (BOXER_AUTHENTICATION_STATE_APPROVED, "已通过")
)

COIN_CHANGE_TYPE_INCREASE_RECHARGE = 'INCREASE_COIN_RECHARGE'
COIN_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE = 'INCREASE_COIN_OFFICIAL_RECHARGE'
COIN_CHANGE_TYPE_INCREASE_GUESSING_AWARD = 'INCREASE_GUESSING_AWARD'
COIN_CHANGE_TYPE_INCREASE_USER_DONATE = 'INCREASE_USER_DONATE'
COIN_CHANGE_TYPE_INCREASE_USER_VIDEO_DONATE = 'INCREASE_USER_VIDEO_DONATE'
COIN_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK = 'INCREASE_COIN_REJECT_WITHDRAW_REBACK'
COIN_CHANGE_TYPE_INCREASE_WITHDRAW_FAILED_REBACK = 'INCREASE_WITHDRAW_FAILED_REBACK'
COIN_CHANGE_TYPE_REDUCE_USER_DONATE = 'REDUCE_USER_DONATE'
COIN_CHANGE_TYPE_REDUCE_USER_VIDEO_DONATE = 'REDUCE_USER_VIDEO_DONATE'
COIN_CHANGE_TYPE_REDUCE_SHOPPING_EXCHANGE = 'REDUCE_SHOPPING_EXCHANGE'
COIN_CHANGE_TYPE_REDUCE_GUESSING_BET = 'REDUCE_GUESSING_BET'
COIN_CHANGE_TYPE_REDUCE_START_VOTE = 'REDUCE_START_VOTE'
COIN_CHANGE_TYPE_REDUCE_WITHDRAW_APPLY = 'REDUCE_WITHDRAW_APPLY'

MONEY_CHANGE_TYPE_INCREASE_RECHARGE = 'INCREASE_MONEY_RECHARGE'
MONEY_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE = 'INCREASE_MONEY_OFFICIAL_RECHARGE'
MONEY_CHANGE_TYPE_INCREASE_ORDER = 'INCREASE_ORDER'
MONEY_CHANGE_TYPE_INCREASE_ORDER_OVERDUE = 'INCREASE_ORDER_OVERDUE'
MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK = 'INCREASE_MONEY_REJECT_WITHDRAW_REBACK'
MONEY_CHANGE_TYPE_REDUCE_WITHDRAW = 'REDUCE_WITHDRAW'
MONEY_CHANGE_TYPE_REDUCE_ORDER = 'REDUCE_ORDER'
MONEY_CHANGE_TYPE_REDUCE_PAY_FOR_VIDEO = 'REDUCE_PAY_FOR_VIDEO'
MONEY_CHANGE_TYPE_REDUCE_SIGN_UP = 'REDUCE_SIGN_UP'

# 拳豆变动类型
COIN_CHANGE_TYPE_CHOICES = (
    # 增加拳豆
    (COIN_CHANGE_TYPE_INCREASE_RECHARGE, '收入-充值'),
    (COIN_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE, '官方充值'),
    (COIN_CHANGE_TYPE_INCREASE_GUESSING_AWARD, '竞猜奖励'),
    (COIN_CHANGE_TYPE_INCREASE_USER_DONATE, '收入-用户打赏'),
    (COIN_CHANGE_TYPE_INCREASE_USER_VIDEO_DONATE, '收入-用户视频打赏'),
    (COIN_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK, '提现被拒绝-退回款项'),
    (COIN_CHANGE_TYPE_INCREASE_WITHDRAW_FAILED_REBACK, '提现失败-退回款项'),
    # 减少拳豆
    (COIN_CHANGE_TYPE_REDUCE_USER_DONATE, '支出-用户打赏'),
    (COIN_CHANGE_TYPE_REDUCE_USER_VIDEO_DONATE, '支出-用户视频打赏'),
    (COIN_CHANGE_TYPE_REDUCE_SHOPPING_EXCHANGE, '商城兑换'),
    (COIN_CHANGE_TYPE_REDUCE_GUESSING_BET, '竞猜下注'),
    (COIN_CHANGE_TYPE_REDUCE_START_VOTE, '支出明星投票'),
    (COIN_CHANGE_TYPE_REDUCE_WITHDRAW_APPLY, '提现申请提现'),
)

# 钱包余额变动类型
MONEY_CHANGE_TYPE_CHOICES = (
    # 增加金额
    (MONEY_CHANGE_TYPE_INCREASE_RECHARGE, '充值'),
    (MONEY_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE, '官方充值'),
    (MONEY_CHANGE_TYPE_INCREASE_ORDER, '约单(收入)'),
    (MONEY_CHANGE_TYPE_INCREASE_ORDER_OVERDUE, '约单(过期)'),
    (MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK, '提现(审核未通过)'),
    # 减少金额
    (MONEY_CHANGE_TYPE_REDUCE_WITHDRAW, '提现'),
    (MONEY_CHANGE_TYPE_REDUCE_ORDER, '约单(支出)'),
    (MONEY_CHANGE_TYPE_REDUCE_PAY_FOR_VIDEO, '付费视频'),
    (MONEY_CHANGE_TYPE_REDUCE_SIGN_UP, '报名'),
)

REPORT_OTHER_REASON = 7

REPORT_REASON_CHOICES = (
    (1, '淫秽色情'),
    (2, '赌博诈骗'),
    (3, '恐怖暴力'),
    (4, '违法信息'),
    (5, '诽谤辱骂'),
    (6, '垃圾广告'),
    (REPORT_OTHER_REASON, '其他'),
)

REPORT_STATUS_NOT_PROCESSED = 1
REPORT_STATUS_PROVED_FALSE = 2
REPORT_STATUS_DELETED = 3

REPORT_STATUS_CHOICES = (
    (REPORT_STATUS_NOT_PROCESSED, '未处理'),
    (REPORT_STATUS_PROVED_FALSE, '核实为假'),
    (REPORT_STATUS_DELETED, '已删除')
)


class OperationTarget:
    BOXER_IDENTIFICATION = 'BOXER_IDENTIFICATION'

    CHOICES = (
        (BOXER_IDENTIFICATION, '拳手认证'),

    )


class OperationType:
    BOXER_AUTHENTICATION_APPROVED = 'BOXER_AUTHENTICATION_APPROVED'
    BOXER_AUTHENTICATION_REFUSE = 'BOXER_AUTHENTICATION_REFUSE'
    BOXER_ORDER_LOCK = 'LOCK'
    BOXER_ORDER_UNLOCK = 'UNLOCK'

    CHOICES = (
        (BOXER_AUTHENTICATION_APPROVED, '拳手认证通过'),
        (BOXER_AUTHENTICATION_REFUSE, '拳手认证驳回'),
        (BOXER_ORDER_LOCK, '拳手接单状态锁定'),
        (BOXER_ORDER_UNLOCK, '拳手接单状态解锁'),
    )


BOXER_ALLOWED_COURSES_THAI_BOXING = "泰拳"
BOXER_ALLOWED_COURSES_MMA = 'MMA'
BOXER_ALLOWED_COURSES_BOXING = '拳击'

BOXER_ALLOWED_COURSES_CHOICE = (
    (BOXER_ALLOWED_COURSES_THAI_BOXING, "泰拳"),
    (BOXER_ALLOWED_COURSES_MMA, "MMA"),
    (BOXER_ALLOWED_COURSES_BOXING, "拳击")
)

# 举报 (model名, type_id)
REPORT_OBJECT_DICT = {
    'message': 1,
    'comment': 2,
    'hot_video': 3,
}

# 评论
COMMENT_OBJECT_DICT = {
    'message': 1,
    'hot_video': 2,
    'game_news': 3,
}

# 分享
SHARE_OBJECT_LIST = (
    'message',
    'hot_video',
    'game_news',
    'boxer',
)

# 支付
PAYMENT_OBJECT_DICT = {
    'hot_video': 1,
    'course_order': 2
}

PAYMENT_STATUS_UNPAID = 1
PAYMENT_STATUS_PAID = 2

ORDER_PAYMENT_STATUS = (
    (PAYMENT_STATUS_UNPAID, '未支付'),
    (PAYMENT_STATUS_PAID, '已支付'),
)

COURSE_ORDER_STATUS_NOT_CONFIRMED = 1
COURSE_ORDER_STATUS_BOXER_CONFIRMED = 2
COURSE_ORDER_STATUS_USER_CONFIRMED = 3

COURSE_PAYMENT_STATUS_UNPAID = 1
COURSE_PAYMENT_STATUS_WAIT_USE = 2
COURSE_PAYMENT_STATUS_WAIT_COMMENT = 3
COURSE_PAYMENT_STATUS_FINISHED = 4
COURSE_PAYMENT_STATUS_OVERDUE = 5

COURSE_ORDER_PAYMENT_STATUS = (
    (COURSE_PAYMENT_STATUS_UNPAID, '未支付'),
    (COURSE_PAYMENT_STATUS_WAIT_USE, '待使用'),
    (COURSE_PAYMENT_STATUS_WAIT_COMMENT, '待评论'),
    (COURSE_PAYMENT_STATUS_FINISHED, '已完成'),
    (COURSE_PAYMENT_STATUS_OVERDUE, '已过期'),
)

COURSE_ORDER_CONFIRM_STATUS = (
    (COURSE_ORDER_STATUS_NOT_CONFIRMED, '未确认'),
    (COURSE_ORDER_STATUS_BOXER_CONFIRMED, '拳手已确认'),
    (COURSE_ORDER_STATUS_USER_CONFIRMED, '用户已确认')
)

PAYMENT_TYPE_ALIPAY = 1
PAYMENT_TYPE_WECHAT = 2
PAYMENT_TYPE_WALLET = 3

PAYMENT_TYPE = (
    (PAYMENT_TYPE_ALIPAY, '支付宝'),
    (PAYMENT_TYPE_WECHAT, '微信'),
    (PAYMENT_TYPE_WALLET, '余额')
)

DEVICE_PLATFORM_IOS = 1
DEVICE_PLATFORM_ANDROID = 2

DEVICE_PLATFORM = (
    (DEVICE_PLATFORM_IOS, 'iOS'),
    (DEVICE_PLATFORM_ANDROID, 'Android'),
)

BANNER_LINK_TYPE_IN_APP_WEB = 1
BANNER_LINK_TYPE_OUT_APP_WEB = 2
BANNER_LINK_TYPE_IN_APP_NATIVE = 3

BANNER_LINK_TYPE = (
    (BANNER_LINK_TYPE_IN_APP_WEB, 'app内网页跳转'),
    (BANNER_LINK_TYPE_OUT_APP_WEB, 'app外网页跳转'),
    (BANNER_LINK_TYPE_IN_APP_NATIVE, 'app内本地跳转'),
)

APP_JUMP_OBEJCT_NEWS = 'game_news'

# banner 跳转对象model
BANNER_LINK_MODEL_TYPE = (
    # 'game_votes',  # 赛事投票
    # 'game_apply',  # 赛事报名
    APP_JUMP_OBEJCT_NEWS,  # 赛事资讯
)

WITHDRAW_STATUS_WAITING = 'WAITING'
WITHDRAW_STATUS_APPROVED = 'APPROVED'
WITHDRAW_STATUS_REJECTED = 'REJECTED'

WITHDRAW_STATUS_CHOICE = (
    (WITHDRAW_STATUS_WAITING, "审核中"),
    (WITHDRAW_STATUS_APPROVED, "审核通过"),
    (WITHDRAW_STATUS_REJECTED, "审核未通过")
)

WITHDRAW_MIN_CONFINE = 200  # unit:分

OFFICIAL_ACCOUNT_CHANGE_TYPE_RECHARGE = 1
OFFICIAL_ACCOUNT_CHANGE_TYPE_WITHDRAW = 2
OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_COURSE = 3
OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_VIDEO = 4

OFFICIAL_ACCOUNT_CHANGE_TYPE_CHOICE = (
    (OFFICIAL_ACCOUNT_CHANGE_TYPE_RECHARGE, "充值"),
    (OFFICIAL_ACCOUNT_CHANGE_TYPE_WITHDRAW, "提现"),
    (OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_COURSE, "约单"),
    (OFFICIAL_ACCOUNT_CHANGE_TYPE_BUY_VIDEO, "热门视频")
)

if settings.ENVIRONMENT != settings.PRODUCTION:
    DELAY_SEVEN_DAYS = timedelta(minutes=5)
else:
    DELAY_SEVEN_DAYS = timedelta(days=7)

# user type
USER_TYPE_BOXER = 1
USER_TYPE_CELEBRITY = 2
USER_TYPE_MEDIA = 3
USER_TYPE_CHOICE = (
    (USER_TYPE_BOXER, "拳手"),
    (USER_TYPE_CELEBRITY, "名人"),
    (USER_TYPE_MEDIA, "自媒体")
)
USER_TYPE_MAP = dict(USER_TYPE_CHOICE)

# user default bio
DEFAULT_BIO_FORMAT = "{}好懒哦，什么都没留下～"
DEFAULT_BIO_OF_MEN = DEFAULT_BIO_FORMAT.format("小哥哥")
DEFAULT_BIO_OF_WOMEN = DEFAULT_BIO_FORMAT.format("小姐姐")

# chat rooms
CHAT_ROOM_NAME = "拳城BB"
CHAT_ROOM_DESCRIPTION = "拳城出击聊天室"
CHAT_ROOM_MAXUSERS = 10000  # 聊天室最大用户数量

# user default nickname、avatar
DEFAULT_NICKNAME_FORMAT = "拳城{}"
DEFAULT_AVATAR = ""

MAX_HOT_VIDEO_BIND_USER_COUNT = 7

