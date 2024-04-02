from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
import datetime
import telebot
import itertools

# Alfabeto italiano
alfabeto = 'abcdefghijklmnopqrstuvwxyz'

# Genera tutte le combinazioni di tre lettere
combinazioni = list(itertools.product(alfabeto, repeat=2))

setMatch = set()

bot = telebot.TeleBot("6961169177:AAEuuMd6FiSVpUBz21-4uPfiNpY_-K13_5s")

# instantiate driver
service = Service()
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

# load website
urlGen = 'https://www.ninjabet.it/dutcher?data-a=' + (datetime.date.today() + datetime.timedelta(days=4)).strftime('%Y-%m-%d') + '&combinazioni=2&scommessa1=1,X,2,Goal,No%20Goal,1x%20-%20DC,x2%20-%20DC,12%20-%20DC,Pari,Dispari,Rigore%20Si,Rigore%20No,Under%200.5,Over%200.5,Under%201.5,Over%201.5,Under%202.5,Over%202.5,Under%203.5,Over%203.5,Under%204.5,Over%204.5,Under%205.5,Over%205.5,Under%206.5,Over%206.5&sport=Calcio&book1=888sport,Admiral,Bet365,Betaland,Betclic,Betfairsportbook,Betflagsportbook,Betic,Betman,Better,Betway,Bwin,Casinomania,Chancebet,Domusbet,E-play24,Eurobet,Giobet,Giocodigitale,Goldbet,Leovegas,Marathonbet,Netbet,Newgioco,Novibet,Olybet,Pinnacle,Pinterbet,Planetwin365,Pokerstarssport,Quigioco,Scommettendo,Sisal,Stanleybet,Starcasino,Starvegas,Totowinbet,Unibet,Williamhill,Wintoto&book2=888sport,Admiral,Bet365,Betaland,Betclic,Betfairsportbook,Betflagsportbook,Betic,Betman,Better,Betway,Bwin,Casinomania,Chancebet,Domusbet,E-play24,Eurobet,Giobet,Giocodigitale,Goldbet,Leovegas,Marathonbet,Netbet,Newgioco,Novibet,Olybet,Pinnacle,Pinterbet,Planetwin365,Pokerstarssport,Quigioco,Scommettendo,Sisal,Stanleybet,Starcasino,Starvegas,Totowinbet,Unibet,Wintoto'

js_code = """
return document.getElementsByClassName('hCenter back');
"""



def convert_unicode_to_latin(text):
    # Define a regular expression pattern to match Unicode escape sequences
    pattern = re.compile(r'\\u([0-9a-fA-F]{4})')

    # Define a function to replace each match with its corresponding Latin capital letter
    def replace(match):
        return chr(int(match.group(1), 16)).upper()

    # Use the sub() method to replace all matches in the text
    return pattern.sub(replace, text)


def callDutcher(url):
    driver.get(url)
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.SHIFT + 'i')
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'hCenter.back')))
    except:
        return None
    elements = driver.execute_script(js_code)
    return elements


def adaptMatch(triLet):
    url = 'https://www.ninjabet.it/get_events.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.ninjabet.it',
        'Referer': 'https://www.ninjabet.it/dutcher',
        'Cookie': 'cf_clearance=2bkOoNcLOvOY_.ZaasgdQN3FTMFrQzb8wE26IJPQMiA-1709912482-1.0.1.1-EA15fCgtDTEdHVrq6qTHSI7oTv4jHcFBwRV7yQX59LfEQLWqK9YdxooAmYHjACRA0oP7pDhYNr2T.HrrN41sow; _ga_7X9Y759NT3=GS1.1.1709912481.1.0.1709912481.60.0.0; _ga=GA1.2.879775430.1709912482; _gid=GA1.2.1316145858.1709912483; _uetsid=50c27410dd6211ee8835652ed72dd060; _uetvid=50c29ad0dd6211ee928191a508364d4a; _hjSessionUser_2824700=eyJpZCI6Ijg2NzFhYmEwLWEyNGYtNTk3NS1iNTViLTQzNzUzMmUwOWUzNSIsImNyZWF0ZWQiOjE3MDk5MTI0ODI4MzAsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_2824700=eyJpZCI6IjlhZTMyYTZlLWUzNzEtNDUzNS1hMzk2LTA3ODU5NGUxZGRhMSIsImMiOjE3MDk5MTI0ODI4MzEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }
    try:
        data = {
            'name': triLet,
        }
    except:
        print('')

    response = requests.post(url, headers=headers, data=data)
    return response.text.split('"')


def checkMatch(elem1, elem2, diff):
    url2 = 'https://www.ninjabet.it/dutcher_get_data_copy_max2.php'
    #for combinazione in combinazioni:
    for i in range(0, len(combinazioni)):
        #if combinazioni[i][0] != combinazioni[i][1] or combinazioni[i][2] != combinazioni[i][1] or combinazioni[i][2] != combinazioni[i][0]:
            comb = combinazioni[i]
            aux = adaptMatch(''.join(combinazioni[i]))
            if len(aux) > 1:
                print('c')
                for i in range(3, len(aux), 8):
                    if aux[i].find(' v ') == -1 or aux[i].find(',') != -1 or aux[i] in setMatch:
                        continue
                    setMatch.add(aux[i])
                    match = convert_unicode_to_latin(aux[i])
                    Id = aux[i + 4]
                    headers = {
                        'Host': 'www.ninjabet.it',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Origin': 'https://www.ninjabet.it',
                        'Connection': 'keep-alive',
                        'Referer': 'https://www.ninjabet.it/dutcher?' + 'partita=' + match,
                        'Cookie': 'cf_clearance=2bkOoNcLOvOY_.ZaasgdQN3FTMFrQzb8wE26IJPQMiA-1709912482-1.0.1.1-EA15fCgtDTEdHVrq6qTHSI7oTv4jHcFBwRV7yQX59LfEQLWqK9YdxooAmYHjACRA0oP7pDhYNr2T.HrrN41sow; _ga_7X9Y759NT3=GS1.1.1710009141.2.0.1710009141.60.0.0; _ga=GA1.2.879775430.1709912482; _uetvid=50c29ad0dd6211ee928191a508364d4a; _hjSessionUser_2824700=eyJpZCI6Ijg2NzFhYmEwLWEyNGYtNTk3NS1iNTViLTQzNzUzMmUwOWUzNSIsImNyZWF0ZWQiOjE3MDk5MTI0ODI4MzAsImV4aXN0aW5nIjpmYWxzZX0=',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin'
                    }

                    data = {
                        "bf_comm": "0.045",
                        "bg_comm": "0.05",
                        "name[]": Id,
                        "refund": "100",
                        "back_stake2": "100",
                        "back_stake": "100",
                        "filterbookies": "",
                        "filterbookies2": "",
                        "filterbookies3": "",
                        "bookies": "1,2,3,4,5,6,7,9,11,14,15,16,19,20,24,27,28,30,32,33,34,35,36,37,38,39,40,41,44,50,52,53,54,56,57,59,60,61,62,63,64,101,102",
                        "rating-from": "",
                        "rating-to": "",
                        "odds-from": "",
                        "odds-to": "",
                        "sort-column": "4",
                        "sort-direction": "desc",
                        "offset": "0",
                        "date-from": "",
                        "date-to": "",
                        "sport": "",
                        "tz": "-60",
                        "bet-type": "",
                        "combinazioni": "tutti",
                        "book1": "",
                        "book2": "",
                        "game_play": "1"
                    }

                    try:
                        response2 = requests.post(url2, headers=headers, data=data)
                        text1 = response2.text
                    except:
                        bot.send_message("365637666", match[0] + ' ' + match[1] + ' ,maybe')
                        continue

                    tmp1 = text1.split(':')
                    aux1 = '"' + str(elem1) + '"'
                    aux2 = '"' + str(elem2) + '"'
                    countBet = 11

                    while countBet < len(tmp1):
                        bet1 = tmp1[countBet].split(',')[0]
                        bet2 = tmp1[countBet + 1].split(',')[0]
                        if bet1 == aux1 and bet2 == aux2:
                            bot.send_message("365637666", match + ', percentage: ' + str(diff * 150))
                            #driver.quit()
                            #exit()
                        countBet += 35


while True:
    # get the entire website content
    setMatch = set()
    listElements = callDutcher(urlGen)
    try:
        elem1 = listElements[0].text
        elem2 = listElements[1].text
    except:
        continue
    if elem1 == '' or elem2 == '': continue
    sum = 1 / float(elem1) + 1 / float(elem2)
    diff = (1 - sum) * 2
    if diff >= 0.005:
        checkMatch(elem1, elem2, diff)
        bot.send_message("365637666", 'finish')
