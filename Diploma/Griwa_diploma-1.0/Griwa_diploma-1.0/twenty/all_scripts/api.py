import requests
from bs4 import BeautifulSoup


def get_html_data(text, font):
    api = (
        'https://fastapi-text-asciify-npt1siwyq-ganmahmud.vercel.app/asciify/')
    params = dict(text=text, font=font)  # only ASCII symbols

    try:
        response = requests.get(api, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e}')
    except requests.exceptions.RequestException as e:
        print(f'Error occured: {e}')

    else:
        return response


def text_art(text, font):
    html_data = get_html_data(text, font)
    soup = BeautifulSoup(html_data.text, 'lxml')
    output = soup.find('pre', class_='art')

    return output.text
