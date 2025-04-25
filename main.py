import datetime
import json
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import validators
import requests # image validation
from dotenv import load_dotenv

import database
import views
import modals

load_dotenv()

app = App(token=os.environ["BILLBOARD_BOT_TOKEN"])
db = database.Database(**{
        "dbname": "felixgao_the_billboard",
        "user": "felixgao",
        "password": os.environ['DB_PASSWORD'],
        "host": "hackclub.app",
        "port": 5432
    })

ADMINS = ['U07BU2HS17Z']
AUTHORIZED = []


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
    logger.info(body)
    ads = db.get_ad(user_id=body["user"]["id"])
    views.generate_view_ads(client, body["user"]["id"], ads) # FIXME: lol


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
    formatted_url, url = (form["ad-img"]["ad-img"]["value"],)*2 # *2 is goofy lol
    if not (url.startswith("https://") or url.startswith("http://")):
        formatted_url = "https://" + url # attempt to fix missing protocol via duct tape

    valid_url = validators.url(formatted_url, consider_tld=True, may_have_port=False)
    trigger = body["trigger_id"]
    form_data = json.dumps(form)

    try:
        response = requests.head(url, allow_redirects=True, timeout=1)
    except requests.RequestException:
        client.views_open(trigger_id=trigger, view=modals.ad_invalid_url_error(url, metadata=form_data))
        return # TODO: Add a more specfic error message

    if not valid_url or not response.headers.get('Content-Type', '').startswith('image/'):
        client.views_open(trigger_id=trigger, view=modals.ad_invalid_url_error(url, metadata=form_data))
        return # TODO: seperate between bad url and no image found

    try:
        db.add_ad(
            slack_id=body["user"]["id"],
            ad_text=form["ad-text"]["ad-text"]["value"],
            ad_img=formatted_url,
            ad_alt=form["ad-alt"]["ad-alt"]["value"],
            ad_cta=form["ad-cta"]["ad-cta"]["value"]
        )
    except ValueError:
        client.views_open(trigger_id=trigger, view=modals.ad_exists_error(url, metadata=form_data))
        return
    client.views_open(trigger_id=trigger, view=modals.ad_success())


@app.action("section-schedule")
def view_schedule_base(ack, client, body, logger):
    ack()

    # get next the 2 weeks starting tmr
    start_next_week = datetime.date.today() + datetime.timedelta(days=1)
    week_list = [start_next_week + datetime.timedelta(days=i) for i in range(14)]

    first = datetime.datetime.combine(week_list[0], datetime.time.min)
    last = datetime.datetime.combine(week_list[-1], datetime.time.max)
    schedule = db.get_schedule(first.timestamp(), last.timestamp())
    print(schedule)
    views.generate_schedule(client, body["user"]["id"], week_list)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["BILLBOARD_APP_TOKEN"])
    handler.start()
