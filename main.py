import telebot
import requests
import time
from telebot import types

bot_token = '6031064732:AAHswx8tnxhYl5Hp_cPyF_GU2oL_EqRnH28'
bot = telebot.TeleBot(bot_token)

appid = '3ec53bf38002c6ec12cac9467e9817a9'
bot_city = 'Москва'
bot_lang = 'ru'
start_check = 0

def getData(bot_city, bot_lang, appid):
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'q': bot_city, 'units': 'metric', 'lang': bot_lang, 'APPID': appid})
    data = res.json()
    return data

def getData5(bot_city, bot_lang, appid):
    res = requests.get("https://api.openweathermap.org/data/2.5/forecast",
                       params={'q': bot_city, 'units': 'metric', 'lang': bot_lang, 'APPID': appid})
    data5 = res.json()
    return data5

@bot.message_handler(commands=['start', 'restart'])
def start(message):
    global start_check
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("🇷🇺Русский", "🇺🇸English")
    bot.send_message(message.chat.id, 'Выберите язык/Choose language', reply_markup=keyboard)
    start_check += 1

@bot.message_handler(content_types=['text'])
def answer(message):
    text = message.text
    global start_check, bot_lang, data, data5, \
        bot_city_ru, bot_city_eng, last_city2_ru, last_city_ru, last_city2_eng, last_city_eng
    if text == "🇷🇺Русский" and start_check == 1:
        bot_lang = 'ru'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('Москва', 'Якутск')
        bot.send_message(message.chat.id, 'Напишите или выберите название города', reply_markup=keyboard)
        start_check += 1
    elif text == "🇺🇸English" and start_check == 1:
        bot_lang = 'eng'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('Moscow', 'Yakutsk')
        bot.send_message(message.chat.id, 'Write or select the name of the city', reply_markup=keyboard)
        start_check += 1
    elif text == "🇷🇺Русский":
        bot_lang = 'ru'
        data = getData(bot_city_ru, bot_lang, appid)
        data5 = getData5(bot_city_ru, bot_lang, appid)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('🌞Погода сейчас')
        keyboard.row('⛅На завтра', '🛰️5 дней')
        keyboard.row('⚙Настройки')
        bot.send_message(message.chat.id, 'Вы поменяли язык на 🇷🇺Русский\nВот список того, что я умею:', reply_markup=keyboard)
    elif text == "🇺🇸English":
        bot_lang = 'eng'
        data = getData(bot_city_eng, bot_lang, appid)
        data5 = getData5(bot_city_eng, bot_lang, appid)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('🌞Weather right now')
        keyboard.row('⛅For tomorrow', '🛰️For 5 days')
        keyboard.row('⚙Settings')
        bot.send_message(message.chat.id, 'You have changed language to the 🇺🇸English\nHere is a list of what I can do:', reply_markup=keyboard)
    elif text.startswith('⚙'):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if bot_lang == 'ru':
            keyboard.row('🗣️Поменять язык', '🗺️Поменять город', '↩️Назад')
            bot.send_message(message.chat.id, 'Выберите нужные вам настройки', reply_markup=keyboard)
        else:
            keyboard.row('🗣️Change language', '🗺️Change city', '↩️Return')
            bot.send_message(message.chat.id, 'Select the settings you need', reply_markup=keyboard)
    elif text.startswith('🗣️'):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if bot_lang == 'ru':
            keyboard.row('🇷🇺Русский', '🇺🇸English', '🔙Отмена')
            bot.send_message(message.chat.id, 'Выберите язык', reply_markup=keyboard)
        else:
            keyboard.row('🇷🇺Русский', '🇺🇸English', '🔙Back')
            bot.send_message(message.chat.id, 'Select language', reply_markup=keyboard)
    elif text.startswith("🗺️"):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if bot_lang == 'ru':
            keyboard.row('🏙️Последние города', '🔙Отмена')
            bot.send_message(message.chat.id, 'Напишите название города, или выберите из последних', reply_markup=keyboard)
        else:
            keyboard.row('🏙️Last cities', '🔙Back')
            bot.send_message(message.chat.id, 'Write the name of the city or select from previous', reply_markup=keyboard)
    elif text.startswith('🏙️'):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if bot_lang == 'ru':
            try:
                if(last_city_ru != last_city2_ru):
                    keyboard.row(last_city_ru)
                    keyboard.row(last_city2_ru)
                else:
                    keyboard.row(last_city_ru)
                keyboard.row('🔙Отмена')
                bot.send_message(message.chat.id, 'Ваш последний город: ' + last_city_ru, reply_markup=keyboard)
            except:
                bot.send_message(message.chat.id, 'Вы еще не указывали свое местоположение')
        else:
            try:
                if(last_city_eng != last_city2_eng):
                    keyboard.row(last_city_eng)
                    keyboard.row(last_city2_eng)
                else:
                    keyboard.row(last_city_eng)
                keyboard.row('🔙Back')
                bot.send_message(message.chat.id, 'Your last city: ' + last_city_eng, reply_markup=keyboard)
            except:
                bot.send_message(message.chat.id, 'You have not selected your location yet')
    elif text.startswith("↩️"):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if bot_lang == 'ru':
            keyboard.row('🌞Погода сейчас')
            keyboard.row('⛅На завтра', '🛰️5 дней')
            keyboard.row('⚙Настройки')
            bot.send_message(message.chat.id, 'Вот список того, что я умею:', reply_markup=keyboard)
        else:
            keyboard.row('🌞Weather right now')
            keyboard.row('⛅For tomorrow', '🛰️For 5 days')
            keyboard.row('⚙Settings')
            bot.send_message(message.chat.id, 'Here is a list of what I can do:', reply_markup=keyboard)
    elif text.startswith('🔙'):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if bot_lang == 'ru':
            keyboard.row('🗣️Поменять язык', '🗺️Поменять город', '↩️Назад')
            bot.send_message(message.chat.id, 'Выберите нужные вам настройки', reply_markup=keyboard)
        else:
            keyboard.row('🗣️Change language', '🗺️Change city', '↩️Return')
            bot.send_message(message.chat.id, 'Select the settings you need', reply_markup=keyboard)
    elif text.startswith("🌞"):
        if bot_lang == 'ru':
            try:
                weather = "Погода сейчас: "
                main = data['main']
                for description in data['weather']:
                    weather += str(description['description']) + '\n'
                temp = '🌡️Температура: ' + str(main['temp']) + '°C, чувствуется как ' + str(main['feels_like']) + '°C\n'
                wind = '💨Ветер: ' + str(data['wind']['speed']) + ' м/c\n'
                visibility = '👁️Видимость: ' + str(data['visibility']) + ' м\n'
                clouds = '☁Облачность: ' + ' ' + str(data['clouds']['all']) + '%\n'
                humidity = '💦Влажность: ' + str(main['humidity']) + '%\n'
                pressure = '🗜Давление: ' + str(main['pressure'] * 0.75) + ' мм рт. ст.\n'
                weather += temp + wind + visibility + clouds + humidity + pressure
                bot.send_message(message.chat.id, weather)
            except:
                bot.send_message(message.chat.id, 'Укажите все данные в настройках')
        else:
            try:
                weather = "Weather right now: "
                main = data['main']
                for description in data['weather']:
                    weather += str(description['description']) + '\n'
                temp = '🌡️Temperature: ' + str(main['temp']) + '°C, feels like ' + str(main['feels_like']) + '°C\n'
                wind = '💨Wind: ' + str(data['wind']['speed']) + ' m/s\n'
                visibility = '👁️Visibility: ' + str(data['visibility']) + ' m\n'
                clouds = '☁Clouds: ' + ' ' + str(data['clouds']['all']) + '%\n'
                humidity = '💦Humidity: ' + str(main['humidity']) + '%\n'
                pressure = '🗜Pressure: ' + str(main['pressure'] * 0.75) + ' mm Hg.\n'
                weather += temp + wind + visibility + clouds + humidity + pressure
                bot.send_message(message.chat.id, weather)
            except:
                bot.send_message(message.chat.id, 'Select all the data in the settings')
    elif text.startswith("⛅"):
        if bot_lang == 'ru':
            forecast = 'Погода на завтра '
        else:
            forecast = 'Weather for tomorrow '
        day_check = 0
        for wea in data5['list']:
            time1 = time.gmtime(wea['dt'])
            dt = wea['dt_txt']
            main = wea['main']
            if day_check == 1 and dt[12] == '0':
                break
            elif dt[12] == '0':
                forecast += '(' + time.strftime('%d.%m', time1) + ')\n'
                day_check += 1
            if day_check == 1:
                forecast += time.strftime('%H:%M', time1) + ' '
                for weather in wea['weather']:
                    forecast += str(weather['description']) + '\n'
                forecast += '🌡️' + str(main['temp']) + '°C'
                if bot_lang == 'ru':
                    forecast += '  💨' + str(wea['wind']['speed']) + ' м/c' + '\n\n'
                else:
                    forecast += '  💨' + str(wea['wind']['speed']) + ' m/s' + '\n\n'
        bot.send_message(message.chat.id, forecast)

    elif text.startswith("🛰️"):
        if bot_lang == 'ru':
            forecast = 'Погода на 5 дней\n'
            for wea in data5['list']:
                time5 = time.gmtime(wea['dt'])
                dt = wea['dt_txt']
                main = wea['main']
                if dt[12] == '0':
                    forecast += time.strftime('%d.%m.', time5)
                if dt[12] == '6':
                    f_morning = '🌄Утро: '
                    for weather in wea['weather']:
                        f_morning += str(weather['description']) + '\n'
                    f_morning += '🌡️' + str(main['temp']) + '°C'
                    f_morning += '  💨' + str(wea['wind']['speed']) + ' м/c'
                    forecast += f_morning
                if dt[12] == '2':
                    f_day = '☀День: '
                    for weather in wea['weather']:
                        f_day += str(weather['description']) + '\n'
                    f_day += '🌡️' + str(main['temp']) + '°C'
                    f_day += '  💨' + str(wea['wind']['speed']) + ' м/c'
                    forecast += f_day
                if dt[12] == '8':
                    f_evening = '🌃Вечер: '
                    for weather in wea['weather']:
                        f_evening += str(weather['description']) + '\n'
                    f_evening += '🌡️' + str(main['temp']) + '°C'
                    f_evening += '  💨' + str(wea['wind']['speed']) + ' м/c'
                    forecast += f_evening
                forecast += '\n'
            bot.send_message(message.chat.id, forecast)
        else:
            forecast = 'Weather for 5 days\n'
            for wea in data5['list']:
                time5 = time.gmtime(wea['dt'])
                dt = wea['dt_txt']
                main = wea['main']
                if dt[12] == '0':
                    forecast += time.strftime('%d.%m.', time5)
                if dt[12] == '6':
                    f_morning = '🌄Morning: '
                    for weather in wea['weather']:
                        f_morning += str(weather['description']) + '\n'
                    f_morning += '🌡️' + str(main['temp']) + '°C'
                    f_morning += '  💨' + str(wea['wind']['speed']) + ' m/s'
                    forecast += f_morning
                if dt[12] == '2':
                    f_day = '☀Afternoon: '
                    for weather in wea['weather']:
                        f_day += str(weather['description']) + '\n'
                    f_day += '🌡️' + str(main['temp']) + '°C'
                    f_day += '  💨' + str(wea['wind']['speed']) + ' m/s'
                    forecast += f_day
                if dt[12] == '8':
                    f_evening = '🌃Evening: '
                    for weather in wea['weather']:
                        f_evening += str(weather['description']) + '\n'
                    f_evening += '🌡️' + str(main['temp']) + '°C'
                    f_evening += '  💨' + str(wea['wind']['speed']) + ' m/s'
                    forecast += f_evening
                forecast += '\n'
            bot.send_message(message.chat.id, forecast)

    elif start_check != 1:
        if getData(text, bot_lang, appid) == {'cod': '404', 'message': 'city not found'}:
            if bot_lang == 'ru':
                bot.send_message(message.chat.id, 'Извините, я Вас не понял')
            else:
                bot.send_message(message.chat.id, "I'm sorry, I don't understand you")
        else:
            data = getData(text, bot_lang, appid)
            data5 = getData5(text, bot_lang, appid)
            bot_city_ru = getData(text, 'ru', appid)['name']
            try:
                last_city2_ru = last_city_ru
            except:
                last_city2_ru = ''
            last_city_ru = bot_city_ru
            bot_city_eng = getData(text, 'eng', appid)['name']
            try:
                last_city2_eng = last_city_eng
            except:
                last_city2_eng = ''
            last_city_eng = bot_city_eng
            if bot_lang == 'ru':
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.row('🌞Погода сейчас')
                keyboard.row('⛅На завтра', '🛰️5 дней')
                keyboard.row('⚙Настройки')
                bot.send_message(message.chat.id, 'Вы выбрали город: ' + bot_city_ru + '\nВот список того, что я умею:', reply_markup=keyboard)
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.row('🌞Weather right now')
                keyboard.row('⛅For tomorrow', '🛰️For 5 days')
                keyboard.row('⚙Settings')
                bot.send_message(message.chat.id, 'You have selected a city: ' + bot_city_eng + '\nHere is a list of what I can do:', reply_markup=keyboard)

bot.polling(none_stop=True)

