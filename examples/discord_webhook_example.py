"""
Example: Discord Webhook using Hermes Formatter

Posts formatted agent messages to a Discord channel via webhook.

Prerequisites:
    pip install discord-webhook

Set environment variable DISCORD_WEBHOOK_URL.
"""

import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from hermes_formatter import format


def send_agent_report(task: str, raw_output: str, webhook_url: str = None):
    """
    Send agent output to Discord channel with nice embed.
    """
    webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Error: Set DISCORD_WEBHOOK_URL environment variable")
        return

    # Format for Discord
    formatted = format(raw_output, platform="discord")

    # Truncate if needed (Discord limit 2000)
    if len(formatted) > 1900:
        formatted = formatted[:1897] + "..."

    webhook = DiscordWebhook(url=webhook_url, content=formatted)

    # Optional: add embed with metadata
    embed = DiscordEmbed(
        title=f"Agent Task: {task}",
        color="00ff00" if "✅" in raw_output else "ff0000"
    )
    embed.add_embed_field(name="Status", value="Completed" if "✅" in raw_output else "Failed")
    embed.set_timestamp()
    webhook.add_embed(embed)

    response = webhook.execute()
    print(f"Sent to Discord: {response.status_code}")


def main():
    # Example agent output
    raw = """✅ **Scraping Complete!**

I've finished scraping product pages.

**Results:**
• 143 products found
• 12 price changes detected
• 3 new items in stock

Next: Price analysis phase 🚀"""

    send_agent_report("price_monitor", raw)


if __name__ == "__main__":
    main()
