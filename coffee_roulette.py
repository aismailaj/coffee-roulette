import os
import random
from slack_sdk import WebClient

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
channel_id = os.environ["SLACK_CHANNEL_ID"]

# Get all members in the channel
result = client.conversations_members(channel=channel_id)
members = result["members"]

# Remove bots from the list
real_members = []
for member_id in members:
    info = client.users_info(user=member_id)
    if not info["user"]["is_bot"]:
        real_members.append(member_id)

# Shuffle and pair them up
random.shuffle(real_members)
pairs = [(real_members[i], real_members[i+1]) for i in range(0, len(real_members) - 1, 2)]

# If odd number of people, add the last person to the final pair
if len(real_members) % 2 != 0:
    pairs[-1] = pairs[-1] + (real_members[-1],)

# Post a message for each pair
for pair in pairs:
    names = [f"<@{uid}>" for uid in pair]
    paired = " and ".join(names)
    client.chat_postMessage(
        channel=channel_id,
        text=f"☕ Time for coffee! Pairing up {paired} this week — reach out and find a time!"
    )
