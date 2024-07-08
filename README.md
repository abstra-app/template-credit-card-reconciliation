# Abstra Template: Credit Card Reconciliation
by Bruno Kuntz – CFO at [Deco.cx](https://deco.cx/)

Workflow designed to check, justify and approve corporate purchases via credit cards.

It features Abstra's native AI for automatically identifying and verifying information within invoices and receipts.

Integrations:
- Starkbank API
- Slack API
- Native email

## Workflow Stages:

![image](https://github.com/abstra-app/template-credit-card-reconciliation/assets/111701155/1d19c703-b5aa-4853-b139-dcc3d66b9f50)

## Stages Overview:

### Get New Expenses (Hook):
  - Triggered when there is a new purchase on a corporate card;
  - Retrieve purchase and credit card information via StarkBank API;
  - Add purchase information to the Abstra Table;
  - Request the credit card holder to fill out a form via e-mail notification.

**IMPORTANT:**
  - Check for recent changes to the StarkBank API;
  - Configure the Hook in your StarkBank workspace with your POST URL.
    
### Justify Expense (Form):
  - Justify each pending expense;
  - Upload the purchase invoice;
  - Check the invoice file via Abstra AI.

### Check for Expenses Pending Approval (Job):
  - Check daily for pending expenses;
  - Request the finance team to fill out the approval form.

### Approve Expenses (Form):
  - Review each expense;
  - Approve or reject it.

### Save Expense to Payables Table (Script):
  - Add approved expenses to the ```payables``` table.

### Notify Expense Rejected on Slack (Script):
  - Notify the reason for rejection on Slack.

## Tables Schema:
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
  - Add the finance e-mail in the ```check_for_expenses_pending_approval.py``` Job:

![image](https://github.com/abstra-app/template-credit-card-reconciliation/assets/111701155/314510cb-7049-44da-aed1-ea3ede2f03d0)

  - Team members and corporate cards (with card number as returned by API) need to be registered to the tables.
