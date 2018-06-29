from django.db.transaction import atomic
from biz.models import MoneyChangeLog, User
from django.db.models import F


class ChangeMoneyException(Exception):
    pass


@atomic
def change_money(user, amount, change_type, remarks=None):
    money_change_log = MoneyChangeLog.objects.create(
        user=user, change_type=change_type, last_amount=user.money_balance, change_amount=amount,
        remain_amount=user.money_balance + amount, operator=user, remarks=remarks
    )
    rows = User.objects.filter(pk=user.id, money_balance__gte=-amount).update(money_balance=F('money_balance') + amount)
    if rows == 0:
        raise ChangeMoneyException('余额不足')
    return money_change_log
