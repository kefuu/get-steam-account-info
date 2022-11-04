import requests
from bs4 import BeautifulSoup

url_body = 'https://steamid.pro/lookup/'


def get_bans(steam_id):

    try:
        r = requests.get(f'{url_body}{steam_id}')
        soup = BeautifulSoup(r.text, 'html.parser')

        divs_info = soup.find_all('div', class_='col-lg-6 col-12')
        bans_div = divs_info[1]
        bans = bans_div.find('table', class_='rtable rtable-bordered table-fixed table-responsive-flex').find_all('tr')

        bans_info = []

        for ban in bans:
            tds = ban.find_all('td')
            bans_info.append(f"{tds[0].text} : {tds[1].text}")

        return bans_info

    except Exception as ex:
        print(ex)


def get_account_price(steam_id):
    try:
        r = requests.get(f'{url_body}{steam_id}')
        soup = BeautifulSoup(r.text, 'html.parser')

        price = soup.find('span', class_='number-price')

        return price.text

    except Exception as ex:
        print(ex)


def time_played(steam_id):
    try:
        r = requests.get(f'{url_body}{steam_id}')
        soup = BeautifulSoup(r.text, 'html.parser')

        divs_info = soup.find_all('div', class_='col-lg-6 col-12')
        hours_div = divs_info[1]
        hours_info = hours_div.find_all('table', class_='rtable rtable-bordered table-fixed table-responsive-flex')[1]

        hours_played = hours_info.find_all('td')

        return f'Часов наигранно : <b>{hours_played[1].text}</b>'

    except Exception as ex:
        print(ex)


def get_simple(steam_id):
    try:
        r = requests.get(f'{url_body}{steam_id}')
        soup = BeautifulSoup(r.text, 'html.parser')

        info_div = soup.find('div', class_='ml-3')
        mix_info = info_div.find_all('span')

        data = []

        nick = info_div.find('h1', class_='mb-0 text-white').text
        steam_level = mix_info[0].text

        data.append(f'Ник: {nick}')
        data.append(f'Уровень стим: {steam_level}')

        return data

    except Exception as ex:
        print(ex)


def main_func(steam_id):
    message_text = ''

    bans_info = get_bans(steam_id=steam_id)

    message_text += 'Стандартная информация: \n'
    info = get_simple(steam_id=steam_id)
    for item in info:
        message_text += f'<b>{item}</b>\n'

    message_text += "\nБаны аккаунта: \n"
    for ban in bans_info:
        message_text += f'<b>{ban}</b>\n'

    account_price = get_account_price(steam_id=steam_id)
    message_text += f"\nПримерная цена аккаунта: <b>{account_price}</b>\n"

    time = time_played(steam_id=steam_id)
    message_text += time

    return message_text
