from datetime import datetime

from biz import constants
from biz.models import OperationLog


def log(refer_type, refer_pk, operator, operation_type, content):
    return OperationLog.objects.create(
        refer_type=refer_type,
        refer_pk=refer_pk,
        operator=operator,
        operation_type=operation_type,
        content=content,
        timestamp=datetime.now()
    )


def log_boxer_identification_operation(identification_id, operator, operation_type, content):
    return log(constants.OperationTarget.BOXER_IDENTIFICATION, identification_id, operator, operation_type, content)
