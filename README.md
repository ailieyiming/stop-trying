# stop-trying 别试了

A Telegram bot that eases anxiety through Daoist (道家) philosophy.

一个用道家哲学帮你缓解焦虑的 Telegram 机器人。

---

## What is this? / 这是什么？

**EN:** It never tells you to fix yourself. It never asks "how does that make you feel?" It speaks like a 道长 (Daoist master) who has seen ten thousand people with the same problem — and tells you, in three sentences or less, that it's not your fault. For things you can't control, it doesn't analyze why. It just says: what's the big deal?

**ZH:** 它不会让你修自己。不会问"你觉得呢？"它像一个见过一万个人的道长——用最多三句话告诉你：不是你的问题。对于你控制不了的事，它不分析原因，直接说：有什么大不了的？

---

## How it works / 怎么用

1. `/start` — Onboarding: name, age, city / 输入姓名、年龄、城市
2. 求签 — Draw your daily fortune / 抽今日运签（上上签 / 上签 / 中签 / 下签）
3. Talk — Tell it what's bothering you / 说出你的烦恼
4. It responds: names the external cause, gives you one physical action, drops a Daoist quote. Done. / 它回复：点破外因，给你一个身体动作，丢一句道家经典。完。

---

## Setup / 安装

### 1. Clone / 克隆

```bash
git clone https://github.com/AilieYiming/stop-trying.git
cd stop-trying
```

### 2. Install dependencies / 安装依赖

```bash
pip install -r requirements.txt
```

### 3. Configure / 配置

```bash
cp .env.example .env
```

Edit `.env` — you only need your Telegram bot token:
编辑 `.env` — 只需要填你的 Telegram bot token：

```
TELEGRAM_BOT_TOKEN=your_token_from_botfather
```

**How to get a Telegram bot token / 如何获取 bot token：**
1. Open Telegram → search `@BotFather` / 打开 Telegram → 搜索 `@BotFather`
2. Send `/newbot` → follow prompts → copy the token / 发送 `/newbot` → 按提示操作 → 复制 token

### 4. Run / 运行

```bash
python telegram_bot.py
```

Open Telegram → find your bot → `/start`

打开 Telegram → 找到你的 bot → 发送 `/start`

---

## Commands / 命令

| Command | What it does / 功能 |
|---------|-------------|
| `/start` | Begin onboarding + draw fortune / 开始注册 + 抽签 |
| `/reset` | Clear profile, start over / 清除资料，重新开始 |

---

## Philosophy / 哲学

> 曲则全，枉则直，洼则盈。
> *Yield and overcome. Bend and be straight. Empty and be full.*

> 上善若水。水善利万物而不争。
> *The highest good is like water — it benefits all things without striving.*

The bot never tells you to meditate, journal, or "try harder." It tells you the world is hard, gives you something small and physical to do right now, and reminds you:

这个 bot 不会叫你冥想、写日记、或"加油"。它告诉你世界本来就难，给你一个现在就能做的小动作，然后提醒你：

**别试了。你已经是你自己了。**

---

## License

MIT
