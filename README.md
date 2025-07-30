# VibeCheckr

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A powerful Discord bot that checks the vibe using transformer-based models. Built with `discord.py`, `transformers`, and custom emotion detection logic.

## Features

- Emotion detection powered by HuggingFace models
- Fast and async-ready with `aiohttp`
- Easily configurable via `.env`
- Dashboard support

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/OmgRod/VibeCheckr.git
   cd vibecheckr
   ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file with your bot token:

    ```bash
    BOT_TOKEN=your_token_here
    ```

4. Run the bot:

    ```bash
    python bot.py
    ```

## License

MIT License. See [LICENSE](LICENSE).
