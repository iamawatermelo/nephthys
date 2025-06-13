from nephthys.data.transcript import Transcript


def get_unknown_user_view(name: str):
    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": Transcript.home_unknown_user_title.format(name=name),
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": Transcript.home_unknown_user_text},
            },
        ],
    }
