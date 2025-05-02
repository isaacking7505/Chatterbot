# TriviaMaster Bot
A Discord bot for trivia games and motivational quotes.

## Features
- `!trivia`: Start a trivia game
- `!quote`: Get random motivational quote
- Restricted to #CPT-1 channel
- Owner commands: `!restart`, `!shutdown`

## Setup
1. Rename `.env.example` to `.env` and fill values
2. Install requirements:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm