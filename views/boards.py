def generate_boards(client, user_id):
    """
    Displays the boards :D
    """
    client.views_publish(
        user_id=user_id,
        view={  # pylint: disable=line-too-long
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
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "You can use different sizes (within reason), but I've found these to work well :D. All the stuff is decorative to make it look nice fyi, just focus on the size :pf:.",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Ordered by most recommended, so A is recommended over B over C.",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":tw_information_source: *Tip:* I designed all the banners for this bot, and these sample board, <https://www.figma.com/design/wS7kudyrIxyY57NYQ2sRPb/Untitled?node-id=0-1&t=WMfmRqgx1dnJP6lQ-1|in this Figma>!"
                    }
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": "Sample Board A, 800x400 px",
                        "emoji": True
                    },
                    "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/3886a9736ed367e58799fcb54543f4f357fc9947_template_a.png",
                    "alt_text": "Sample Board A, 800x400 px"
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": "Sample Board B, 800x200 px",
                        "emoji": True
                    },
                    "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/24e3f9658990e1496ccd3e6a26d6693cce1aa1da_template_b.png",
                    "alt_text": "Sample Board B, 800x200 px"
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": "Sample Board C, 800x800 px // Are you sure you want a board THIS big?",
                        "emoji": True
                    },
                    "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/b24e134952601c129aa9cfa68e4209798c836844_template_c.png",
                    "alt_text": "Sample Board C, 800x800 px. Text reading, 'Are you sure you want a board THIS big?'"
                }
            ]
        }
    )
