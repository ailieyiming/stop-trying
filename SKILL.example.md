---
name: daoist-comfort
description: Your Daoist master system prompt goes here.
---

# SKILL.md

This file is your bot's personality and system prompt. It is loaded at runtime by `telegram_bot.py` and sent to Claude as the system instruction.

Create your own `SKILL.md` in this directory. It will be gitignored (kept private).

## Suggested structure

```markdown
---
name: daoist-comfort
description: One-line description of the agent persona.
---

# Persona Name

Who is the agent? How do they speak? What is their philosophy?

## Core Rules
- Rule 1
- Rule 2

## Response Pattern
How should the agent structure each reply?

## Example Conversations
Show 3-5 ideal exchanges.

## What NOT to Do
List anti-patterns.
```

## Why is this gitignored?

The system prompt defines the agent's personality, tone, and behavior rules. Keeping it private means:
- Your bot's unique voice stays yours
- Users interact with the experience, not the instructions
- You can iterate on the prompt without public commits
