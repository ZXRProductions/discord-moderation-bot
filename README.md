# Discord Moderation & Analytics Bot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.6.4-5865F2?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/ZXRProductions/discord-moderation-bot)
![Issues](https://img.shields.io/github/issues/ZXRProductions/discord-moderation-bot)

## Table of Contents

- [Preview](#preview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Why SQLite?](#why-sqlite)
- [Contributing](#contributing)
- [License](#license)


A modular Discord moderation bot built in Python using `discord.py`.
It provides a simple warning system, per-server analytics, and a heartbeat task designed to keep track of the bot’s status over time. 
The codebase is intentionally small, clean, and easy to extend, ideal for learning or building upon.

---

## Preview

Here’s an example of the bot’s embed outputs:

![Bot preview - Usage outputs](previews/preview.png)

---

## Features

### 🔧 Moderation Tools
- **/warn @user reason**  
  Records a warning for a user in the server’s SQLite database.
- **/warnings @user**  
  Displays a user’s recent warnings, including moderator, reason, and timestamp.

### 📊 Analytics
- **/stats**  
  Summarizes moderation activity in the server:
  - Total warnings
  - Unique users warned
  - Top warned users
  - Warnings per moderator
  - Daily warnings (last 7 days)

### 🩺 Heartbeat Task
Runs every 5 minutes, logging:
- Number of servers the bot is in  
- Estimated member count  
- Total warnings in the database  

This provides a simple “health check” for monitoring the bot’s activity.

---

## Tech Stack

**Language:**
- Python 3.10+

**Frameworks & Libraries:**
- discord.py - Discord API wrapper
- python-dotenv - Environment variable management
- asyncio - Async event loop (standard library)

**Database:**  
- SQLite - Lightweight relational database (built into Python)

**Architecture:**
- Modular command cogs
- Layered structure (commands, config, database, main runner)
- Slash commands (Discord interactions API) 
- Background task (heartbeat loop)

**Tooling:**
- Git / GitHub for version control
- MIT License  
- Preview media included (`/previews/`)
- `.env.example` for environment setup

---

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```


### 2. Create a `.env` file
```
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_test_server_id # optional
```


### 3. Run the bot
```bash
python main.py
```

---

## Usage

Once the bot is running and invited to your server, you can use the following slash commands:

### `/ping`
Verifies the bot is online and responding.

### `/warn @user reason`
Adds a warning to the server’s database.
- The warning includes the user, moderator, reason, timestamp, and guild ID.
- Only users with the “Moderate Members” permission can use this command.

### `/warnings @user`
Shows the most recent warnings for a given user in the current server.
- Results display in an embed.
- The response is ephemeral (only visible to you).

### `/stats`
Displays moderation analytics for the server:
- Total warnings
- Unique users warned
- Top users by number of warnings
- Warnings per moderator
- Daily warnings (last 7 days)

### Background Heartbeat
A background task runs every 5 minutes and logs:
- Number of guilds the bot is in  
- Estimated member count  
- Total warnings in the database  
- A simple uptime-style “heartbeat”  

This helps verify that the bot is healthy and operating correctly.

---

## Project Structure
```
discord-mod-bot/
├─ main.py
├─ config.py
├─ db.py
├─ commands/
│  ├─ basic.py         # /ping
│  ├─ moderation.py    # /warn, /warnings
│  └─ stats.py         # /stats
├─ modbot.sqlite3
└─ requirements.txt
```

- **main.py**  
  Starts the bot, loads cogs, syncs slash commands, and runs the heartbeat task.

- **db.py**  
  Contains all SQLite database logic.  
  Handles warning creation, lookups, stats aggregation, and over-time analytics.

- **commands/**  
  Each file contains a Discord cog with slash commands grouped by purpose.

---

## Requirements
- Python 3.10 or later  
- `discord.py`  
- `python-dotenv`  
- SQLite (built into Python)

---

## Why SQLite?
For a small to medium-sized Discord bot, SQLite is fast, easy to maintain, and doesn’t require running an external database server. 
The schema is intentionally simple so it can be swapped for PostgreSQL or MySQL later if needed.

---

## Contributing
The project is intentionally minimal and easy to expand.  
If you'd like to add more commands, analytics, logging, or moderation tools, feel free to open a pull request.

---

## License
This project is licensed under the MIT License.
You’re free to use this project for your own bots or modify it however you like.