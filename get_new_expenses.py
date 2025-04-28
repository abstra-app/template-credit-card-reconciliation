from abstra.tasks import *
from abstra.tables import *
import abstra.hooks as ah

import starkbank

from texts import user_not_registered


EXPENSES_TABLE = 'expenses'
TEAM_TABLE = "team"
CARDS_TABLE = "corporate_cards"

# Use Abstra Hooks to create Python endpoints
body, _, _ = ah.get_request()


# get purchase info
purchase_id = body['purchase_id']

purchase_obj = starkbank.CorporatePurchase.get(purchase_id)

value = purchase_obj.amount
timestamp = purchase_obj.created
tags = purchase_obj.tags

card_id = purchase_obj.card_id
corporate_card_obj = starkbank.CorporateCard.get(card_id)
card_number = corporate_card_obj.number


# retriever user
try:
    card_table_row = select_one(CARDS_TABLE, where={'card_number': card_number})
except IndexError:
    print("Card not registered")
    exit()

try: 
    employee_table_row = select_one(TEAM_TABLE, where={'id': card_table_row['team_id']})
except IndexError:
    print(user_not_registered)
    exit()

employee_email = employee_table_row['email']
employee_team_id = employee_table_row['id']


# insert new expense
data = {
    'value': int(value * 100),
    'expense_time': timestamp,
    'justification': None,
    'approval_status': None,
    'team_id': employee_team_id,
    'card_id': card_table_row['id'],
    'tags': tags
}

insert(EXPENSES_TABLE, data)

payload = {"employee_email": employee_email}

send_task("employee_email", payload)
