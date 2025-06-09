from nephthys.utils.env import env


class Transcript:
    FAQ_LINK = "https://hackclub.slack.com/docs/T0266FRGM/F090MQF0H2Q"
    first_ticket_create = f"""
oh, hey (user) it looks like this is your first time here, welcome! someone should be along to help you soon but in the mean time i suggest you read the faq <{FAQ_LINK}|here>, it answers a lot of common questions. 
if your question has been answered, please hit the button below to mark it as resolved
    """

    ticket_create = f"""
someone should be along to help you soon but in the mean time i suggest you read the faq <{FAQ_LINK}|here> to make sure your question hasn't already been answered. if it has been, please hit the button below to mark it as resolved :D
    """

    ticket_resolve = f"""
oh, oh! it looks like this post has been marked as resolved by (user)! if you have any more questions, please make a new post in <#{env.slack_help_channel}> and someone'll be happy to help you out! not me though, i'm just a silly racoon ^-^
    """
