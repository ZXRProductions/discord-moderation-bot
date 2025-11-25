# Contributing to discord-moderation-bot

Thanks for your interest in contributing!  
This project is intentionally small and easy to work with, and contributions are always welcome — whether it’s fixing a bug, improving documentation, or adding new features.

Please take a moment to read the guidelines below before opening a pull request.

---

## Getting Started

1. **Fork the repository** on GitHub  
2. **Clone your fork** locally:  
```bash
git clone https://github.com/your-username/discord-moderation-bot.git
```
3. Create and activate a virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Create a `.env` file based on `.env.example` (or the README instructions).

---

## Making Changes
- Keep the code style consistent with the existing project.
- Avoid adding unnecessary dependencies.
- If you add a new command, place it inside the commands/ folder as its own cog.
- If you introduce new configuration values, document them clearly.
- For database changes, update db.py and describe the change in your pull request.

---

## Commit Messages
Please write clear commit messages.

Example formats:
- `Add /kick command with permission checks`
- `Fix bug in stats query`
- `Improve README formatting`
- `Refactor db.py for clarity`

Avoid vague messages like “fix stuff” or “update”.

---

## Opening a Pull Request
When you’re ready:
1. Push your changes to your fork.
2. Open a pull request against the main branch.
3. Include:
- A short summary of what you changed
- Any relevant screenshots (if UI-related)
- Notes for reviewers if needed

I’ll review your PR as soon as possible.

---

## Code of Conduct

Please be respectful and constructive in all discussions.
We’re here to learn, share ideas, and build useful tools together.

---

Thanks again for taking the time to contribute!