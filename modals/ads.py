def upload_ad(*, prefill = None) -> dict:
    """
    Displays the ad upload modal :D
    """
    if prefill: # ad_cta is optional so the logic gets weird ehhhh :c
        if prefill.get('ad-cta',{}).get('ad-cta',{}).get('value'):
            ad_cta = prefill['ad-cta']['ad-cta']['value']
        else:
            ad_cta = ''
    else:
        ad_cta = ''
    return { # pylint: disable=line-too-long
        "type": "modal",
        "callback_id": "submit-ad-form",
        "title": {
            "type": "plain_text",
            "text": "Billboard: Submit Ad",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Send it!",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Nevermind",
            "emoji": True
        },
        "blocks": [
            {
                "type": "image",
                "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/78a4c6c8b6b8b7f65a0cb72e84ca6ed3898e730f_ads_.png",
                "alt_text": "Text reading '#the-billboard, make an ad today!.' From Hack Club's press kit, assemble event."
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":tw_information_source: *Check the canvas in #the-billboard-dev to see how these sections get put together!*"
                }
            },
            {
                "type": "input",
                "block_id": "ad-text",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "ad-text",
                    "initial_value": prefill["ad-text"]["ad-text"]["value"] if prefill else '',
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Find IRL and virtual events, cool channels, projects, ships, and more! Written with love by the Newspaper Team :).",
                        "emoji": True
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Ad Top Text",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "ad-img",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "ad-img",
                    "initial_value": prefill["ad-img"]["ad-img"]["value"] if prefill else '',
                    "placeholder": {
                        "type": "plain_text",
                        "text": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/...",
                        "emoji": True
                    }
                },
                "hint": {
                    "type": "plain_text",
                    "text": ":tw_information_source: Tip: Make sure it's a valid link + high enough resolution!",
                    "emoji": True
                },
                "label": {
                    "type": "plain_text",
                    "text": "Ad Image URL (You can use #cdn!)",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "ad-alt",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "ad-alt",
                    "initial_value": prefill["ad-alt"]["ad-alt"]["value"] if prefill else '',
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Text reading '#happenings, join today!' The background is Counterspell Ottawa.",
                        "emoji": True
                    }
                },
                "hint": {
                    "type": "plain_text",
                    "text": ":tw_information_source: Tip: Would it be detailed enough if you could only read this text and not see the image? Be short, brief, and describe only what's important.",
                    "emoji": True
                },
                "label": {
                    "type": "plain_text",
                    "text": "Image Alt Text",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "optional": True,
                "block_id": "ad-cta",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "ad-cta",
                    "initial_value": ad_cta,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Join #happenings!",
                        "emoji": True
                    }
                },
                "hint": {
                    "type": "plain_text",
                    "text": ":tw_information_source: Tip: Include your main Call to Action, like a channel to join. All other details should be in the ad top text.",
                    "emoji": True
                },
                "label": {
                    "type": "plain_text",
                    "text": "Ad Bottom Text/Call to Action (CTA)",
                    "emoji": True
                }
            }
        ]
    }


def ad_exists_error(url_in_question: str, *, metadata = '') -> dict:
    """
    Ah sucks, the ad already exists lol
    """
    return { # pylint: disable=line-too-long
        "private_metadata": metadata,
        "title": {
            "type": "plain_text",
            "text": "The Billboard",
            "emoji": True
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Exit",
            "emoji": True
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Error: URL Already Exists",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Oops, so turns out `{url_in_question}` is already an ad? Yea we can't exactly do the same ad twice lol."
                }
            },
            {
			    "type": "actions",
	    		"elements": [
	    			{
	    				"type": "button",
	    				"style": "primary",
	    				"text": {
	    					"type": "plain_text",
	    					"text": "Try Again :D",
	    					"emoji": True
	    				},
	    				"action_id": "section-submit-ad-fix"
	    			}
	    		]
	    	}
        ]
    }


def ad_invalid_url_error(url_in_question: str, *, metadata = '') -> dict:
    """
    Informs the user their link sucks
    """
    return { # pylint: disable=line-too-long
        "private_metadata": metadata,
        "title": {
            "type": "plain_text",
            "text": "The Billboard",
            "emoji": True
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Exit",
            "emoji": True
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Error: Invalid URL",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Oops, so turns out `{url_in_question}` isn't a valid URL. Go check up on that link and fix it :D."
                }
            },
            {
			    "type": "actions",
	    		"elements": [
	    			{
	    				"type": "button",
	    				"style": "primary",
	    				"text": {
	    					"type": "plain_text",
	    					"text": "Try Again :D",
	    					"emoji": True
	    				},
	    				"action_id": "section-submit-ad-fix"
	    			}
	    		]
	    	}
        ]
    }


def ad_success():
    """
    Let's gooo! Ad success confirmation prompt
    """
    return { # pylint: disable=line-too-long
        "title": { 
            "type": "plain_text",
            "text": "The Billboard",
            "emoji": True
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Horray! (Exit)",
            "emoji": True
        },
        "blocks": [
            {
                "type": "image",
                "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/9331228d62a8562afc92fe4edd13085e09db798b_welcome_2__misc.png",
                "alt_text": "Background; People watch red fireworks fire in the distance at pitch-black night (credit: jamie street via unsplash). The text '#the-billboard. advertising made simple.' is overlayed."
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":partyparrot: Your ad has been uploaded!",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "What's next? *Your ad is now pending manual approval!* Go to the dashboard to view its approval status. You'll also get a message from this bot upon approval."
                }
            }
        ]
    }
