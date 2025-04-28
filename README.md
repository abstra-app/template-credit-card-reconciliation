# Abstra Template: Credit Card Reconciliation
by Bruno Kuntz – CFO at [Deco.cx](https://deco.cx/)

## How it works:
This project includes a credit card expense evaluation system implemented using Abstra and Python scripts. The system integrates with Slack to send alerts for rejected expenses.

Integrations:
  - Starkbank
  - Slack
    
To customize this template for your team and build a lot more, [book a demonstration here.](https://meet.abstra.app/demo?url=template-credit-card-reconciliation)

![a credit card expense evaluation workflow built in Abstra](https://github.com/user-attachments/assets/97223b91-bc14-43b7-9159-7beccdff3b96)

## Initial Configuration:
To use this project, some initial configurations are necessary:

1. **Python Version**: Ensure Python version 3.9 or higher is installed on your system.
2. **Integrations**: To connect to Slack, this template uses Abstra connectors. To connect, simply open your project in [Abstra Cloud Console](https://cloud.abstra.io/projects/), add the Slack connector, and authorize it.
3. **Environment Variables**:

    The following environment variables are required for both local development and online deployment:
  
    - `FINANCE_TEAM_EMAIL`: Email address for the finance team (or any other team responsible for verifying expenses).
  
    For local development, create a `.env` file at the root of the project and add the variables listed above (as in `.env.example`). For online deployment, configure these variables in your [environment settings](https://docs.abstra.io/cloud/envvars).

4. **Dependencies**: To install the necessary dependencies for this project, a `requirements.txt` file is provided. This file includes all the required libraries.

   Follow these steps to install the dependencies:

   1. Open your terminal and navigate to the project directory.
   2. Run the following command to install the dependencies from `requirements.txt`:
  
      ```sh
      pip install -r requirements.txt
      ```
5. **Access Control**: The generated form is protected by default. For local testing, no additional configuration is necessary. However, for cloud usage, you need to add your own access rules. For more information on how to configure access control, refer to the [Abstra access control documentation](https://docs.abstra.io/concepts/access-control).
   
6. **Database configuration**: Set up your database tables in Abstra Cloud Tables according to the schema defined in `abstra-tables.json`.

    To automatically create the table schema, follow these steps:
  
    1. Open your terminal and navigate to the project directory.
  
    3. Run the following command to install the table schema from `abstra-tables.json`:
       ```sh
       abstra restore
       ```
   For guidance on creating and managing tables in Abstra, refer to the [Abstra Tables documentation](https://docs.abstra.io/cloud/tables).
   
5. **Internal Registration**: Team members and corporate cards (with card number as returned by API) need to be registered to the tables `team` and `corporate_cards`.

7. **Local Usage**: To access the local editor with the project, use the following command:

   ```sh
      abstra editor path/to/your/project/folder/
   ```
   
## General Workflow:
To implement this system use the following scripts:

### Getting New Expenses:
To retrieve and justify new purchases on corporate cards registered in the tables, use:
  - **get_new_expenses.py**: Script triggered by a new purchase on a corporate card, retrieving purchase details from the Starkbank API.
  - **justify_expense.py**: Script to generate a form requesting the credit card holder (as registered in the tables) to justify the pending expense and upload the purchase invoice, which is validated with Abstra AI.

**IMPORTANT:**
  - Check for recent changes to the StarkBank API;
  - Configure the Hook in your StarkBank workspace with your POST URL.

### Approving Expenses:
To retrieve and evaluate pending expenses, use:
  - **check_for_expenses_pending_approval.py**: Daily script to get expenses for evaluation.
  - **approve_expenses.py**: Script to generate a form where the expenses can be reviewed and approved/rejected.
  - **save_expense_to_payables_table.py**: Script to save approved expenses to the `payables` database.
  - **expense_reject_notification.py**: Script to send a notification to the requester on Slack about the rejection of an expense. 

If you're interested in customizing this template for your team in under 30 minutes, [book a customization session here.](https://meet.abstra.app/demo?url=template-credit-card-reconciliation)
