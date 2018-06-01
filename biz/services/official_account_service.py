from biz.models import OfficialAccountChangeLog


def create_official_account_change_log(change_amount, related_user, change_type, remarks):
    OfficialAccountChangeLog.objects.create(
        change_amount=change_amount, related_user=related_user, change_type=change_type, remarks=remarks
    )
