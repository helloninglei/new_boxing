from biz.models import MoneyChangeLog
from django.db.transaction import atomic


@atomic
def change_money(user, amount, change_type):
    MoneyChangeLog.objects.create(
        user=user, change_type=change_type, last_amount=user.money_balance, change_amount=amount,
        remain_amount=user.money_balance + amount, operator=user
    )
    user.money_balance += amount
    user.save()
