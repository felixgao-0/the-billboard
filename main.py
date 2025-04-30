import datetime
import json
import os
import re
import time

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient # make use of the admin token

import validators
import requests # image validation
from dotenv import load_dotenv

import database
import views
import modals

load_dotenv()

app = App(token=os.environ["BILLBOARD_BOT_TOKEN"])
user_client = WebClient(token=os.environ['BILLBOARD_USERBOT_TOKEN'])
db = database.Database(**{
        "dbname": "felixgao_the_billboard",
        "user": "felixgao",
        "password": os.environ['DB_PASSWORD'],
        "host": "hackclub.app",
        "port": 5432
    })

ADMINS = os.environ.get("ADMINS").split(",") if os.environ.get("ADMINS") else []
AUTHORIZED = os.environ.get("AUTHORIZED").split(",") if os.environ.get("AUTHORIZED") else []
DAY_BLOCKS = [
    (datetime.time(0,0),datetime.time(7,59,59)),   # 12am - 7:19am
    (datetime.time(8,0),datetime.time(15,59,59)),  # 8am - 3:59pm
    (datetime.time(16,0),datetime.time(23,59,59)), # 4pm - 11:59pm
]


@app.event("message")
def handle_message_events(body, logger):
    """
    Create a cheap temu firehose and make #the-billboard read-only
    """
    event = body.get("event", {})
    user = event.get("user")

    if not event.get("channel") or not event.get("ts") or not user:
        return # shouldn't happen but just in case

    if event.get("channel") != "C08MRG6NK1V":
        return # not the-billboard

    if user in (ADMINS + AUTHORIZED) or user == os.environ.get("BOT_ID"):
        return

    user_client.chat_delete(channel=event['channel'], ts=event['ts'])
    app.client.chat_postEphemeral(
            channel=event["channel"],
            user=user,
            thread_ts=event.get("thread_ts", event["ts"]),
            text="""
:stop: *You can't talk here :no-no:* // This is a read-only channel (sorry)

Want to talk about the bot, the ads, or run one? <#C08NU78MR4G>
Felix has a personal channel too :D <#C07H1JQP9DJ>

Enjoy the ads tho :bangbang:"""
        )



@app.action("dashboard")
def render_home_tab(ack, client, user_id, logger):
    """
    Renders the home tab
    """
    ack()
    if os.environ.get("DEV") == "true" and (user_id not in ADMINS and user_id not in AUTHORIZED):
        views.generate_unauthorized(client, user_id)
        logger.warning(f"{user_id} is unauthorized :c")
        return

    views.generate_dashboard(client, user_id)


@app.event("app_home_opened")
def home_tab_opened(event, client, logger):
    """
    The base home tab
    """
    user_id = event["user"]
    logger.info(f"{user_id} opened za home tab")

    # pass in a lambda cause ack doesn't apply and im too lazy to make a seperate func lol
    render_home_tab(lambda: None, client, user_id, logger)


@app.action("section-templates")
def show_templates(ack, client, body, logger):
    """
    Displays templates for the user's convience :D
    """
    ack()
    logger.info(body)
    views.generate_boards(client, body["user"]["id"])


@app.action("section-view-ads")
def view_ads_modal(ack, client, body, logger):
    """
    View all the ads a user has submitted previously
    """
    ack()
    views.generate_loading(client, body["user"]["id"])

    ads = db.get_ad(user_id=body["user"]["id"])
    views.generate_view_ads(client, body["user"]["id"], ads)


@app.action("section-submit-ad")
def submit_ad_modal(ack, client, body, logger):
    """
    Opens za submit ad modal when the user clicks the button
    """
    ack()
    logger.info(body)
    client.views_open(trigger_id=body["trigger_id"], view=modals.upload_ad())


@app.action("section-submit-ad-fix")
def submit_ad_modal_fix(ack, client, body, logger):
    """
    Fix your mistakes; submit ad modal but editing
    """
    ack()
    client.views_update(
        view_id=body["container"]['view_id'],
        view=modals.upload_ad(prefill=json.loads(body['view']['private_metadata']))
    )


@app.view("submit-ad-form")
def form_ad_submitted(ack, client, body, view, logger):
    """
    Handles the ad submission form"""
    ack()
    form = view["state"]["values"]
    # preserve the original url for error message reasons
    # TODO: Strip the leading / + whitespace from the url
    formatted_url, url = (form["ad-img"]["ad-img"]["value"],)*2 # *2 is goofy lol
    if not (url.startswith("https://") or url.startswith("http://")):
        formatted_url = "https://" + url # attempt to fix missing protocol via duct tape

    valid_url = validators.url(formatted_url, consider_tld=True, may_have_port=False)
    trigger = body["trigger_id"]
    form_data = json.dumps(form)

    if not valid_url:
        client.views_open(trigger_id=trigger, view=modals.ad_gen_error(
            'Invalid URL Syntax', f"The URL (`{url}`) syntax is incorrect looking :c. Please check it and try again.",
            metadata=form_data))
        return

    try:
        response = requests.head(formatted_url, allow_redirects=True, timeout=1)
    except requests.RequestException:
        client.views_open(trigger_id=trigger, view=modals.ad_gen_error(
            'Invalid URL', f"Something with this URL (`{url}`) is broken can couldn't withstand a test HTTP request. Please check it and try again.",
            metadata=form_data))
        return

    if not response.headers.get('Content-Type', '').startswith('image/'):
        client.views_open(trigger_id=trigger, view=modals.ad_gen_error(
            'Not an Image', f"This URL (`{url}`) doesn't point to an image. Please gib image :D.",
            metadata=form_data))
        return

    try:
        db.add_ad(
            slack_id=body["user"]["id"],
            ad_text=form["ad-text"]["ad-text"]["value"],
            ad_img=formatted_url,
            ad_alt=form["ad-alt"]["ad-alt"]["value"],
            ad_cta=form["ad-cta"]["ad-cta"]["value"]
        )
    except ValueError:
        client.views_open(trigger_id=trigger, view=modals.ad_gen_error("Image Already Exists", f"This URL (`{url}`) alrady exists in a DB that hates twins :c. Go make your ad unique!", metadata=form_data))
        return
    client.views_open(trigger_id=trigger, view=modals.ad_success())


@app.action(re.compile(r"schedule-ad-\d"))
def schedule_event(ack, client, body, logger):
    """
    Get your ad schedule for 3am!
    """
    ack()
    value = body["actions"][0].get("selected_option", {}).get("value")
    
    start = time.time() # FIXME: timer, DELETE BEFORE PROD PLS
    views.generate_loading(client, body["user"]["id"])

    # get next the 2 weeks starting tmr
    start_next_week = datetime.date.today() + datetime.timedelta(days=1)
    week_list = [start_next_week + datetime.timedelta(days=i) for i in range(14)]

    first = datetime.datetime.combine(week_list[0], datetime.time.min)
    last = datetime.datetime.combine(week_list[-1], datetime.time.max)
    db_schedule = db.get_schedule(first.timestamp(), last.timestamp()) # get entire week range
    taken_time_ranges = []

    for schedule in db_schedule:
        taken_time_ranges.append((schedule[2], schedule[3]))

    schedule = []
    for day in week_list: # for everything in the next 2 weeks
        avail_slots = []
        for slot in DAY_BLOCKS:
            start = datetime.datetime.combine(day, slot[0])
            if any(start <= start.timestamp() < end for start, end in taken_time_ranges):
                continue # if the start time is taken, skip this slot

            avail_slots.append({ # add slot to list
                'start': start,
                'end': datetime.datetime.combine(day, slot[1])
            })

    views.generate_schedule(client, body["user"]["id"], schedule)
    end = time.time()
    print(f"Schedule took {end - start} seconds")


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["BILLBOARD_APP_TOKEN"])
    handler.start()
