# stop-trying 别试了

A Telegram bot that eases anxiety through Daoist philosophy.

It never tells you to fix yourself. It never asks "how does that make you feel?" It speaks like a 道长 who has seen ten thousand people with the same problem — and tells you **stop trying**.

## How it works

1. `/start` — onboarding: name, age, city
2. 求签 — draw your daily fortune 
3. Talk — tell it what's on your mind, in Chinese or English
4. It responds: it never tells you to fix yourself..

## Setup

```bash
git clone https://github.com/AilieYiming/stop-trying.git
cd stop-trying
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:
```
TELEGRAM_BOT_TOKEN=your_token_from_botfather
ANTHROPIC_API_KEY=your_key_from_console_anthropic_com
```

Create your `SKILL.md` (see `SKILL.example.md` for the format). This is the system prompt — the bot's personality. It's gitignored so it stays private.

Run:
```bash
python telegram_bot.py
```

Open Telegram → find your bot → `/start`.

## Getting tokens

**Telegram bot token:** Open Telegram → @BotFather → `/newbot` → copy token

**Anthropic API key:** [console.anthropic.com](https://console.anthropic.com) → API Keys

## Commands

| Command | What it does |
|---------|-------------|
| `/start` | Begin onboarding + draw fortune |
| `/reset` | Clear profile, start over |

## File structure

```
stop-trying/
├── telegram_bot.py      ← Bot logic (Telegram + Claude API)
├── SKILL.md             ← System prompt / personality (gitignored, private)
├── SKILL.example.md     ← Template for creating your own SKILL.md
├── prd.md               ← Product requirements document
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Philosophy

> 曲则全，枉则直，洼则盈。
> *Yield and overcome. Bend and be straight. Empty and be full.*

> 上善若水。水善利万物而不争。
> *The highest good is like water — it benefits all things without striving.*

The bot never tells you to meditate, journal, or "try harder." It tells you the world is hard and reminds you: 别试了。足够了。

## License

MIT
