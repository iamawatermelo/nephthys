from nephthys.data.transcript import Transcript
from nephthys.utils.delete_thread import add_thread_to_delete_queue
from nephthys.utils.env import env
from nephthys.utils.logging import send_heartbeat
from prisma.enums import TicketStatus


async def resolve(ts: str, resolver: str, client):
    ticket = await env.db.ticket.find_first(
        where={"msgTs": ts, "NOT": [{"status": TicketStatus.CLOSED}]}
    )
    if not ticket:
        return

    tkt = await env.db.ticket.update(
        where={"msgTs": ts},
        data={"status": TicketStatus.CLOSED, "closedBy": {"connect": {"id": resolver}}},
    )
    if not tkt:
        await send_heartbeat(
            f"Failed to resolve ticket with ts {ts} by {resolver}. Ticket not found.",
            messages=[f"Ticket TS: {ts}", f"Resolver ID: {resolver}"],
        )
        return

    await client.chat_postMessage(
        channel=env.slack_help_channel,
        text=Transcript.ticket_resolve,
        thread_ts=ts,
    )

    await client.reactions_add(
        channel=env.slack_help_channel,
        name="white_check_mark",
        timestamp=ts,
    )

    await client.reactions_remove(
        channel=env.slack_help_channel,
        name="thinking_face",
        timestamp=ts,
    )

    await add_thread_to_delete_queue(
        channel_id=env.slack_ticket_channel, thread_ts=tkt.ticketTs
    )
