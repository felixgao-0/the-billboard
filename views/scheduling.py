def generate_schedule(client, user_id, weeks_avail):
    """
    Scheduling! :yay:
    """
    days_block = []
    for day in weeks_avail:
        days_block.append({
            "text": {
                "type": "plain_text",
                    "text": day.strftime("%b %d, %Y"),
                    "emoji": True
                },
                "value": day.strftime("%Y-%m-%d")
            }
        )
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
                    "type": "input",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Feb 30, 2025",
                            "emoji": True
                        },
                        "options": days_block,
                        "action_id": "static_select-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Select a Day",
                        "emoji": True
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "Why not a date selector? Slack won't let me clamp it to certain dates ._.",
                            "emoji": True
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "style": "primary",
                            "text": {
                                "type": "plain_text",
                                "text": ":mag: Search",
                                "emoji": True
                            },
                            "action_id": "section-schedule-date-search"
                        }
                    ]
                }
            ]
        }
    )