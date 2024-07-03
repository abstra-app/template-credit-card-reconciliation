from abstra.workflows import *
from abstra.tables import *

PAYABLES_TABLE = 'payables'

expense = get_data('expense')

data = {
    'value': expense['value'],
    'expense_id': expense['id'],
    'approved_by': expense['approved_by'],
}

insert(PAYABLES_TABLE, data)
