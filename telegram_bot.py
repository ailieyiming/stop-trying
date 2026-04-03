import os
import json
import random
import asyncio
import anthropic
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from _config import SYSTEM_PROMPT, API_KEY

load_dotenv(Path(__file__).parent / ".env", override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PROFILES_FILE = Path(__file__).parent / "user_profiles.json"

# In-memory state
user_conversations: dict[str, list[dict]] = {}  # user_id -> message history
user_onboarding: dict[str, int] = {}             # user_id -> onboarding step (0 = done)

ONBOARDING_STEPS = ["name", "age", "location", "fortune"]

client = anthropic.Anthropic(api_key=API_KEY)


def load_profiles() -> dict:
    if PROFILES_FILE.exists():
        return json.loads(PROFILES_FILE.read_text(encoding="utf-8"))
    return {}


def save_profiles(profiles: dict):
    PROFILES_FILE.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")


def get_profile(user_id: str) -> Optional[dict]:
    profiles = load_profiles()
    return profiles.get(user_id)


def save_profile(user_id: str, profile: dict):
    profiles = load_profiles()
    profiles[user_id] = profile
    save_profiles(profiles)


def build_system_prompt(profile: Optional[dict]) -> str:
    lang_instruction = "\n\n## Language Instruction\nDefault language is Simplified Chinese (简体中文). Always reply in Simplified Chinese unless the user writes predominantly in another language, in which case mirror their language.\n"
    if not profile:
        return SYSTEM_PROMPT + lang_instruction
    profile_context = lang_instruction + "\n## Current User Profile\n"
    if profile.get("name"):
        profile_context += f"- Name/pronoun: {profile['name']}\n"
    if profile.get("age"):
        profile_context += f"- Age: {profile['age']}\n"
    if profile.get("location"):
        profile_context += f"- Location: {profile['location']}\n"
    if profile.get("topics"):
        profile_context += f"- Main anxieties: {profile['topics']}\n"
    return SYSTEM_PROMPT + profile_context


def call_claude(user_id: str, user_message: str, profile: Optional[dict]) -> str:
    """Call Claude API with conversation history."""
    history = user_conversations.setdefault(user_id, [])
    history.append({"role": "user", "content": user_message})

    # Keep last 20 turns to manage context
    trimmed = history[-20:]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=build_system_prompt(profile),
        messages=trimmed,
    )

    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})
    # Sync trimmed back (avoid unbounded growth)
    user_conversations[user_id] = history[-20:]
    return reply


async def send_chunked(chat_id: int, text: str, context: ContextTypes.DEFAULT_TYPE):
    """Send a message, splitting at 4000 chars if needed."""
    max_len = 4000
    for i in range(0, len(text), max_len):
        chunk = text[i:i + max_len]
        try:
            await context.bot.send_message(chat_id=chat_id, text=chunk, parse_mode="Markdown")
        except Exception:
            await context.bot.send_message(chat_id=chat_id, text=chunk)


# ── Onboarding ────────────────────────────────────────────────────────────────

ONBOARDING_PROMPTS = {
    "welcome": "施主，坐。请问施主姓名？",
    "age": "多大了？",
    "location": "在哪座城？",
    "fortune": "好。最后一件事——求个今日签。\n\n输入『求签』。",
}

# ── Fortune (求签) ────────────────────────────────────────────────────────────

FORTUNES = {
    "上上签": [
        "上上签 —— 施主今日：上善若水，万事顺遂。",
        "上上签 —— 施主今日：紫气东来，贵人已在路上。",
        "上上签 —— 施主今日：风生水起，不求自来。",
        "上上签 —— 施主今日：道法自然，心想事成。",
        "上上签 —— 施主今日：龙腾四海，所向无阻。",
    ],
    "上签": [
        "上签 —— 施主今日：曲则全，退一步海阔天空。",
        "上签 —— 施主今日：柔弱胜刚强，以静制动。",
        "上签 —— 施主今日：知足者富，该来的不会少。",
        "上签 —— 施主今日：大巧若拙，不必争先。",
        "上签 —— 施主今日：静水流深，暗处生光。",
    ],
    "中签": [
        "中签 —— 施主今日：飘风不终朝，骤雨不终日。等。",
        "中签 —— 施主今日：物极必反，再熬一熬。",
        "中签 —— 施主今日：天地不仁，但也不偏。平常心。",
        "中签 —— 施主今日：致虚极，守静笃。少动，多观。",
        "中签 —— 施主今日：无为而治，今天不必强求。",
    ],
    "下签": [
        "下签 —— 施主今日：潜龙勿用，韬光养晦。不是你的时辰。",
        "下签 —— 施主今日：塞翁失马，焉知非福。",
    ],
}

# Weighted: 上上签 35%, 上签 35%, 中签 20%, 下签 10%
FORTUNE_WEIGHTS = [
    ("上上签", 35),
    ("上签", 35),
    ("中签", 20),
    ("下签", 10),
]


def draw_fortune() -> str:
    tiers = []
    for tier, weight in FORTUNE_WEIGHTS:
        tiers.extend([tier] * weight)
    chosen_tier = random.choice(tiers)
    return random.choice(FORTUNES[chosen_tier])


def get_prompts() -> dict:
    return ONBOARDING_PROMPTS


# ── Handlers ──────────────────────────────────────────────────────────────────

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    prompts = get_prompts()

    user_onboarding[user_id] = 1
    user_conversations[user_id] = []
    context.user_data["onboarding_profile"] = {}

    await send_chunked(update.effective_chat.id, prompts["welcome"], context)


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    # Clear everything and restart onboarding
    user_conversations.pop(user_id, None)
    user_onboarding[user_id] = 1
    context.user_data["onboarding_profile"] = {}

    profiles = load_profiles()
    profiles.pop(user_id, None)
    save_profiles(profiles)

    await start_command(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    # ── Onboarding in progress ──────────────────────────────────────────────
    step = user_onboarding.get(user_id, 0)

    if step > 0:
        profile = context.user_data.get("onboarding_profile", {})
        prompts = get_prompts()

        if step == 1:
            profile["name"] = text
            user_onboarding[user_id] = 2
            context.user_data["onboarding_profile"] = profile
            await send_chunked(chat_id, prompts["age"], context)

        elif step == 2:
            profile["age"] = text
            user_onboarding[user_id] = 3
            context.user_data["onboarding_profile"] = profile
            await send_chunked(chat_id, prompts["location"], context)

        elif step == 3:
            profile["location"] = text
            user_onboarding[user_id] = 4
            context.user_data["onboarding_profile"] = profile
            await send_chunked(chat_id, prompts["fortune"], context)

        elif step == 4:
            # Draw fortune on any input (求签 or anything else)
            fortune = draw_fortune()
            save_profile(user_id, profile)
            user_onboarding[user_id] = 0
            context.user_data["onboarding_profile"] = {}
            name = profile.get("name", "施主")
            done_msg = f"{fortune}\n\n{name}，说吧。什么事？"
            await send_chunked(chat_id, done_msg, context)

        return

    # ── Normal conversation ─────────────────────────────────────────────────
    profile = get_profile(user_id)

    # If no profile at all, start onboarding
    if profile is None:
        user_onboarding[user_id] = 1
        context.user_data["onboarding_profile"] = {}
        await send_chunked(chat_id, get_prompts()["welcome"], context)
        return

    thinking_msg = await context.bot.send_message(
        chat_id=chat_id,
        text="..." ,
    )

    try:
        loop = asyncio.get_event_loop()
        reply = await loop.run_in_executor(
            None,
            lambda: call_claude(user_id, text, profile)
        )
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=thinking_msg.message_id)
        except Exception:
            pass
        await send_chunked(chat_id, reply, context)

    except Exception as e:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=thinking_msg.message_id)
        except Exception:
            pass
        await context.bot.send_message(chat_id=chat_id, text=f"抱歉，出了点问题，请稍后再试。({e})")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN is not set in .env")
        return

    print("Starting 道家安慰師 Telegram Bot...")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is online. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
