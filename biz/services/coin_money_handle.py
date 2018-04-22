# -*- coding: utf-8 -*-
import math
from django.db import transaction

from biz.models import CoinChangeLog, MoneyChangeLog


@transaction.atomic
def coin_handle(effect_user, operator, change_amount=0, change_reason=None):
    lastAmount = effect_user.coin_balance
    remainAmount = int(lastAmount) + int(change_amount)

    coin_change_log = CoinChangeLog.objects.create(user=effect_user,
                                                   operator=operator,
                                                   lastAmount=lastAmount,
                                                   changeAmount=change_amount,
                                                   remainAmount=remainAmount,
                                                   change_reason=change_reason
                                                    )

    effect_user.coin_balance += int(change_amount)
    effect_user.save()
    return coin_change_log

@transaction.atomic
def money_handle(effect_user, operator, change_amount=0, change_reason=None):
    lastAmount = effect_user.money_balance
    remainAmount = int(lastAmount) + int(math.floor(float(change_amount)*100))

    money_change_log = MoneyChangeLog.objects.create(user=effect_user,
                                                     operator=operator,
                                                     lastAmount=lastAmount,
                                                     changeAmount=change_amount,
                                                     remainAmount=remainAmount,
                                                     change_reason=change_reason)

    effect_user.money_balance += int(math.floor(float(change_amount)*100))
    effect_user.save()
    return money_change_log