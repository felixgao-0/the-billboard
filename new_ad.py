"""
Rotates a new ad in at set times
Run via cron job
"""

import os
import sys
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv
from database import Database

load_dotenv()

db_conn_params = {
    "dbname": "felixgao_the_billboard",
    "user": "felixgao",
    "password": os.environ['DB_PASSWORD'],
    "host": "hackclub.app",
    "port": 5432
}

#BOT_ID = os.environ.get("BOT_ID")
ADMINS = os.environ.get("ADMINS").split(",") if os.environ.get("ADMINS") else []
AUTHORIZED = os.environ.get("AUTHORIZED").split(",") if os.environ.get("AUTHORIZED") else []

CHANNEL_ID = "C08MRG6NK1V"  # the-billboard
#CHANNEL_ID = "C08NU78MR4G"  # the-billboard-DEV

try:
    client = WebClient(token=os.environ['BILLBOARD_BOT_TOKEN'])
    user_client = WebClient(token=os.environ['BILLBOARD_USERBOT_TOKEN'])
except SlackApiError as e:
    print(f"Error: {e}")
    sys.exit(1)

try:
    response = client.conversations_history(channel=CHANNEL_ID)
    messages = response["messages"]

    channel_info = client.conversations_info(channel=CHANNEL_ID)
    if not channel_info["channel"]["creator"] == "U07BU2HS17Z":
        raise ValueError("MISSION ABORT, MISSION ABORT. Channel manager safeguard triggered.")

    if CHANNEL_ID not in ['C08MRG6NK1V']:
        raise ValueError("MISSION ABORT, MISSION ABORT. Channel ID safeguard triggered.")

    for msg in messages:
        ts = msg["ts"]
        user = msg["user"]
        if user in (ADMINS + AUTHORIZED):
            continue

        user_client.chat_delete(channel=CHANNEL_ID, ts=ts)
        time.sleep(0.1)  # rate limiting lolies

except SlackApiError as e:
    print(f"Error: {e}")

try:
    db = Database(**db_conn_params)
    client = WebClient(token=os.environ['BILLBOARD_BOT_TOKEN'])

    ads = db.get_ad(current_timestamp=time.time())
    # [('id', 'user-id', 'text', 'img', 'alt', 'cta')]

    if not ads:
        print("nothin")
        sys.exit() # TODO: no ads avail prompts here

    ad_blocks = []
    for i, ad in enumerate(ads):
        ad_blocks.extend([{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ad[2]
            }
        }, {
            "type": "image",
            "image_url": ad[3],
            "alt_text": ad[4]
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{ad[5]} • Posted by <@{ad[1]}>"
            }
        }, {
            "type": "context",
             "elements": [{
                "text": f"Alt Text {i+1}: _{ad[4]}_" if len(ads) > 1 else f"Alt Text: _{ad[4]}_",
                "type": "mrkdwn"
            }]
        }
        ])
        if i != len(ads) - 1 and len(ads) > 1:
            ad_blocks.append({"type": "divider"})

    client.chat_postMessage(
        channel=CHANNEL_ID,
        text='A new billboard ad has dropped :D',
        blocks=ad_blocks,
    )
except Exception as e: # pylint: disable=broad-except
    print(f"Error: {e}")
    client.chat_postMessage(
        channel=CHANNEL_ID,
        text="The billboard has run into an error :c",
        blocks=[ # pylint: disable=line-too-long
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "An error has occured, please bug <@U07BU2HS17Z> to fix :pf:"
                }
            },
            {
                "type": "image",
                "image_url": 'https://hc-cdn.hel1.your-objectstorage.com/s/v3/9133edb480a2bbcdd9807bee07cae3af0d5da3df_error_slot.png',
                "alt_text": "Decorative image of a windows 95 style error dialog box"
            },
            {"type": "divider"},
            {
                "type": "context",
                "elements": [{
                    "text": "Alt Text: _Decorative image of a windows 95 style error dialog box_",
                    "type": "mrkdwn"
                }]
            }
        ]
    )
finally:
    db.pool.close()
