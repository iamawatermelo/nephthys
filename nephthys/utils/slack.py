from typing import Any
from typing import Dict

from slack_bolt.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from nephthys.actions.resolve import resolve
from nephthys.events.message import on_message
from nephthys.utils.env import env

app = AsyncApp(token=env.slack_bot_token, signing_secret=env.slack_signing_secret)


@app.event("message")
async def handle_message(event: Dict[str, Any], client: AsyncWebClient):
    if event["channel"] == env.slack_help_channel:
        await on_message(event, client)


@app.action("mark_resolved")
async def handle_mark_resolved_button(
    ack: AsyncAck, body: Dict[str, Any], client: AsyncWebClient
):
    await ack()
    value = body["actions"][0]["value"]
    resolver = body["user"]["id"]
    await resolve(value, resolver, client)
