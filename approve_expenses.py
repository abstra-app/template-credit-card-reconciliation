from abstra.tasks import *
from abstra.tables import *
from abstra.forms import *

import pandas as pd
from datetime import datetime
from texts import expense_summary_approval, user_not_registered, no_expenses_pending_approval

# receiving task to get notification e-mail
tasks = get_tasks()


EXPENSES_TABLE = 'expenses'
TEAM_TABLE = "team"


def render_reject_input(partial):

    if partial['approval_status'] == False:
        return Page().read_textarea('Reason for Rejection:', key='reject_message')


def run_steps_page(expenses):

    expense_pages = []

    for expense in expenses:
        value = f"R$ {expense['value'] / 100:.2f}"
        time = datetime.strptime(expense['expense_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        time = time.strftime('%d/%m/%Y %H:%M')
        
        tags_str = ', '.join(expense['tags']) if expense['tags'] else 'None'

        expense_pages.append(
            Page()
            .display_markdown(expense_summary_approval.format(timestamp=time, value=value, justification=expense['justification'], tags=tags_str))
            .read_toggle('', on_text='Approved', off_text='Rejected', initial_value=True, key='approval_status')
            .reactive(render_reject_input)
            )

    return run_steps(expense_pages)

for task in tasks:
    # get user information
    user = get_user().claims['email']

    try:
        user_team_row = select_one(TEAM_TABLE, where={'email': user})
        if not user_team_row:
            raise IndexError
    except IndexError:
        display(user_not_registered, end_program=True, size='large')

    user_team_id = user_team_row['id']

    # approve or reject expenses
    expenses = select(EXPENSES_TABLE, where={'approval_status': None})
    approved_expenses = []
    rejected_expenses = []

    if not expenses:
        display(no_expenses_pending_approval, end_program=True, size='large')

    expenses_approval_info = run_steps_page(expenses)

    for i in range(len(expenses)):
        approval_status = expenses_approval_info[i]['approval_status']
        expenses[i]['approval_status'] = approval_status

        if approval_status == False:
            expenses[i]['reject_message'] = expenses_approval_info[i]['reject_message']
            rejected_expenses.append(expenses[i])

        else:
            expenses[i]['approved_by'] = user_team_id
            approved_expenses.append(expenses[i])

        update(EXPENSES_TABLE, where={'id': expenses[i]['id']}, set={'approval_status': approval_status})

    if approved_expenses:
        for expense in approved_expenses:
            payload = {}
            payload["expense"] = expense
            send_task("approved_expenses", payload)
    if rejected_expenses:
        for expense in rejected_expenses:
            payload = {}
            payload["expense"] = expense
            send_task("rejected_expenses", payload)

