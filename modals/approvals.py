def confirmation_form(action_human_readable, action, ad, *, warning_prompt: bool = False) -> dict:
    """
    this action is irreversable ya know!
    """
    if warning_prompt:
        warning_prompt_block = [
            { # pylint: disable=line-too-long
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":siren-real: *DANGER(!!!): your version of the wizard data is outdated. exit and refresh to fix :D.*"
                }
            }
        ]
    else:
        warning_prompt_block = []
    return { # pylint: disable=line-too-long
        "type": "modal",
        "callback_id": "submit-wizard-action",
        "private_metadata": f"{ad[0]}={action}=PENDING",
        "title": {
            "type": "plain_text",
            "text": "Wizard Chaos",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_Are you sure you want to `{action_human_readable}` this ad?_"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: *This action is annoying to reverse! (Requires manual DB editing for now)*"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ad[2]
                }
            },
            {
                "type": "image",
                "image_url": ad[3],
                "alt_text": ad[4]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{ad[5]} • ID: *{ad[0]}* • Posted by <@{ad[1]}>"
                }
            },
            {
			    "type": "context",
			    "elements": [
			    	{
			    		"type": "mrkdwn",
			    		"text": f"Alt Text: _{ad[4]}_",
			    	}
			    ]
		    },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "optional": True,
                "block_id": "reasoning",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "reasoning",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Text reading '#happenings, join today!' The background is Counterspell Ottawa.",
                        "emoji": True
                    }
                },
                "hint": {
                    "type": "plain_text",
                    "text": ":tw_information_source: Tip: Just write whatever :3",
                    "emoji": True
                },
                "label": {
                    "type": "plain_text",
                    "text": f"Reasoning for {action_human_readable}ing this ad (why)",
                    "emoji": True
                }
            },
            *warning_prompt_block
        ]
    }


def wizard_warning(status, objectable) -> dict:
    """
    What have you done?
    Warning modal for the wizard
    """
    return { # pylint: disable=line-too-long
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Database Chaos Ahread",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"This ad's status is mismatched with your version. The ad is currently set to `{status.upper()}` (Objectable: {objectable}). Reload your wizard and try again if applicable. *You may not proceed* (the database might be screwed if you do)."
                }
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":stop:, think, and then proceed.",
                    "emoji": True
                }
            }
        ]
    }
