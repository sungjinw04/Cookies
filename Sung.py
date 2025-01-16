from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests

app = Client("cookie_checker_bot", api_id=28620311, api_hash="3b5c4ed0598e48fc1ab552675555e693", bot_token="7989900536:AAE0KyukB5zN5T0ZgFTKy7NA3rGnqXtYbc0")

# Function to check YouTube cookie validity
def check_youtube_cookie(cookies):
    try:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example URL to test cookie
        response = requests.get(url, cookies=cookies, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        return False

# Start message with buttons
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    # Create an inline keyboard with a "Check Cookie" button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Check YouTube Cookie", callback_data="checkcookie")]
    ])

    # Send a welcome message with the button
    welcome_message = """
    ✨ Welcome to the Cookie Checker Bot! ✨
    🔍 This bot helps you verify if your YouTube cookie is valid or outdated.
    Click the button below to check your cookie! 🎉
    """
    await message.reply(welcome_message, reply_markup=keyboard)

# Command to check YouTube cookie
@app.on_message(filters.command("checkcookie"))
async def check_cookie(client: Client, message: Message):
    try:
        cookie = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
        if cookie:
            cookies = {'VISITOR_INFO1_LIVE': cookie}  # Add more cookies if necessary

            # Check cookie validity
            is_valid = check_youtube_cookie(cookies)
            if is_valid:
                await message.reply("✅ Your YouTube cookie is valid! 🎉")
            else:
                await message.reply("❌ Your YouTube cookie is outdated or invalid. Please check again.")
        else:
            await message.reply("⚠️ Please provide a valid YouTube cookie.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Start the bot
if __name__ == "__main__":
    app.run()


