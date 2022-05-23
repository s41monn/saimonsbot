from pycoingecko import CoinGeckoAPI
import datetime
import itertools
from forex_python.converter import CurrencyRates
import aiogram.utils.markdown as md
import requests
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types, Bot
from aiogram.dispatcher.filters import state, Text
# from aiogram.types import ReplyKeyboardRemove
import COVID19Py
from bs4 import BeautifulSoup
import markup as nav
from config import TOKEN, WEATHER_API_KEY
from states import WeatherStates, HoroscopeStates, CryptoStates, CurrencyStates, MemeStates, DownloaderStates
import os
from moviepy.editor import *
import subprocess
import you_get
from moviepy import *

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# --- mainMenu ---
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Oh!Hello there!!You can ask me anything you want :)", reply_markup=nav.mainMenu)


@dp.message_handler(commands=["back"], state='*')
async def main_menu(message: types.Message):
    try:
        await state.default_state.set()
    except:
        print("couldnt return to default state")
    await message.reply("Back to Main menu", reply_markup=nav.mainMenu)


# --- Weather scripts ---

@dp.message_handler(Text(equals='Weather'))
async def start_command(message: types.Message):
    await message.reply("type a city name")
    await WeatherStates.first()


@dp.message_handler(state=WeatherStates.weatherState1)
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Clear \U00002600",
        "Clouds": "Cloudy \U00002601",
        "Rain": "Rainy \U00002614",
        "Drizzle": "Drizzle \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_API_KEY}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "look out the window, i cant figure out whats going on out there"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Current weather: {city}\nTemperature: {cur_weather}C° {wd}\n"
                            f"Humidity: {humidity}%\nPressure: {pressure} mmHg\nWind: {wind} m/s\n"
                            f"Sunrise time: {sunrise_timestamp}\nSunset time: {sunset_timestamp}\nLength of the day: {length_of_the_day}\n"
                            f"***Have a good day!***", reply_markup=nav.multMenu
                            )



    except:
        await message.reply("\U00002620 city name is incorrect, try again \U00002620")
        # TODO: make a smaller scope of exception / bugfix


# --- Horoscope scripts ---

@dp.message_handler(Text(equals='Horoscope'), state=None)
async def get_Horoscope(message: types.Message):
    await message.answer('enter your sign: ', reply_markup=nav.horoscopeMenu1)

    await HoroscopeStates.first()


@dp.message_handler(state=HoroscopeStates.horoscopeState1)
async def get_Horoscope_S1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sign'] = message.text
    await message.answer('Please enter the horoscope day(today, tomorrow or yesterday):  ',
                         reply_markup=nav.horoscopeMenu2)

    await HoroscopeStates.horoscopeState2.set()


@dp.message_handler(state=HoroscopeStates.horoscopeState2)
async def get_Horoscope_S1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['day'] = message.text

    # get parameters from user

    # get their sign
    # (aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius and pisces.)

    sign = md.bold(data['sign'])

    # get the horoscope day (today,tomorrow or yesterday)

    day = md.bold(data['day'])

    # parameters for the HTTP request

    params = (

        ('sign', sign.replace('*', '')),
        ('day', day.replace('*', ''))

    )
    # make the request
    print(params)
    response = requests.post('https://aztro.sameerkumar.website', params=params)
    # print(response.json())
    json = response.json()

    current_date = json.get('current_date')
    description = json.get('description')
    compatibility = json.get('compatibility')
    mood = json.get('mood')
    color = json.get('color')
    lucky_number = json.get('lucky_number')
    lucky_time = json.get('lucky_time')

    print("\nHoroscope for", json.get('current_date'), "\n")
    print(json.get('description'), "\n")
    print("Compatibility:", json.get('compatibility'))
    print("Mood:", json.get('mood'))
    print("Color:", json.get('color'))
    print("Lucky number:", json.get('lucky_number'))
    print("Lucky time:", json.get('lucky_time'), "\n")

    await message.reply(f"Horoscope for {current_date}\n"
                        f"{description} \n"
                        f"Compatibility: {compatibility}\n"
                        f"Mood:{mood}\n"
                        f"Color:{color}\n"
                        f"Lucky number:{lucky_number}\n"
                        f"Lucky time: {lucky_time}\n", reply_markup=nav.multMenu)


# --- covid stat ---

@dp.message_handler(Text(equals='Covid Statistics'))
async def covid_command(message: types.Message):
    covid19 = COVID19Py.COVID19()
    location = covid19.getLocationByCountryCode("KG")
    country = location[0].get('country')
    country_pop = location[0].get('country_population')
    confirmed = location[0].get('latest').get('confirmed')
    deaths = location[0].get('latest').get('deaths')
    recovered = location[0].get('latest').get('recovered')

    last_updated = location[0].get('last_updated')
    print(country, country_pop, confirmed, deaths, recovered, last_updated)

    await message.reply(f'country: {country} \n'
                        f'country population: {country_pop}\n'
                        f'number of new confirmed cases: {confirmed} \n'
                        f'deaths: {deaths} \n'
                        f'recovered: {recovered} \n'
                        f'last updated on: {last_updated}'
                        , reply_markup=nav.multMenu)


# --- Crypto prices ---
cg = CoinGeckoAPI()


@dp.message_handler(Text(equals='Crypto prices'), state=None)
async def get_crypto(message: types.Message):
    await message.answer('choose an exchange rate: ', reply_markup=nav.cryptoMenu)
    await CryptoStates.first()


@dp.message_handler(state=CryptoStates.cryptoState1)
async def get_crypto_S1(message: types.Message, state: FSMContext):
    cr = message.text
    if cr == 'BTC/USD':
        unfilprice = cg.get_price(ids='bitcoin', vs_currencies='usd')
        price = unfilprice.get('bitcoin').get('usd')
        print(price)
        await message.reply(f'BTC/USD: {price} $', reply_markup=nav.multMenu)
    elif cr == 'ETH/USD':
        # try:
        unfilprice = cg.get_price(ids='ethereum', vs_currencies='usd')
        print(unfilprice)
        price = unfilprice.get('ethereum').get('usd')
        print(price)
        await message.reply(f'ETH/USD: {price} $', reply_markup=nav.multMenu)
        # except:
        #     await message.reply('servers are currently unavailable', reply_markup=nav.multMenu)
    elif cr == 'LTC/USD':
        unfilprice = cg.get_price(ids='litecoin', vs_currencies='usd')
        price = unfilprice.get('litecoin').get('usd')
        await message.reply(f'LTC/USD: {price} $', reply_markup=nav.multMenu)
        print(price)


# # --- currency exchange ---
# @dp.message_handler(Text(equals='Currency exchange prices'), state=None)
# async def get_currency(message: types.Message):
#     await message.answer('choose an exchange rate: ', reply_markup=nav.currencyMenu)
#     await CurrencyStates.first()
#
#
# @dp.message_handler(state=CurrencyStates.currencyState1)
# async def get_currency_S1(message: types.Message):
#     ce = message.text
#     c = CurrencyRates
#     if ce == 'USD/KGS':
#         DOLLAR_SOM = (
#             'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%81%D0%BE%D0%BC%D1%83&oq=%D0%9A%D0%A3%D0%A0%D0%A1+&aqs=chrome.1.69i57j0i512l4j69i61l2j69i60.5681j1j4&sourceid=chrome&ie=UTF-8')
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
#         full_page = requests.get(DOLLAR_SOM, headers=headers)
#         soup = BeautifulSoup(full_page.content, 'html.parser')
#         convert = soup.findAll("span", {"class": "DFlde", "class": "SwHCTb", "data-precision": 2})
#         print(convert)
#         print("Dollar rate " + convert[0].text)


# --- meme ---
@dp.message_handler(Text(equals='Random meme'), state=None)
async def get_memes(message: types.Message):
    await message.answer('select a subreddit: ', reply_markup=nav.memeMenu)
    await MemeStates.first()


@dp.message_handler(state=MemeStates.memeState)
async def get_memes_S1(message: types.Message):
    res = message.text
    if res == 'Wholesome meme':
        r = requests.get('https://meme-api.herokuapp.com/gimme/wholesomememes/')
    elif res == 'Regular meme':
        r = requests.get('https://meme-api.herokuapp.com/gimme/dankmemes/')

    if r.status_code == 200:
        data = r.json()
        url = data.get('url')
        await message.reply(url, reply_markup=nav.multMenu)


# --- youtube downloader ---
@dp.message_handler(Text(equals='Youtube downloader'))
async def get_youtube(message: types.Message):
    await message.answer('select a format: ', reply_markup=nav.downloaderMenu)
    await DownloaderStates.first()


@dp.message_handler(state=DownloaderStates.downloaderState1)
async def get_youtube_S1(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['format'] = message.text
    await message.answer('please send a link to a video ')
    await DownloaderStates.next()


@dp.message_handler(state=DownloaderStates.downloaderState2)
async def get_youtube_S2(message: types.Message, state=FSMContext):
    user_id = message.from_user.id
    url = message.text
    async with state.proxy() as data:
        data['url'] = message.text
    format1 = md.bold(data['format']).replace('*', '')
    url1 = md.bold(data['url']).replace('*', '')
    print(format1, url1, url)
    if format1 == 'Download mp3':
        await message.answer('not implemented yet)')
        # command = f'you-get -o D:\\tgmedia\\ --itag=18 {url}'
        # test = os.system(f'you-get -o D:\\tgmedia\\ --itag=18 {url}')
        # file_path = os.listdir('D:\\tgmedia\\')[0]
        # mp3_file = file_path.replace('.mp4', '.mp3')
        # videoclip = VideoFileClip(file_path)
        # audioclip = videoclip.audio
        # audioclip.write_audiofile(mp3_file)
        # os.remove(f"D:\\tgmedia\\{file_path}")
        # audioclip.close()
        # videoclip.close()
        # srt_file_path = os.listdir('D:\\tgmedia\\')[1]
        # print(file_path)
        # await bot.send_audio(message.from_user.id, {mp3_file}, 'rb')
        #
        # os.remove(f"D:\\tgmedia\\{mp3_file}")
        # os.remove(f"D:\\tgmedia\\{srt_file_path}")

        # legacy youtube_dl implementation (not functional)

        # ydl_opts = {
        #     'format': 'bestaudio/best',
        #     'forcefilename': 'True',
        #     'postprocessors': [{
        #         'key': 'FFmpegExtractAudio',
        #         'preferredcodec': 'mp3',
        #         'preferredquality': '192',
        #     }],
        # }
        # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #
        #     test = subprocess.Popen(
        #         ['youtube-dl', '-i', '--extract-audio', '--audio-format mp3', '--audio-quality 0',
        #          'https://www.youtube.com/watch?v=dQw4w9WgXcQ'])
        # ydl.download([url])
        # info_dict = ydl.extract_info(url, download=False)
        # print(info_dict)
        # file_name = info_dict.get('title', None)
        # print(file_name)
        # await bot.send_audio(message.from_user.id, f"{file_name}.mp3", performer="Performer", title=f"{file_name}")
        #
        # os.remove(f"D:\\tgmedia\\{file_name}.mp3")

    # legacy mp3 implementation, not fully functional

    # if format1 == 'Download mp3':
    #     youtube = pytube.YouTube(url)
    #     print('got the url')
    #     video = youtube.streams.filter(only_audio=True).first()
    #     print('got the stream')
    #     video.download('D:\\tgmedia')
    #     print('download complete')
    #     file_name = video.title
    #     time.sleep(10)
    #     videoclip = VideoFileClip(video)
    #     audioclip = videoclip.audio
    #     audioclip.write_audiofile(file_name)
    #     await bot.send_audio(message.from_user.id, f"{file_name}.mp3", 'rb')

    elif format1 == 'Download video':

        # file_name = os.system('you-get --json -o D:\\tgmedia\\ --itag=18 https://www.youtube.com/watch?v=MvQ5ynbwfHM')
        await message.answer('please wait a moment (it might take a couple of minutes)')
        command = f'you-get -o D:\\tgmedia\\ --itag=18 {url}'
        test = os.system(f'you-get -o D:\\tgmedia\\ --itag=18 {url}')
        file_path = os.listdir('D:\\tgmedia\\')[0]
        try:
            srt_file_path = os.listdir('D:\\tgmedia\\')[1]
            os.remove(f"D:\\tgmedia\\{srt_file_path}")
        except:
            print('no sart file')
        print(file_path)
        await bot.send_video(chat_id=user_id,
                             video=open(f"D:\\tgmedia\\{file_path}", 'rb'),
                             reply_markup=nav.multMenu)

        os.remove(f"D:\\tgmedia\\{file_path}")

        # youtube = pytube.YouTube(url)
        # print('got the url')
        # video = youtube.streams.filter(progressive=True).get_highest_resolution()
        # print('got the stream')
        # video.download('D:\\tgmedia')
        # print('download complete')
        # file_name = video.title
        # time.sleep(10)
        # await bot.send_video(chat_id=user_id,
        #                      video=open(f"D:\\tgmedia\\{file_name}.mp4", 'rb'),
        #                      reply_markup=nav.multMenu)
