def generate_approval_wizard(client, user_id, ads) -> dict:
    """
    Approve those ads!
    """
    ad_blocks = []
    print(ads)
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
                "text": f"{ad[5]} • ID: *{ad[0]}* • Posted by <@{ad[1]}>"
            }
        }, {
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": f"Alt Text {i+1}: _{ad[4]}_" if len(ads) > 1 else f"Alt Text: _{ad[4]}_",
				}
			]
		},{
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":check-check: Approve",
                        "emoji": True
                    },
                    "action_id": "ad-approve",
                    "value": f"{ad[0]}"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":no_entry: Reject",
                        "emoji": True
                    },
                    "action_id": "ad-reject",
                    "value": f"{ad[0]}"
                },
                        {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":stop: Reject (Unappealable)",
                        "emoji": True
                    },
                    "action_id": "ad-reject-final",
                    "value": f"{ad[0]}"
                }
            ]
        }])
        if i != len(ads) - 1 and len(ads) > 1:
            ad_blocks.append({"type": "divider"})
    if not ads:
        ad_blocks = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*No ads pending approval!*"
            }
        }]
    client.views_publish(
        user_id=user_id,
        view={ # pylint: disable=line-too-long
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Approval Wizard",
                        "emoji": True
                    }
                },
                {
                    "type": "image",
                    "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/609407fb07897033bc2188a237806e71f8eb0fcb_admin__ad_approval.png",
                    "alt_text": "A partial view of a laptop half closed from the top, the screen is glowing blue. Text overlayed reads, '#the-billboard, approve those ads!' with an admin symbol on the top-right."
                },
                {
                    "type": "divider"
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": ":hq: Home",
                                "emoji": True
                            },
                            "action_id": "dashboard"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": ":safari-loading: Reload",
                                "emoji": True
                            },
                            "action_id": "section-approval-wizard"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                *ad_blocks,
            ]
        }
    )
