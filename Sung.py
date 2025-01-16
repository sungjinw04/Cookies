import httpx
import json
from pyrogram import Client, filters

# Initialize your Pyrogram Client
app = Client(
    "cookie_checker_bot",
    api_id=28620311,  # Replace with your API ID
    api_hash="3b5c4ed0598e48fc1ab552675555e693",  # Replace with your API Hash
    bot_token="7989900536:AAE0KyukB5zN5T0ZgFTKy7NA3rGnqXtYbc0",  # Replace with your Bot Token
)


def check_cookies(cookies):
    """
    Validate cookies by sending a test request.
    Returns True if cookies are valid, otherwise False.
    """
    test_url = "https://example.com"  # Replace with the website to validate cookies
    try:
        with httpx.Client(cookies=cookies, timeout=10) as client:
            response = client.get(test_url)
            # Check if the response indicates a valid login/session
            if response.status_code == 200:
                return True, "Cookies are active."
            else:
                return False, f"Cookies are invalid. Status Code: {response.status_code}"
    except Exception as e:
        return False, f"Error during validation: {e}"


@app.on_message(filters.command("checkcookies") & filters.reply)
async def handle_cookie_check(client, message):
    """
    Check cookies validity when a user replies to the command with cookies.
    """
    # Check if cookies are provided as text or file
    if message.reply_to_message.text:
        raw_cookies = message.reply_to_message.text.strip()
    elif message.reply_to_message.document:
        file_path = await message.reply_to_message.download()
        with open(file_path, "r") as file:
            raw_cookies = file.read()
    else:
        await message.reply("Please reply with valid cookies as text or a file.")
        return

    # Attempt to parse cookies
    try:
        cookies = json.loads(raw_cookies)
    except json.JSONDecodeError:
        await message.reply("Invalid cookie format. Please provide JSON-formatted cookies.")
        return

    # Check the cookies
    await message.reply("Checking cookies, please wait...")
    is_valid, result = check_cookies(cookies)

    if is_valid:
        await message.reply(f"✅ {result}")
    else:
        await message.reply(f"❌ {result}")


@app.on_message(filters.command("start"))
async def start_command(client, message):
    """
    Greet the user and explain how to use the bot.
    """
    await message.reply(
        "Hello! I can check if cookies are active or outdated.\n\n"
        "Reply to my `/checkcookies` command with your cookies in JSON format (as text or file)."
    )


if __name__ == "__main__":
    app.run()
  
