from slack_bolt.context.ack.async_ack import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from nephthys.utils.env import env


async def channel_left(ack: AsyncAck, event: dict, client: AsyncWebClient):
    await ack()
    user_id = event["user"]
    channel_id = event["channel"]

    if channel_id == env.slack_help_channel:
        return

    users = await client.usergroups_users_list(usergroup=env.slack_user_group)
    new_users = users.get("users", [])
    new_users.remove(user_id)
    await client.usergroups_users_update(
        usergroup=env.slack_user_group, users=new_users
    )

    await env.db.user.update(where={"id": user_id}, data={"helper": False})

    match channel_id:
        case env.slack_bts_channel:
            await client.conversations_kick(channel=channel_id, user=user_id)
        case env.slack_ticket_channel:
            await client.conversations_kick(channel=channel_id, user=user_id)
