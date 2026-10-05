from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
print("BOT_TOKEN EXISTS:", bool(BOT_TOKEN))
print("BOT_TOKEN LENGTH:", len(BOT_TOKEN) if BOT_TOKEN else 0)
print("TOKEN START:", repr(BOT_TOKEN[:5]) if BOT_TOKEN else None)
print("TOKEN END:", repr(BOT_TOKEN[-5:]) if BOT_TOKEN else None)
# =========================================================
# CATEGORY BUTTONS
# این ایموجی‌ها فقط برای نمایش دکمه‌ها هستند
# =========================================================

CATEGORIES = {
    "fun": ("🎉", "Fun"),
    "music": ("🎵", "Music"),
    "animations": ("🦄", "Animations"),
    "movies": ("🎬", "Movies"),
    "games": ("🎮", "Games"),
    "idk": ("👀", "IDK"),
    "vehicles": ("🚗", "Vehicles"),
    "military": ("🪖", "Military"),
    "brink": ("☕", "Brink"),
    "sports": ("🏀", "Sports"),
    "motivational": ("⬆️", "Motivational"),
}


# =========================================================
# CAPTION SETTINGS
# =========================================================

CAPTION_SETTINGS = {
    "fun": ("🐺", "Earth024", "#Fun"),
    "music": ("🐺", "Earth024", "#Music"),
    "animations": ("🐺", "Earth024", "#Animations"),
    "movies": ("🐺", "Earth024", "#Movies"),
    "games": ("🐺", "Earth024", "#Games"),
    "idk": ("🐺", "Earth024", "#IDK"),
    "vehicles": ("🐺", "Earth024", "#Vehicles"),
    "military": ("🐺", "Earth024", "#Military"),
    "brink": ("🐺", "Earth024", "#Brink"),
    "sports": ("🐺", "Earth024", "#Sports"),
    "motivational": ("🐺", "Earth024", "#Motivational"),
}


# =========================================================
# CREATE CATEGORY KEYBOARD
# =========================================================

def category_keyboard():

    buttons = []
    row = []

    for key, (icon, name) in CATEGORIES.items():

        button = InlineKeyboardButton(
            f"{icon} {name}",
            callback_data=f"category:{key}"
        )

        row.append(button)

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(buttons)


# =========================================================
# HANDLE NEW VIDEO IN CHANNEL
# =========================================================

async def handle_video(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.channel_post

    if not message:
        return

    if not message.video:
        return

    try:

        await message.edit_reply_markup(
            reply_markup=category_keyboard()
        )

        print(
            f"Buttons added to message {message.message_id}"
        )

    except Exception as e:

        print("Error adding buttons:", e)


# =========================================================
# CATEGORY BUTTON CLICK
# =========================================================

async def category_selected(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if not query:
        return

    message = query.message

    if not message:
        return


    # =====================================================
    # CHECK USER PERMISSION
    # =====================================================

    try:

        member = await context.bot.get_chat_member(
            chat_id=message.chat_id,
            user_id=query.from_user.id
        )

        # administrator = ادمین
        # creator = مالک کانال

        if member.status not in (
            "administrator",
            "creator"
        ):

            await query.answer(
                "❌ فقط ادمین‌ها می‌تونن دسته‌بندی رو انتخاب کنن.",
                show_alert=True
            )

            return

    except Exception as e:

        print("Admin check error:", e)

        await query.answer(
            "❌ نتونستم دسترسی شما رو بررسی کنم.",
            show_alert=True
        )

        return


    # =====================================================
    # BUTTON IS VALID
    # =====================================================

    await query.answer()

    data = query.data

    if not data.startswith("category:"):
        return

    category = data.split(":", 1)[1]


    # =====================================================
    # CHECK CATEGORY
    # =====================================================

    if category not in CAPTION_SETTINGS:
        return


    # =====================================================
    # GET CAPTION SETTINGS
    # =====================================================

    emoji, name, hashtag = CAPTION_SETTINGS[category]

    caption = f"{emoji} | {name} | {hashtag}"


    # =====================================================
    # CHANGE CAPTION
    # REMOVE BUTTONS
    # =====================================================

    try:

        await message.edit_caption(
            caption=caption,
            reply_markup=None
        )

        print(
            f"Message {message.message_id} "
            f"changed to {category}"
        )

    except Exception as e:

        print("Error editing caption:", e)


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    print("ERROR:", context.error)


# =========================================================
# MAIN
# =========================================================

def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )


    # New videos
    app.add_handler(
        MessageHandler(
            filters.VIDEO,
            handle_video
        )
    )


    # Category buttons
    app.add_handler(
        CallbackQueryHandler(
            category_selected,
            pattern=r"^category:"
        )
    )


    # Errors
    app.add_error_handler(error_handler)


    print("Bot started...")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# =========================================================
# START BOT
# =========================================================

if __name__ == "__main__":
    main()