from biz.models import OfficialAccountChangeLog


def change_official_account(change_amount, related_user, change_type, remarks):
    OfficialAccountChangeLog.objects.create(
        change_amount=change_amount, related_user=related_user, change_type=change_type, remarks=remarks
    )
