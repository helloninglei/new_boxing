# -*- coding: utf-8 -*-
import math
from django.db import transaction

from biz.models import CoinChangeLog, MoneyChangeLog


@transaction.atomic
def coin_handle(effect_user, operator, change_amount=0, change_type=None, remarks=None):
    lastAmount = effect_user.coin_balance
    remainAmount = int(lastAmount) + int(change_amount)

    coin_change_log = CoinChangeLog.objects.create(user=effect_user,
                                                   operator=operator,
                                                   lastAmount=lastAmount,
                                                   changeAmount=change_amount,
                                                   change_type=change_type,
                                                   remainAmount=remainAmount,
                                                   remarks=remarks
                                                    )

    effect_user.coin_balance += int(change_amount)
    effect_user.save()
    return coin_change_log

@transaction.atomic
def money_handle(effect_user, operator, change_amount=0, change_type=None, remarks=None):
    lastAmount = effect_user.money_balance
    remainAmount = int(lastAmount) + int(math.floor(float(change_amount)*100))

    money_change_log = MoneyChangeLog.objects.create(user=effect_user,
                                                     operator=operator,
                                                     lastAmount=lastAmount,
                                                     changeAmount=change_amount,
                                                     change_type=change_type,
                                                     remainAmount=remainAmount,
                                                     remarks=remarks)

    effect_user.money_balance += int(math.floor(float(change_amount)*100))
    effect_user.save()
    return money_change_log

def write_coin_and_money_log_remarks(request):
    remarks = request.data.get('remarks',None)
    return remarks