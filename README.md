# Template: Credit Card Reconciliation - StarkBank

Workflow designed to justify, check and apporve corporate puchases via StarkBank API integration.

## Workflow Stages:

![image](https://github.com/abstra-app/template-credit-card-reconciliation/assets/111701155/1d19c703-b5aa-4853-b139-dcc3d66b9f50)

## Stages Overview:

### Get New Espenses (Hook):
  - Triggered when there is a new purchase in a corporate card;
  - Retrieve purchase and credit card info via StarkBank API;
  - Add purchase info to Abstra Table;
  - Request credit card holder to fill form via e-mail notification.

    **IMPORTANT:**
    - Check for changes in StarckBank API;
    - Configure Hook in your StarkBank workspace with your POST URL.
    
### Justify Expense (Form):
  - Justify each pending expense;
  - Upload purchase invoice;
  - Check invoice file via Abstra AI.

### Check For Expenses Pending Approval (Job):
  - Check daily for pending expenses;
  - Request finance team to fill approval form.

### Approve Expenses (Form):
  - Review each expense.
  - Approve or reject.

### Save Expense To Payables Table (Script):
  - Add approved expenses to ```payables``` table.

### Notify Expense Rejected On Slack (Script):
  - Notify reason for rejection on Slack.

## Table Schema:
  - team:

    |name|email|
    |:-:|:-:|
    |```str```|```str```|

  - corporate_cards:

    |card_number|team_id|
    |:-:|:-:|
    |```str```|```reference to team(id)```|

  - expenses:

    |expense_time|value|tags|justification|invoice_uuid_path|approval_status|team_id|card_id|
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    |```timestamp```|```int```|```json```|```str```|```str```|```boolean```|```reference to team(id)```|```reference to corporate_cards(id)```|
    | | | |nullable|nullable|nullable| | |

  - payables:

    |value|expense_id|approved_by|
    |:-:|:-:|:-:|
    |```int```|```reference to expenses(id)```|```reference to team(id)```|

## Variables Config:
  - Add your Slack Bot Token in a ```.env``` file in the same directory:

![image](https://github.com/abstra-app/template-credit-card-reconciliation/assets/111701155/1a096b5e-68b6-4b43-8b72-cbdfa44f88cb)
  - Add finance e-mail in the ```check_for_expenses_pending_approval.py``` Job:

![image](https://github.com/abstra-app/template-credit-card-reconciliation/assets/111701155/314510cb-7049-44da-aed1-ea3ede2f03d0)

  - Team members and corporate cards (with card number as returned by API) need to be registred to tables.
