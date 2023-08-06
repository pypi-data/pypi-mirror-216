import requests


def requests_get(url, params, headers):
    return requests.get(url=url, headers=headers, params=params)


def requests_post(url, json, headers):
    return requests.post(url=url, headers=headers, json=json)
