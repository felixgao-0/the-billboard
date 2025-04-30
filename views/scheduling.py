from datetime import datetime

def generate_schedule(client, user_id, weeks_avail):
    """
    Scheduling! :yay:
    """
    days_block = []
    for day in weeks_avail:
        days_block.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{day['day'].strftime('%b %d, %Y')}*"
            }
        })
        slots_block = []
        for i, slot in enumerate(day['slots']):
            slots_block.append({
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": f"{slot[0].strftime('%I:%M %p')} - {slot[1].strftime('%I:%M %p')}",
					"emoji": True
				},
				"value": f"{datetime.combine(day['day'], slot[0]).timestamp()}", # Uhhhhh will this work?
				"action_id": f"schedule-time-select-{i}"
				})
        days_block.append({
			"type": "actions",
			"elements": slots_block
		})
        # "value": day.strftime("%Y-%m-%d")

    client.views_publish(
        user_id=user_id,
        view={  # pylint: disable=line-too-long
            "type": "home", 
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Scheduling Wizard",
                        "emoji": True
                    }
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": "Don't we love ads at 3am? /s",
                        "emoji": True
                    },
                    "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/a6d2455d21e47b2df5cbe09ed06b9682c01c9d5f_3am_ads.png",
                    "alt_text": "A small table-top clock sitting on an open cabinet. Overlayed text reads, 'the billboard, yes 1 ad for 3am please' as sarcasm."
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":tw_information_source: Tip: Time slots are as follows: 12am-7:59am, 8am to 3:59pm, 4pm to 11:59pm. Options which do not appear below are *taken.* You may book between tomorrow to 14 days inclusive after today."
                    }
                },
                *days_block
            ]
        }
    )
