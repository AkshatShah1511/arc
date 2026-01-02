# 🛰️ ARC — Agentic Research & Contact
**Quality over Quantity. Context over Noise.**

ARC is a human-in-the-loop agentic system that turns **manual web signals** into **high-context Gmail drafts**.  
It automates research and drafting while keeping humans firmly in control.

---

## ✨ What ARC Does

1. Capture a company signal (email + website) via a Chrome extension  
2. Research the company using real website content  
3. Decide if the company is a good outreach match  
4. Draft a personalized email  
5. Create a **Gmail draft** for human review  

No auto-sending. No spam.

---

## 🧠 Architecture

Chrome Extension
↓
Google Sheets (State Queue)
↓
Website Fetcher + Heuristics
↓
Agent 1: Research & Match
↓
Agent 2: Email Drafting
↓
Gmail Draft (Human Review)


---

## 🧩 Key Features

- Human-in-the-loop by design  
- Explainable agent decisions  
- Real website understanding (no URL guessing)  
- Context-aware, job-seeker perspective drafting  
- Safe automation (drafts only)

---

## 🛠️ Tech Stack

- Chrome Extension (Manifest V3)
- Python agent pipeline
- Google Sheets API (state & coordination)
- Gmail API (draft creation)
- Gemini (LLM reasoning & drafting)

---

## 🚀 How It Works

1. Start the watcher:
   ```bash python3 watch.py
2.Add a signal using the extension
3.ARC automatically drafts an email in Gmail

🔐 Safety Principles
-No auto-sending emails
-No hidden background actions
-Full human control & review

🏆 Why ARC

Most tools optimize for volume.
ARC optimizes for judgment, context, and quality.

👤 Author  
Built by Akshat Shah
As a study in human-centered agentic systems.
