def generate_loading(client, user_id):
    """
    For wen the code is so slow you need a loading screen
    """
    client.views_publish(
        user_id=user_id,
        view={  # pylint: disable=line-too-longTrue,
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":safari-loading: Loading... :safari-loading: ",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Yes the code is slow enough that one is needed ._.",
                        "emoji": True
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "Stuck here? Click below to escape back to the home page and/or report this bug in #the-billboard-dev",
                            "emoji": True
                        }
                    ]
                },
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
                }
            ]
        }
    )
