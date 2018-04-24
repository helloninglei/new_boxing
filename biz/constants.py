# coding=utf-8
<<<<<<< HEAD


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
    (COIN_CHANGE_TYPE_INCREASE_RECHARGE, u'收入-充值'),
    (COIN_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE, u'官方充值'),
    (COIN_CHANGE_TYPE_INCREASE_GUESSING_AWARD, u'竞猜奖励'),
    (COIN_CHANGE_TYPE_INCREASE_USER_DONATE, u'收入-用户打赏'),
    (COIN_CHANGE_TYPE_INCREASE_USER_VIDEO_DONATE, u'收入-用户视频打赏'),
    (COIN_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK, u'提现被拒绝-退回款项'),
    (COIN_CHANGE_TYPE_INCREASE_WITHDRAW_FAILED_REBACK, u'提现失败-退回款项'),
    #减少拳豆
    (COIN_CHANGE_TYPE_REDUCE_USER_DONATE, u'支出-用户打赏'),
    (COIN_CHANGE_TYPE_REDUCE_USER_VIDEO_DONATE, u'支出-用户视频打赏'),
    (COIN_CHANGE_TYPE_REDUCE_SHOPPING_EXCHANGE, u'商城兑换'),
    (COIN_CHANGE_TYPE_REDUCE_GUESSING_BET, u'竞猜下注'),
    (COIN_CHANGE_TYPE_REDUCE_START_VOTE, u'支出明星投票'),
    (COIN_CHANGE_TYPE_REDUCE_WITHDRAW_APPLY, u'提现申请提现'),
)

# 钱包余额变动类型
MONEY_CHANGE_TYPE_CHOICES = (
    #增加金额
    (MONEY_CHANGE_TYPE_INCREASE_RECHARGE, u'充值'),
    (MONEY_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE, u'官方充值'),
    (MONEY_CHANGE_TYPE_INCREASE_ORDER,u'约单(收入)'),
    (MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK, u'提现(审核未通过)'),
    #减少金额
    (MONEY_CHANGE_TYPE_REDUCE_WITHDRAW, u'提现'),
    (MONEY_CHANGE_TYPE_REDUCE_ORDER,u'约单(支出)'),
    (MONEY_CHANGE_TYPE_REDUCE_PAY_FOR_VIDEO, u'付费视频'),
    (MONEY_CHANGE_TYPE_REDUCE_SIGN_UP, u'报名'),
)
=======
>>>>>>> master
