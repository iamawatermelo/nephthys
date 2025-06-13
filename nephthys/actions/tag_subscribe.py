from typing import Any
from typing import Dict

from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from nephthys.events.app_home_opened import open_app_home
from nephthys.utils.env import env
from nephthys.utils.logging import send_heartbeat


async def tag_subscribe_callback(
    ack: AsyncAck, body: Dict[str, Any], client: AsyncWebClient
):
    """
    Callback for the tag subscribe button
    """
    await ack()
    user_id = body["user"]["id"]

    user = await env.db.user.find_unique(where={"id": user_id})
    if not user:
        await send_heartbeat(
            f"Attempted to subscribe to tag by unknown user <@{user_id}>"
        )
        return

    tag_id, tag_name = body["actions"][0]["value"].split(";")
    # check if user is subcribed
    if await env.db.usertagsubscription.find_first(
        where={"userId": user_id, "tagId": tag_id}
    ):
        await env.db.usertagsubscription.delete(
            where={"userId_tagId": {"tagId": tag_id, "userId": user_id}}
        )
    else:
        await env.db.usertagsubscription.create(
            data={
                "user": {"connect": {"id": user_id}},
                "tag": {"connect": {"id": tag_id}},
            }
        )

    await open_app_home("tags", client, user_id)
