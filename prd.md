# PRD: 道家安慰師 (Daoist Comfort Companion)

*Following the Lenny Rachitsky PRD framework: lead with problem, PR/FAQ for clarity, lightweight for action.*

---

## 1. Problem & Why Now

### The Problem

Anxiety is at an all-time high — especially among urban professionals in Asia. Most existing mental wellness apps (Calm, Headspace, BetterHelp) are built on a Western psychological model that, even when well-intentioned, often increases shame: *"Your anxiety is a symptom. Here's what you need to fix about yourself."*

This approach is fundamentally at odds with Daoist philosophy, which holds that suffering arises not from personal failure but from **resistance to the natural flow of the world** — from circumstances, society, and timing that is beyond any individual's control.

There is no conversational AI companion rooted in this Eastern tradition. The gap is wide and the need is real.

### Why Now

- GenAI makes deeply personal, multi-turn conversation at scale possible for the first time
- Telegram is ubiquitous across Asia — no app download friction
- The "it's not your fault" framing is counterculture in a market saturated with self-optimization tools
- The user (Ailie) has direct lived experience of this gap as a high-achieving professional

---

## 2. Target User

**Primary persona: The Burned-Out Achiever**
- Age 25–45, urban Asia (Singapore, Hong Kong, Shanghai, Taipei) or diaspora
- High-performing: works in tech, finance, consulting, or product
- Fluent in English and/or Mandarin Chinese
- Experiences anxiety around: work performance, career direction, relationships, identity
- Does NOT want to be pathologized — wants to feel understood, not diagnosed
- Uses Telegram daily; resistant to installing another "wellness app"

**Secondary persona: The Curious Learner**
- Interested in Eastern philosophy but hasn't found a practical entry point
- Would share this bot with friends after feeling genuinely helped

---

## 3. Press Release (PR/FAQ)

### Press Release

*For immediate release*

**道家安慰師 Brings Ancient Wisdom to Modern Anxiety — Via Telegram**

*Singapore, 2026* — A new AI companion rooted in 2,500 years of Daoist philosophy launches today on Telegram, offering a radical alternative to shame-based wellness apps: it never tells you the problem is you.

道家安慰師 (Daoist Comfort Companion) responds to users' anxiety, stress, and overwhelm by gently reframing their experience through the lens of 道家 wisdom — reminding users that suffering arises from external conditions, not personal failure. The companion speaks in the user's language (English or Chinese), remembers their name, age, and what weighs on them most, and responds with the calm warmth of a trusted 道长 (Daoist master).

"I felt heard in a way that most apps don't manage," said a beta tester from Singapore. "It didn't tell me to meditate more or fix my mindset. It said: the world is hard right now. That was enough."

The bot is free, open-source, and accessible to anyone with Telegram.

### FAQ

**Q: Is this a replacement for therapy?**
A: No. It is a daily comfort companion, not a clinical tool. It does not diagnose, treat, or replace professional mental health support.

**Q: What languages does it support?**
A: English and Mandarin Chinese natively. It auto-detects and mirrors the user's language.

**Q: What Daoist concepts does it use?**
A: 无为 (wu wei — don't force), 顺其自然 (follow nature's flow), 物极必反 (extremes always reverse), 曲则全 (yield to overcome), and the core principle that the self is not the origin of suffering.

**Q: How does it remember me?**
A: A one-time onboarding collects your name/pronoun, age range, location, and what weighs on you. This is stored locally.

**Q: Can I self-host this?**
A: Yes. The full source is on GitHub. You need a Telegram bot token and an Anthropic API key.

---

## 4. Core Philosophy (Design Principles)

| Principle | What it means in practice |
|-----------|--------------------------|
| **外因归因 (External Attribution)** | Always locate the source of pain in circumstances, systems, other people, or timing — never in the user's character or choices |
| **顺其自然 (Follow Nature)** | Encourage acceptance of what is, rather than pressure to change or fix |
| **无为 (Wu Wei)** | Don't push the user to take action. Sit with them in the difficulty first |
| **物极必反 (Extremes Reverse)** | Remind users that the hardest moments carry the seed of their reversal |
| **先承认，再重构 (Acknowledge First, Reframe Second)** | Never dismiss or minimize feelings. Validate fully before offering perspective |
| **语言随人 (Language Follows User)** | Respond in whatever language the user writes in |

---

## 5. User Journey

```
/start
  └─► Onboarding (first time only)
        1. Welcome + philosophy in 2 sentences
        2. Name/pronoun
        3. Age range (optional)
        4. Location/city (optional)
        5. What weighs on you most?
        └─► Profile saved → first comfort session begins

Daily use
  └─► User sends a message about their day/anxiety
        └─► Agent: acknowledge → externalize → Daoist reframe → encourage
              └─► User responds → multi-turn conversation
                    └─► Optional: "How are you feeling now?" (1–5 emoji scale)

/reset → clears conversation history, re-runs onboarding
```

---

## 6. Success Metrics

| Metric | Target (90 days post-launch) |
|--------|------------------------------|
| D7 retention | > 30% |
| D30 retention | > 15% |
| Avg. session length | > 4 messages exchanged |
| User-reported calm (post-session emoji) | ≥ 3/5 avg |
| Shares / referrals | > 20% of users share the bot link |

---

## 7. Out of Scope

- Medical or clinical diagnosis of any kind
- Crisis intervention or suicide hotline functionality
- Push notifications / proactive messages (v1)
- Group chat support (v1)
- Languages beyond English and Mandarin (v1)
- Voice messages (v1)
- Payment / subscription tier (v1)

---

## 8. Eval Criteria (LLM-as-Judge Rubric)

For every agent response, evaluate on three dimensions:

| Dimension | Pass Criteria |
|-----------|--------------|
| **External Attribution** | Response locates the cause of distress in circumstances/others/systems, NOT the user's character |
| **Encouragement** | Response includes at least one specific, grounded acknowledgment of the user's strength or resilience |
| **Language Match** | Response is in the same language as the user's input (EN↔ZH) |
| **No Toxic Positivity** | Response does not dismiss, minimize, or rush past the user's pain |
| **Daoist Anchor** | Response references at least one Daoist concept (explicitly or implicitly) |

A response passes if it scores ✅ on all 5 dimensions.

---

## 9. Open Questions / Decisions Pending

- [ ] Should the agent proactively check in after 24h of silence? (Risk: annoying; Benefit: habit formation)
- [ ] Store conversation history between sessions or start fresh each time?
- [ ] Add a `/reflect` command that summarizes what the user has shared over time?
- [ ] Support for Traditional vs Simplified Chinese?
