from typing import Any
from typing import Dict

from slack_sdk.web.async_client import AsyncWebClient

from nephthys.data.transcript import Transcript
from nephthys.utils.env import env

ALLOWED_SUBTYPES = ["file_share", "me_message"]


async def on_message(event: Dict[str, Any], client: AsyncWebClient):
    """
    Handle incoming messages in Slack.
    """
    print("Received message event:", event)
    if "subtype" in event and event["subtype"] not in ALLOWED_SUBTYPES:
        return

    if event.get("thread_ts"):
        return

    user = event.get("user", "unknown")
    text = event.get("text", "")

    thread_url = f"https://hackclub.slack.com/archives/{env.slack_help_channel}/p{event['ts'].replace('.', '')}"

    db_user = await env.db.user.find_first(where={"id": user})
    if db_user:
        past_tickets = await env.db.ticket.count(where={"openedById": user})
    else:
        past_tickets = 0
        db_user = await env.db.user.upsert(
            where={
                "id": user,
            },
            data={"create": {"id": user}, "update": {"id": user}},
        )

    user_info = await client.users_info(user=user)
    profile_pic = None
    display_name = "Explorer"
    if user_info:
        profile_pic = user_info["user"]["profile"].get("image_512", "")
        display_name = (
            user_info["user"]["profile"]["display_name"] or user["user"]["real_name"]
        )

    ticket = await client.chat_postMessage(
        channel=env.slack_ticket_channel,
        text=f"New message from <@{user}>: {text}",
        blocks=[
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Submitted by <@{user}>. They have {past_tickets} past tickets. <{thread_url}|View thread>.",
                    }
                ],
            }
        ],
        username=display_name or None,
        icon_url=profile_pic or None,
        unfurl_links=True,
        unfurl_media=True,
    )

    await env.db.ticket.create(
        {
            "title": f"New ticket from {user}",
            "description": text,
            "msgTs": event["ts"],
            "ticketTs": ticket["ts"],
            "openedBy": {"connect": {"id": user}},
        },
    )

    text = (
        Transcript.first_ticket_create.replace("(user)", display_name)
        if past_tickets == 0
        else Transcript.ticket_create.replace("(user)", display_name)
    )
    await client.chat_postMessage(
        channel=event["channel"],
        text=text,
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "i get it now"},
                        "style": "primary",
                        "action_id": "mark_resolved",
                        "value": f"{event['ts']}",
                    }
                ],
            },
        ],
        thread_ts=event.get("ts"),
        unfurl_links=True,
        unfurl_media=True,
    )

    await client.reactions_add(
        channel=event["channel"], name="thinking_face", timestamp=event["ts"]
    )
