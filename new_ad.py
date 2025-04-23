"""
Rotates a new ad in at set times
"""
import os
import sys
from slack_sdk import WebClient
#from slack_sdk.errors import SlackApiError

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

CHANNEL_ID = "C08NU78MR4G"  # the-billboard-DEV

# a giant try-except to display error blocks
try:
    db = Database(**db_conn_params)
    client = WebClient(token=os.environ['BILLBOARD_BOT_TOKEN'])

    ads = db.get_ad(current_timestamp=505)  # FIXME: Change to proper timestamp with time.time()
    # [(1, 'user-id', 'text', 'img', 'alt', 'cta')]

    if not ads:
        print("nothin")
        sys.exit() # TODO: no ads avail prompts here

    ad_blocks = []
    for i, ad in enumerate(ads): # TODO PLS FIXME: use list.extend(), move alt text pos
        ad_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ad[2]
            }
        })

        ad_blocks.append({
            "type": "image",
            "image_url": ad[3],
            "alt_text": ad[4]
        })
        ad_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{ad[5]} • Posted by <@{ad[1]}>"
            }
        })
        if i != len(ads) - 1 and len(ads) > 1:
            ad_blocks.append({"type": "divider"})

        ad_blocks.append({
            "type": "context",
             "elements": {
                "text": f"Alt Text {i+1}: _{ad[4]}_" if len(ads) > 1 else f"Alt Text: _{ad[4]}_",
                "type": "mrkdwn"
            }
        })

    client.chat_postMessage(
        channel=CHANNEL_ID,
        text='Insert text here later trust', # FIXME: Add text here
        blocks=ad_blocks,
    )
except Exception as e: # pylint: disable=broad-except
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

"""
try:
    response = client.conversations_history(channel=channel_id)
    messages = response["messages"]

    for msg in messages:
        ts = msg["ts"]
        client.chat_delete(channel=channel_id, ts=ts)
        time.sleep(0.5)  # rate limiting

    print("Channel cleared.")
except SlackApiError as e:
    print(f"Error: {e.response['error']}")
"""
