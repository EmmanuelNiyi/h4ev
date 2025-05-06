import requests


def get_user_forms(username: str) -> dict:
    params = {
        'owner': username,
    }
    response = requests.get('https://api.ona.io/api/v1/forms', params=params)
    response.raise_for_status()
    data = response.json()
    return data


def get_form_submissions(form_id: str) -> dict:
    response = requests.get(f'https://api.ona.io/api/v1/data/{form_id}')
    response.raise_for_status()
    data = response.json()
    return data
