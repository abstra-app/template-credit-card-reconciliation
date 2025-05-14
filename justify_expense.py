from abstra.tasks import *
from abstra.tables import *
from abstra.forms import *
from abstra.ai import prompt
from abstra.common import get_persistent_dir

from texts import expense_summary_justification, user_not_registered, no_expenses_pending_justification
from texts import not_invoice_error, value_mismatch_error

from datetime import datetime
import uuid, os

tasks = get_tasks()


EXPENSES_TABLE = 'expenses'
TEAM_TABLE = 'team'

INVOICE_DIR = get_persistent_dir() / 'expense-invoices'
    

# check if the file is an invoice and if values match
def validate_invoice(value):

    def __validate(partial):
        
        if not partial['invoice']:
            return

        invoice_info = prompt(
            ["Here is an invoice", partial['invoice']],
            format={
                "is_invoice": {"type": "boolean", "description": "Is this an invoice?"},
                "invoice_value": {"type": "string", "description": "What is the value of the service in dollars?"},
                "value_match": {"type": "boolean", "description": f"Is the value of the service in dollars approximately equal to {value}?"},
                }
            )
        
        if not invoice_info['is_invoice']:
            return not_invoice_error
        
        elif not invoice_info['value_match']:
            return value_mismatch_error.format(invoice_value=invoice_info['invoice_value'])
        
    return __validate


def run_steps_page(pending_expenses):

    pending_pages = []

    for expense in pending_expenses:
        numeric_value = round(expense['value'] / 100, 2)
        formatted_value = "$ {:.2f}".format(numeric_value)
        time = datetime.strptime(expense['expense_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        time = time.strftime('%d/%m/%Y %H:%M')

        tags_str = ', '.join(expense['tags']) if expense['tags'] else 'None'

        pending_pages.append(
            Page(validate=validate_invoice(formatted_value))
            .display_markdown(expense_summary_justification.format(timestamp=time, value=formatted_value, tags=tags_str))
            .read_image('Upload Purchase Invoice:', key='invoice', required=True)
            .read_textarea(f"Justify Expense:", key='justification', required=True)
        )

    return run_steps(pending_pages)

for task in tasks:

    # get user information
    employee_email = get_user().claims['email']

    try:
        employee_team_id = select_one(TEAM_TABLE, where={'email': employee_email})['id']
    except IndexError:
        display(user_not_registered, end_program=True, size='large')

    expenses = select(EXPENSES_TABLE, where={'team_id': employee_team_id, 'approval_status': None, 'justification': None})

    if not expenses:
        task.complete()
        display(no_expenses_pending_justification, end_program=True, size='large')


    # build justification pages
    justifications = run_steps_page(expenses)

    for i in range(len(expenses)):
        justifications[i]['id'] = expenses[i]['id']


    # update expenses with justifications and invoice paths / save invoices
    if not os.path.exists(INVOICE_DIR):
        os.makedirs(INVOICE_DIR)

    for page in justifications:
        expense_id = page['id']

        invoice_uuid_path = f"{uuid.uuid4()}.jpg"
        invoice_file = page['invoice'].file
        invoice_path = INVOICE_DIR / invoice_uuid_path

        with open(invoice_path, 'wb') as f:
            f.write(invoice_file.read())

        update(EXPENSES_TABLE, where={'id': expense_id}, set={'justification': page['justification'], 'invoice_uuid_path': invoice_uuid_path})


    task.complete()