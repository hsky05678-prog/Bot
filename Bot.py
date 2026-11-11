import os
from anthropic import AsyncAnthropic
from telegram.ext import ApplicationBuilder, MessageHandler, filters

ai = AsyncAnthropic(api_key=os.environ["AI_API_KEY"])
history = {}

async def reply(update, ctx):
    msgs = history.setdefault(update.effective_user.id, [])
    msgs.append({"role": "user", "content": update.message.text})
    msgs[:] = msgs[-19:]
    r = await ai.messages.create(
        model="claude-sonnet-5-5", max_tokens=1000, messages=msgs)
    text = r.content[0].text
    msgs.append({"role": "assistant", "content": text})
    await update.message.reply_text(text)

app = ApplicationBuilder().token(os.environ["9023600914:AAFLMB6qs9yJbuaaOkIt6cu-cEhJZ_LlgQM"]).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
