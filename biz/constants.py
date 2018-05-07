# coding=utf-8

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
MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK = 'INCREASE_MONEY_REJECT_WITHDRAW_REBACK'
MONEY_CHANGE_TYPE_REDUCE_WITHDRAW = 'REDUCE_WITHDRAW'
MONEY_CHANGE_TYPE_REDUCE_ORDER = 'REDUCE_ORDER'
MONEY_CHANGE_TYPE_REDUCE_PAY_FOR_VIDEO = 'REDUCE_PAY_FOR_VIDEO'
MONEY_CHANGE_TYPE_REDUCE_SIGN_UP = 'REDUCE_SIGN_UP'


# 拳豆变动类型
COIN_CHANGE_TYPE_CHOICES = (
    #增加拳豆
    (COIN_CHANGE_TYPE_INCREASE_RECHARGE, '收入-充值'),
    (COIN_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE, '官方充值'),
    (COIN_CHANGE_TYPE_INCREASE_GUESSING_AWARD, '竞猜奖励'),
    (COIN_CHANGE_TYPE_INCREASE_USER_DONATE, '收入-用户打赏'),
    (COIN_CHANGE_TYPE_INCREASE_USER_VIDEO_DONATE, '收入-用户视频打赏'),
    (COIN_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK, '提现被拒绝-退回款项'),
    (COIN_CHANGE_TYPE_INCREASE_WITHDRAW_FAILED_REBACK, '提现失败-退回款项'),
    #减少拳豆
    (COIN_CHANGE_TYPE_REDUCE_USER_DONATE, '支出-用户打赏'),
    (COIN_CHANGE_TYPE_REDUCE_USER_VIDEO_DONATE, '支出-用户视频打赏'),
    (COIN_CHANGE_TYPE_REDUCE_SHOPPING_EXCHANGE, '商城兑换'),
    (COIN_CHANGE_TYPE_REDUCE_GUESSING_BET, '竞猜下注'),
    (COIN_CHANGE_TYPE_REDUCE_START_VOTE, '支出明星投票'),
    (COIN_CHANGE_TYPE_REDUCE_WITHDRAW_APPLY, '提现申请提现'),
)

# 钱包余额变动类型
MONEY_CHANGE_TYPE_CHOICES = (
    #增加金额
    (MONEY_CHANGE_TYPE_INCREASE_RECHARGE, '充值'),
    (MONEY_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE, '官方充值'),
    (MONEY_CHANGE_TYPE_INCREASE_ORDER, '约单(收入)'),
    (MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK, '提现(审核未通过)'),
    #减少金额
    (MONEY_CHANGE_TYPE_REDUCE_WITHDRAW, '提现'),
    (MONEY_CHANGE_TYPE_REDUCE_ORDER, '约单(支出)'),
    (MONEY_CHANGE_TYPE_REDUCE_PAY_FOR_VIDEO, '付费视频'),
    (MONEY_CHANGE_TYPE_REDUCE_SIGN_UP, '报名'),
)

DISCOVER_MESSAGE_REPORT_OTHER_REASON = 7

DISCOVER_MESSAGE_REPORT_CHOICES = (
    (1, '淫秽色情'),
    (2, '赌博诈骗'),
    (3, '恐怖暴力'),
    (4, '违法信息'),
    (5, '诽谤辱骂'),
    (6, '垃圾广告'),
    (DISCOVER_MESSAGE_REPORT_OTHER_REASON, '其他'),
)

BOXER_ALLOWED_COURSES_THAI_BOXING = "THAI_BOXING"
BOXER_ALLOWED_COURSES_MMA = 'MMA'
BOXER_ALLOWED_COURSES_BOXING = 'BOXING'

BOXER_ALLOWED_COURSES_CHOICE = (
    (BOXER_ALLOWED_COURSES_THAI_BOXING, "泰拳"),
    (BOXER_ALLOWED_COURSES_MMA, "MMA"),
    (BOXER_ALLOWED_COURSES_BOXING, "拳击")
)