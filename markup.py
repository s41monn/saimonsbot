from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Main Menu --
btnWeather = KeyboardButton('Weather')
btnHoroscope = KeyboardButton('Horoscope')
btnCovidStat = KeyboardButton('Covid Statistics')
btnCrypto = KeyboardButton('Crypto prices')
btnMeme = KeyboardButton('Random meme')
btnDownloader = KeyboardButton('Youtube downloader')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnWeather, btnHoroscope, btnCovidStat,
                                                                                 btnCrypto, btnMeme,
                                                                                 btnDownloader)

# --- multipurpose menu ---
btnBack = KeyboardButton('/back')
multMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnBack)

# --- Horoscope inline menu ---
# (aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius and pisces.)

btnAries = KeyboardButton('aries')
btnTaurus = KeyboardButton('taurus')
btnGemini = KeyboardButton('gemini')
btnCancer = KeyboardButton('cancer')
btnLeo = KeyboardButton('leo')
btnVirgo = KeyboardButton('virgo')
btnLibra = KeyboardButton('libra')
btnScorpio = KeyboardButton('scorpio')
btnSagittarius = KeyboardButton('sagittarius')
btnCapricorn = KeyboardButton('capricorn')
btnAquarius = KeyboardButton('aquarius')
btnPisces = KeyboardButton('pisces')
horoscopeMenu1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnAries, btnTaurus, btnGemini,
                                                                                       btnCancer,
                                                                                       btnLeo, btnVirgo, btnLibra,
                                                                                       btnScorpio,
                                                                                       btnSagittarius, btnCapricorn,
                                                                                       btnAquarius,
                                                                                       btnPisces)

btnYesterday = KeyboardButton('yesterday')
btnToday = KeyboardButton('today')
btnTomorrow = KeyboardButton('tomorrow')
horoscopeMenu2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnYesterday, btnToday,
                                                                                       btnTomorrow)

# --- Crypto menu ---
btnBtctoUsd = KeyboardButton('BTC/USD')
btnETHtoUsd = KeyboardButton('ETH/USD')
btnLTCtoUsd = KeyboardButton('LTC/USD')
cryptoMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnBtctoUsd, btnETHtoUsd,
                                                                                   btnLTCtoUsd)

# --- Currency menu ---
btnUSDtoKGS = KeyboardButton('USD/KGS')
btnEURtoKGS = KeyboardButton('EUR/KGS')
btnRUBtoKGS = KeyboardButton('USD/KGS')
btnKGStoUSD = KeyboardButton('KGS/USD')
btnKGStoEUR = KeyboardButton('EUR/USD')
btnKGStoRUB = KeyboardButton('KGS/RUB')
currencyMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnKGStoRUB, btnKGStoUSD,
                                                                                     btnKGStoEUR, btnRUBtoKGS,
                                                                                     btnEURtoKGS, btnUSDtoKGS)

# --- meme menu ---
btnWholesome = KeyboardButton('Wholesome meme')
btnNormal = KeyboardButton('Regular meme')
memeMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnWholesome, btnNormal)

# --- youtube downloader menu ---
btnVideo = KeyboardButton('Download video')
btnAudio = KeyboardButton('Download mp3')
downloaderMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnAudio, btnVideo)
