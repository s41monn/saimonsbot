from aiogram.dispatcher.filters.state import StatesGroup, State


# -- weather states ---
class WeatherStates(StatesGroup):
    weatherState1 = State()


# --- Horoscope states ---
class HoroscopeStates(StatesGroup):
    horoscopeState1 = State()
    horoscopeState2 = State()


# --- Crypto states ---

class CryptoStates(StatesGroup):
    cryptoState1 = State()
    cryptoState2 = State()

# --- Currency States ---

class CurrencyStates(StatesGroup):
    currencyState1 = State()
    currencyState2 = State()


# --- Meme States ---
class MemeStates(StatesGroup):
    memeState = State()

# --- downloader states ---
class DownloaderStates(StatesGroup):
    downloaderState1 = State()
    downloaderState2 = State()