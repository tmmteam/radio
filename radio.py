import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from datetime import datetime

# Logging Setup
logging.basicConfig(
    format="[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

LOGGER = logging.getLogger("RADIO-BOT")

# Radio Station URLs
RADIO_STATION = {
    "Air Bilaspur": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio110/playlist.m3u8",
    "Air Raipur": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio118/playlist.m3u8",
    "Capital FM": "http://media-ice.musicradio.com/CapitalMP3?.mp3",
    "English": "https://hls-01-regions.emgsound.ru/11_msk/playlist.m3u8",
    "Mirchi": "http://peridot.streamguys.com:7150/Mirchi",
}
valid_stations = "\n".join([f"`{name}`" for name in sorted(RADIO_STATION.keys())])

# Store start time
__start_time__ = datetime.now()

# Initialize Bot
app = Client(
    "radio_bot",
    api_id=12345,  # Replace with your API ID
    api_hash="your_api_hash",  # Replace with your API hash
    bot_token="your_bot_token",  # Replace with your bot token
)

# Start Button and Help Button
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Commands", callback_data="commands")],
            [InlineKeyboardButton("Add Me To Group", url="https://t.me/your_bot_username?startgroup=true")],
        ]
    )
    await message.reply_text(
        f"Hello, {message.from_user.mention}!\n\n"
        "I am a Radio Bot that can stream radio and media in your group voice chat.",
        reply_markup=buttons,
    )

@app.on_callback_query(filters.regex("commands"))
async def show_commands(client, query):
    commands = (
        "**Commands List**\n\n"
        "/radio [station_name] - Play radio.\n"
        "/pause - Pause the stream.\n"
        "/resume - Resume the stream.\n"
        "/skip - Skip to the next track.\n"
        "/stop - Stop the stream.\n"
        "/stats - Get bot statistics.\n"
        "/ping - Check bot's response time.\n"
    )
    await query.message.edit_text(commands)

# Radio Functionality
@app.on_message(filters.command(["radio", "radioplay"]) & filters.group)
async def radio(client, message: Message):
    station_name = " ".join(message.command[1:])
    RADIO_URL = RADIO_STATION.get(station_name)
    if not RADIO_URL:
        return await message.reply_text(
            f"Please specify a valid radio station!\nAvailable stations:\n{valid_stations}"
        )

    msg = await message.reply_text("Starting radio stream...")
    # Dummy logic for streaming (replace with your implementation)
    await asyncio.sleep(2)
    await msg.edit_text(f"Streaming **{station_name}** now!")

# Bot Broadcast
@app.on_message(filters.command("broadcast") & filters.user(5311223486))  # Replace with your user ID
async def broadcast(client, message):
    text = message.reply_to_message.text if message.reply_to_message else message.text.split(None, 1)[1]
    # Replace chat IDs with actual group IDs where you want to broadcast
    chat_ids = [-100210607104]  
    for chat_id in chat_ids:
        try:
            await client.send_message(chat_id, text)
        except Exception as e:
            LOGGER.error(f"Failed to send broadcast to {chat_id}: {e}")

# Ping and Stats
@app.on_message(filters.command("ping"))
async def ping(client, message):
    start_time = datetime.now()
    msg = await message.reply_text("Pinging...")
    end_time = datetime.now()
    await msg.edit_text(f"Pong! Response time: {(end_time - start_time).microseconds / 1000} ms.")

@app.on_message(filters.command("stats"))
async def stats(client, message):
    uptime = datetime.now() - __start_time__
    await message.reply_text(f"Bot is running for {uptime}.")

# Pause, Resume, Skip, Stop
@app.on_message(filters.command("pause"))
async def pause(client, message):
    await message.reply_text("Paused the stream.")

@app.on_message(filters.command("resume"))
async def resume(client, message):
    await message.reply_text("Resumed the stream.")

@app.on_message(filters.command("skip"))
async def skip(client, message):
    await message.reply_text("Skipped to the next track.")

@app.on_message(filters.command("stop"))
async def stop(client, message):
    await message.reply_text("Stopped the stream.")

# Run the Bot
if __name__ == "__main__":
    app.run()
