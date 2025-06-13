from prisma.models import User


def get_buttons(user: User, current: str = "dashboard"):
    buttons = []

    buttons.append(
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Dashboard", "emoji": True},
            "action_id": "dashboard",
            **({"style": "primary"} if current != "dashboard" else {}),
        }
    )
    if user.admin:
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Tags", "emoji": True},
                "action_id": "tags",
                **({"style": "primary"} if current != "tags" else {}),
            }
        )

    buttons.append(
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "My Stats", "emoji": True},
            "action_id": "my-stats",
            **({"style": "primary"} if current != "my-stats" else {}),
        }
    )

    blocks = {"type": "actions", "elements": buttons}
    return blocks
