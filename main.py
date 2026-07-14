import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN")
DETOX_URL = "https://coralclub.ru/shop/coral-detox.html?language=ru&REF_CODE=177934283555&app_redirect=y&search=Y&utm_source=copy-link&utm_medium=prod-recom"
DETOX_PLUS_URL = "https://coralclub.ru/shop/coral-detox-plus.html?language=ru&REF_CODE=177934283555&app_redirect=y&search=Y&utm_source=copy-link&utm_medium=prod-recom"
WELCOME_PHOTO = "https://i.ibb.co/VcsJdJHY/6-C84-AF11-FBD1-4-A23-9356-7887644063-C6.png"
DETOX_PHOTO = "https://i.ibb.co/SDSs339g/IMG-3344.jpg"
RESULT_PHOTO_1 = "https://i.ibb.co/9k6czTBz/IMG-3306.jpg"
RESULT_PHOTO_2 = "https://i.ibb.co/23szgCcd/IMG-3308.png"
RESULT_PHOTO_3 = "https://i.ibb.co/wFwSY4hJ/IMG-3309.png"

USERS = {}

QUESTIONS = [
    "🤢 Вопрос 1 из 18\n\nПосле жирной еды, праздничного стола или даже одного бокала вина — чувствуешь тяжесть, тошноту или давление в правом боку? Печень 'жалуется'?",
    "😵 Вопрос 2 из 18\n\nПросыпаешься с тяжёлой головой или 'туманом' — хотя накануне не пила и легла вовремя?",
    "😴 Вопрос 3 из 18\n\nК обеду уже нет сил, хочется лечь? Кофе даёт короткий всплеск и потом ещё больше усталость?",
    "🌫 Вопрос 4 из 18\n\nТрудно сосредоточиться, забываешь простые вещи, мысли 'плывут'? Чувствуешь что 'не в ресурсе'?",
    "💛 Вопрос 5 из 18\n\nКожа стала тусклой, серой, без сияния? Или желтоватый оттенок — заметный на фото при дневном свете?",
    "🌸 Вопрос 6 из 18\n\nВысыпания или акне появляются после праздников, стресса или определённой еды? Кожа реагирует на всё?",
    "💨 Вопрос 7 из 18\n\nНеприятный запах изо рта возвращается через час после чистки? Или горький привкус по утрам?",
    "🚽 Вопрос 8 из 18\n\nСтул реже чем каждый день? Или чередуются запоры и диарея — кишечник давно непредсказуем?",
    "⚖️ Вопрос 9 из 18\n\nЕшь относительно нормально, но вес растёт или стоит намертво — особенно в области живота?",
    "🍷 Вопрос 10 из 18\n\nПьёшь алкоголь хотя бы раз в неделю — вино за ужином, пиво в пятницу, бокал на встрече? Даже 'по чуть-чуть'?",
    "🚬 Вопрос 11 из 18\n\nКуришь — сигареты, кальян, электронные? Или живёшь/работаешь рядом с теми кто курит?",
    "💧 Вопрос 12 из 18\n\nПьёшь меньше 1,5 литров чистой воды в день? Чай, кофе и соки — не в счёт. Именно воды?",
    "💊 Вопрос 13 из 18\n\nПринимала антибиотики, гормональные таблетки или обезболивающие за последние 2 года?",
    "🥩 Вопрос 14 из 18\n\nЧасто ешь жареное, фастфуд, колбасы, копчёности или сладкое — хотя бы несколько раз в неделю?",
    "😤 Вопрос 15 из 18\n\nРезкие перепады настроения, срываешься на близких, тревога или раздражительность без причины — особенно вечером?",
    "💅 Вопрос 16 из 18\n\nВолосы выпадают больше обычного, ногти ломаются, кожа сухая — хотя пьёшь витамины и ухаживаешь за собой?",
    "🤧 Вопрос 17 из 18\n\nБолеешь чаще 3-4 раз в год? Любой вирус 'цепляется' быстро и долго не отпускает?",
    "🏙 Вопрос 18 из 18\n\nЖивёшь в городе, часто бываешь в пробках, дышишь городским воздухом? Или работаешь в помещении без проветривания?",
]

WELCOME_TEXT = "👋 Тебя приветствует клуб докторов и нутрициологов!\n\nМы подготовили этот тест на уровень интоксикации специально для участников нашего интенсива — как один из первых шагов к пониманию своего здоровья.\n\nТоксины накапливаются в нашем организме каждый день. Усталость без причины, тусклая кожа, лишний вес — это сигналы перегруженного организма.\n\n⚠️ Чем дольше токсины в организме — тем глубже последствия.\n\nОтветь на 18 вопросов Да или Нет — и получишь не просто результат, а чёткое понимание что происходит в твоём теле.\n\n🕐 2-3 минуты — и полная ясность."
HOW_TO_BUY = "💡 Как купить по клубной цене:\n\nСначала переключись на вкладку 'Клубная цена' — она дешевле на 20%!\n\nЕсли ты уже зарегистрирован(а) в Coral Club:\n1. Нажми 'Клубная цена' на странице товара\n2. Нажми красную кнопку 'Зарегистрироваться'\n3. Прокрути вниз, найди 'У вас есть Coral ID? Войти' и нажми 'Войти'\n\nЕсли ты ещё не зарегистрирован(а):\nНапиши человеку который поделился с тобой этим тестом — он поможет оформить клубную карту и ты сразу получишь скидку 20% + бесплатную консультацию нутрициолога."
CLOSING = "🌿 Твоё здоровье — это твой выбор.\n\nТоксины не уходят сами. Один курс детоксикации — и организм получает шанс восстановиться. Наши врачи и нутрициологи видят это каждый день.\n\n⏳ Чем дольше ждёшь — тем глубже последствия. Действуй сейчас — пока организм ещё сам просит о помощи."

def get_result_text(yes):
    if yes <= 5:
        return f"🟡 Результат — {yes} из 18 совпадений\n\nНе спеши выдыхать. Даже небольшое количество совпадений говорит о том, что токсины уже работают против тебя. Врачи рекомендуют профилактический курс минимум 1 раз в год. Coral Detox — это не лечение, это обслуживание здорового организма."
    elif yes <= 11:
        return f"🟠 Результат — {yes} из 18 совпадений\n\nТвоё тело подаёт сигналы. Печень, кишечник и лимфа уже работают в режиме перегрузки. Наши врачи настоятельно рекомендуют курс детоксикации как можно скорее."
    else:
        return f"🔴 Результат — {yes} из 18 совпадений\n\nЭто серьёзно. Высокая токсическая нагрузка — твой организм работает на износ. Нужна глубокая системная очистка Coral Detox Plus."

def get_result_photo(yes):
    return RESULT_PHOTO_1 if yes <= 5 else RESULT_PHOTO_2 if yes <= 11 else RESULT_PHOTO_3

def make_kb(yes, with_restart=False):
    buttons = [[InlineKeyboardButton("🌿 Coral Detox", url=DETOX_URL)], [InlineKeyboardButton("🌿 Coral Detox Plus", url=DETOX_PLUS_URL)]]
    if with_restart: buttons.append([InlineKeyboardButton("🔄 Пройти снова", callback_data="restart")])
    return InlineKeyboardMarkup(buttons)

async def send_delayed_messages(bot, chat_id, yes):
    try:
        await asyncio.sleep(37)
        await bot.send_photo(chat_id=chat_id, photo=DETOX_PHOTO, caption=HOW_TO_BUY, reply_markup=make_kb(yes))
        await asyncio.sleep(55)
        await bot.send_photo(chat_id=chat_id, photo=WELCOME_PHOTO, caption=CLOSING, reply_markup=make_kb(yes, True))
    except Exception as e: logging.error(f"Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS[update.effective_user.id] = {"step": 0, "yes": 0}
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Начать тест", callback_data="start")]])
    await update.message.reply_photo(photo=WELCOME_PHOTO, caption=WELCOME_TEXT, reply_markup=kb)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    if q.data in ("start", "restart"):
        USERS[uid] = {"step": 0, "yes": 0}
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Да", callback_data="да_0"), InlineKeyboardButton("❌ Нет", callback_data="нет_0")]])
        await q.message.reply_text(QUESTIONS[0], reply_markup=kb)
        return
    if "_" not in q.data: return
    parts = q.data.rsplit("_", 1)
    ans, q_idx = parts[0], int(parts[1])
    if uid not in USERS or q_idx != USERS[uid]["step"]: return
    if ans == "да": USERS[uid]["yes"] += 1
    await q.edit_message_text(QUESTIONS[q_idx] + f"\n\nТвой ответ: {'✅ Да' if ans == 'да' else '❌ Нет'}")
    next_step = q_idx + 1
    USERS[uid]["step"] = next_step
    if next_step < len(QUESTIONS):
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Да", callback_data=f"да_{next_step}"), InlineKeyboardButton("❌ Нет", callback_data=f"нет_{next_step}")]])
        await q.message.reply_text(QUESTIONS[next_step], reply_markup=kb)
    else:
        yes = USERS[uid]["yes"]
        await context.bot.send_photo(chat_id=q.message.chat_id, photo=get_result_photo(yes), caption=get_result_text(yes))
        asyncio.create_task(send_delayed_messages(context.bot, q.message.chat_id, yes))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
