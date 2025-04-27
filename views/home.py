def generate_dashboard(client, user_id):
    """
    Dashboard view function.
    """
    client.views_publish(
        user_id=user_id,
        view={ # pylint: disable=line-too-long
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Welcome (back), <@{user_id}>!",
                        "emoji": True
                    }
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": "Community advertising, made simple :) // Background: Hack Club Press Kit, Horizon // Board B",
                        "emoji": True
                    },
                    "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/60d3e5be1339f571b38f7bf1a39e28e54ba0563d_welcome_to_the_billboard.png",
                    "alt_text": "Text reading '#the-billboard, community ads made simple.' This is sized board B."
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
                                "text": "View Template Boards",
                                "emoji": True
                            },
                            "action_id": "section-templates"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Your Ads + Scheduling",
                                "emoji": True
                            },
                            "action_id": "section-view-ads"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Submit an Ad",
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
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "The Billboard is a community project by Felix Gao. Feedback can be DM'ed to me or sent to #the-billboard-dev (ping me!)."
                        }
                    ]
                }
            ]
        }
    )


def generate_unauthorized(client, user_id):
    """
    Unauthorized :c
    """
    client.views_publish(
        user_id=user_id,
        view={ # pylint: disable=line-too-long
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":siren-real: Unauthorized // Work in Progress",
                        "emoji": True
                    }
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": "Community advertising, made simple :) // Background: Hack Club Press Kit, Horizon // Board B",
                        "emoji": True
                    },
                    "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/60d3e5be1339f571b38f7bf1a39e28e54ba0563d_welcome_to_the_billboard.png",
                    "alt_text": "Text reading '#the-billboard, community ads made simple.' This is sized board B."
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*This project is a work-in-progress (WIP)*! Check back later for something epic :leeks: // #the-billboard & #the-billboard-dev"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "The Billboard is a community project by Felix Gao. Feedback can be DM'ed to be or sent to #the-billboard-dev (ping me!)."
                        }
                    ]
                }
            ]
        }
    )
