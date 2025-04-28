from abstra.forms import *
from abstra.tasks import *
from abstra.tables import *
import os
import slack_sdk as slack
from slack_sdk.errors import SlackApiError
from abstra.connectors import get_access_token
from texts import expense_rejected_message

task = get_trigger_task()
payload = task.get_payload()
expense = payload["expense"]
requester_team_id = expense["team_id"]
reject_message = expense["reject_message"]

SLACK_TOKEN = get_access_token("slack").token
client = slack.WebClient(token=SLACK_TOKEN)

TEAM_TABLE = 'team'


try:
    requester_team_email = select_one(TEAM_TABLE, where={'id': requester_team_id})['email']
except IndexError:
    print('User is not registered in our database.')
    exit()


def slack_msg(message, channel):
    
    try:
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        assert e.response["error"]


def get_slack_ids_from_email(email):

    user = client.users_lookupByEmail(
        token=SLACK_TOKEN, email=email)['user']['id']

    return user


user_id = get_slack_ids_from_email(requester_team_email)
message = expense_rejected_message.format(reject_message=reject_message)
slack_msg(message, user_id)

task.complete()