from abstra.workflows import *
from abstra.tables import *
from texts import thread_title_pending_approval
import os


EXPENSES_TABLE = 'expenses'
expenses = select(EXPENSES_TABLE, where={'approval_status': None})

finance_email = os.environ["FINANCE_TEAM_EMAIL"]
                 
if expenses:
    set_data('finance_email', finance_email)
    set_title(thread_title_pending_approval)
