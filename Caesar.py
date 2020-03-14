import requests
from bs4 import BeautifulSoup

message = 'MHILY LZA ZBHL XBPZXBL MVYABUHL HWWPBZ ' \
          'JSHBKPBZ JHLJBZ KPJABT HYJHUBT LZA ULBAYVU'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def google_count(input_text):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
    }
    r = requests.get("https://www.google.com/search", headers=headers, params={'q': input_text})
    soup = BeautifulSoup(r.text, "lxml")
    res = soup.find(id="result-stats")
    return res.text


for key in range(1, len(LETTERS)):
    translated = ''
    for symbol in message:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)
            num = num - key
            if num < 0:
                num = num + len(LETTERS)
            translated = translated + LETTERS[num]
        else:
            translated = translated + symbol
    count = google_count(translated)
    print(f'key: {key}, text: {translated}, result: {count}')