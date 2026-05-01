"""
Demo: Hermes Agent with Universal Formatter

This shows how an agent's output gets formatted per platform.
Run: python demo_agent.py
"""

from hermes_formatter import format


def simulate_agent_run(task: str) -> dict:
    """
    Simulate an agent producing output for different tasks.
    In real life, this would be your Hermes agent's response.
    """
    templates = {
        "scrape": """✅ **Scraping Complete!**

I've successfully scraped **5 websites**:
• https://news.ycombinator.com — 27 articles
• https://reddit.com/r/ai — 42 posts
• https://example.com — 3 updates

**Stats:**
• Avg latency: 2.3s
• Total data: 1.2MB
• Errors: 0

See the full report: https://example.com/reports/daily-2026-01-15

:rocket: Ready for next task!""",

        "error": """❌ **Task Failed: Login Error**

Failed to authenticate with the API.

**Error details:**
- Tool: `login_to_system`
- Reason: Invalid credentials
- Code: `401 Unauthorized`
- Retry count: 3

**Suggestion:** Check API key in environment variable `SYSTEM_API_KEY`.

⚠️ *Will retry in 5 minutes*""",

        "monitor": """📊 **Hourly System Health Check**

**Status:** ✅ All systems operational

| Service | Status | Latency |
|---------|--------|---------|
| Web API | 🟢 OK | 45ms |
| Database | 🟢 OK | 12ms |
| Cache | 🟢 OK | 3ms |

**Uptime:** 99.97% this week

*Report time: 2026-01-15 14:00:00 UTC*""",

        "summary": """**Daily Briefing — January 15, 2026**

## What happened today

1. **System update** completed successfully
2. **5 new tickets** in support queue
3. **Revenue milestone** reached: $10K MRR :tada:

### Action items for tomorrow
- [ ] Review PR #234
- [ ] Schedule team sync
- [ ] Deploy hotfix to production

— Hermes Agent"""
    }

    return {"output": templates.get(task, templates["summary"])}


def main():
    print("=" * 60)
    print("HERMES UNIVERSAL FORMATTER — DEMO")
    print("=" * 60)
    print()

    # Simulate a few agent outputs
    tasks = ["scrape", "error", "monitor", "summary"]

    for task in tasks:
        result = simulate_agent_run(task)
        raw_output = result["output"]

        print(f"\n{'─' * 60}")
        print(f"TASK: {task.upper()}")
        print(f"{'─' * 60}")
        print("\n─── RAW (what agent produces) ───")
        print(raw_output)

        print("\n─── TELEGRAM ───")
        print(format(raw_output, platform="telegram"))

        print("\n─── DISCORD ───")
        print(format(raw_output, platform="discord"))

        print("\n─── SLACK ───")
        print(format(raw_output, platform="slack"))

        print("\n─── CLI (colored) ───")
        print(format(raw_output, platform="cli"))

        print("\n─── PLAIN TEXT ───")
        print(format(raw_output, platform="generic", strip_markdown=True))

        print("\n─── EMAIL ───")
        email = format(raw_output, platform="email")
        print("HTML (first 300 chars):", email["html"][:300])
        print("Plain text:", email["text"][:200])

        print("\n" + "=" * 60)


def quick_demo():
    """One-liner demo for README."""
    agent_output = "✅ **Task done!**\n• 5 files processed\n• See: https://example.com/report"

    platforms = ["telegram", "discord", "slack", "cli", "generic"]

    print("Agent output → formatted per platform:\n")
    for p in platforms:
        formatted = format(agent_output, platform=p)
        print(f"[{p.upper()}]")
        print(formatted[:150] + ("..." if len(formatted) > 150 else ""))
        print()


if __name__ == "__main__":
    quick_demo()
    print("\n" + "=" * 60 + "\n")
    main()
