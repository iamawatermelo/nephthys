from nephthys.utils.env import env
from nephthys.views.home.components.buttons import get_buttons
from prisma.enums import TicketStatus
from prisma.models import User


async def get_helper_view(user: User):
    tickets = await env.db.ticket.find_many() or []

    organised_tkts = {}
    for ticket in tickets:
        status = ticket.status
        if status not in organised_tkts:
            organised_tkts[status] = []
        organised_tkts[status].append(ticket)

    formatted_msg = f"""
    *Requests*
    {len(tickets)} requests found
    {len(organised_tkts.get(TicketStatus.OPEN, []))} open
    {len(organised_tkts.get(TicketStatus.IN_PROGRESS, []))} in progress  ({len([ticket for ticket in tickets if ticket.status == TicketStatus.IN_PROGRESS and ticket.assignedToId == user.id])} assigned to you)
    {len(organised_tkts.get(TicketStatus.CLOSED, []))} closed  ({len([ticket for ticket in tickets if ticket.status == TicketStatus.CLOSED and ticket.closedById == user.id])} closed by you)
    """

    btns = get_buttons(user, "dashboard")

    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":rac_cute: helper heidi",
                    "emoji": True,
                },
            },
            btns,
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": formatted_msg}},
        ],
    }
