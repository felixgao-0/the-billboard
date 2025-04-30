def generate_view_ads(client, user_id, ads) -> dict:
    """
    Displays the ad upload modal :D
    """
    ad_blocks = []
    if not ads:
        ad_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You don't have any ads yet! Click the button above to create one."
            }
        })

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
                "text": f"{ad[5]} • *STATUS: {ad[6]}* • ID: *{ad[0]}*"
            }
        }, {
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": f"Alt Text {i+1}: _{ad[4]}_" if len(ads) > 1 else f"Alt Text: _{ad[4]}_",
				}
			]
		}])
        if ad[6] == "APPROVED":
            ad_blocks.append({
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":calendar: Schedule Ad",
						"emoji": True
					},
                    "value": f"{ad[0]}",
					"action_id": f"schedule-ad-{i}",
				}
			]
		})
        if i != len(ads) - 1 and len(ads) > 1:
            ad_blocks.append({"type": "divider"})

    client.views_publish(
        user_id=user_id,
        view={ # pylint: disable=line-too-long
        "type": "home",
        "blocks": [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":hq: Dashboard",
                            "emoji": True
                        },
                        "action_id": "dashboard"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Create an Ad",
                            "emoji": True
                        },
                        "action_id": "section-submit-ad"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Your Ads",
                    "emoji": True
                }
            },
            *ad_blocks,
        ]
    })
