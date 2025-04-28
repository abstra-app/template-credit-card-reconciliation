from abstra.tasks import *
from abstra.tables import *

PAYABLES_TABLE = 'payables'

task = get_trigger_task()
payload = task.get_payload()
expense = payload["expense"]

data = {
    'value': expense['value'],
    'expense_id': expense['id'],
    'approved_by': expense['approved_by'],
}

insert(PAYABLES_TABLE, data)

task.complete()