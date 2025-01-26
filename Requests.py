import requests

#обработка исключений
from requests.exceptions import HTTPError

for url in ['https://api.github.com', 'https://api.github.com/invalid']:
    try:
        response = requests.get(url)

        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')

# Параметры запроса
response = requests.get('https://api.github.com/search/repositories',
    params={'q': 'requests+language:python'},
)

json_response = response.json()
repository = json_response['items'][0]
print(f'Repository name: {repository["name"]}')
print(f'Repository description: {repository["description"]}')


# Работа с заголовками

response = requests.get('https://api.github.com/search/repositories',
    params={'q': 'requests+language:python'},
    headers={'Accept': 'application/vnd.github.v3.text-match+json'}
)

json_response = response.json()
repository = json_response['items'][0]
print(f'Text matches: {repository["text_matches"]}')


