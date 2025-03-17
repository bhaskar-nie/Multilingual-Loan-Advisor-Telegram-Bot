import os
import asyncio
import logging
from flask import Flask
import multiprocessing
import bot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot is running", 200

def run_bot_process():
    """
    Run the bot in a separate process to avoid event loop conflicts
    """
    try:
        # Create a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the bot
        loop.run_until_complete(bot.main())
    except Exception as e:
        logger.error(f"Bot process error: {e}")

def run_server():
    port = int(os.environ.get('PORT', 5000))
    try:
        logger.info(f"Starting Flask server on port {port}")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Server startup error: {e}")

if __name__ == '__main__':
    # Use multiprocessing instead of threading
    bot_process = multiprocessing.Process(target=run_bot_process)
    bot_process.start()

    # Run Flask server in the main process
    run_server()

    # Ensure bot process is terminated when main process ends
    bot_process.join()