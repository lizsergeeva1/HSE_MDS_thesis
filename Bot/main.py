import telebot
from catboost import CatBoostRegressor
from load_data import collect_url_data
import warnings

warnings.filterwarnings("ignore")

token = "6835356691:AAHYWyYJoivdIGHMvl1GOIuz0SMlFc0tSu0"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_keyboard(message, text="Hello! \n"
                                "This bot predicts salary in the IT sector based on job link (hh.ru)\n"
                                "Please provide a link to the vacancy you are interested in"
                  ):
    # keyboard = types.ReplyKeyboardMarkup()
    # it = types.KeyboardButton("Lets start")
    # keyboard.add(it)
    url = bot.send_message(message.chat.id, text=text)
    bot.register_next_step_handler(url, step_pred)


@bot.message_handler(content_types=['text'])
def handle_errors(message):
    send_keyboard(message, text="Sorry, I don't understand:(")


def step_pred(url):
    try:
        X_test = collect_url_data(url.text)
        model = CatBoostRegressor()
        model.load_model('catboost_model.cbm')
        pred = int(round(model.predict(X_test)[0], -3))
        name, skills = X_test['name'].values[0], X_test['key_skills'].values[0]
        text_to_print = "Info from URL: \n" \
                        f"Vacancy: {name} \n" \
                        f"Required skills: {skills} \n" \
                        f"Approximate salary would be  {pred} rub"
        bot.send_message(url.chat.id, text_to_print)
        send_keyboard(url, 'Try again? Pass the URL')
    except:
        handle_errors(url)


bot.polling();
