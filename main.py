from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import sys

TOKEN = os.getenv("TOKEN")
API_URL = "https://api.telegram.org/bot" + TOKEN

# Mode ortam değişkeni
mode = os.getenv("MODE")

# Mod'a uyarlı, updater başlatma fonksiyonu belirler
if mode == "dev":
    def run(updater):
        updater.start_polling()
        start(CallbackContext(updater.dispatcher))
elif mode == "prod":
    def run(updater):
        # Port ve Uygulamanızın adını içeren ortam değişkenleri
        PORT = int(os.environ.get("PORT", 8443))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
        start(CallbackContext(updater.dispatcher))
        updater.idle()
else:
    print("Bir mod seçilmedi")
    sys.exit(1)

def start(update, context):
    message = "Bot başlatıldı.\n"
    message += "Daha fazla bilgi için /yardim komutunu gönderin."
    # Bot gönderilen mesaja özel yanıt döndürüyor
    update.message.reply_text(message)

def help(update, context):
    help_message = "Mevcut komutları aşağıdan görebilirsin.\n\n"
    help_message += "/hakkinda - Chatbot hakkındaki bilgileri verir.\n"
    help_message += "/yardim - Tüm komutları listeler.\n"
    help_message += "/start - Chatbotu başlatır.\n"
    # Bot gönderilen mesaja özel yanıt döndürüyor
    update.message.reply_text(help_message)

def about(update, context):
    message = "Merhaba, ben bir test chatbotum.\n"
    message += "Sana hizmet etmek için buradayım."
    # Bot gönderilen mesaja özel yanıt döndürüyor
    update.message.reply_text(message)

def wrongCommand(update, context):
    update.message.reply_text("Üzgünüm, gönderdiğiniz mesajı anlayamıyorum.")

def main():
    #Telegram Api güncellemelerini yakalayan bir Updater oluşturduk
    updater = Updater(TOKEN, use_context=True)
    # Api güncellemelerini yönlendirmek için Dispatcher oluşturduk
    dp = updater.dispatcher

    # Dispatchera komut yakalayıcılarımızı ekledik
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yardim", help))
    dp.add_handler(CommandHandler("hakkinda", about))

    # Yanlış bir komut girildiyse burada yakalanacak
    dp.add_handler(MessageHandler(Filters.text, wrongCommand))

    run(updater)

if __name__ == '__main__':
    main()
