import requests, json
from sandbox import get_today_str
import pickle
from tqdm.auto import tqdm
def scrape_data():
    url = 'https://auto.ru/-/ajax/desktop/listing/'
    headers = '''
    Host: auto.ru
    Connection: keep-alive
    Content-Length: 90
    x-requested-with: fetch
    x-client-date: 1621148259922
    x-csrf-token: 53b11b57e14caad9a0f6545e1ef9c004344176527b8351c8
    x-page-request-id: 5583f4a5f07cc65d83663e74ff1b70c0
    content-type: application/json
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36
    x-client-app-version: bce8a8244b5
    Accept: */*
    Origin: https://auto.ru
    Sec-Fetch-Site: same-origin
    Sec-Fetch-Mode: same-origin
    Sec-Fetch-Dest: empty
    Referer: https://auto.ru/cars/toyota/all/?has_image=false
    Accept-Encoding: gzip, deflate, br
    Accept-Language: ru,en;q=0.9
    Cookie: _csrf_token=53b11b57e14caad9a0f6545e1ef9c004344176527b8351c8; autoru_sid=a%3Ag60a0bd3b2kqo25taqtiurr1a4b4d51m.80f887a40a36dfb853a77cf7b336d6db%7C1621146939864.604800.JAeqRS8yheUp5PIRxIh1OQ.DUlv-c7QyZSrcTyrXHBBNbK770wzMNBCaY3D8qnxgSc; autoruuid=g60a0bd3b2kqo25taqtiurr1a4b4d51m.80f887a40a36dfb853a77cf7b336d6db; suid=194dd15489105d4ab112cc1abd10309b.ae2f3c36bea592b199755baa130632f9; from=yandex; X-Vertis-DC=vla; yuidlt=1; yandexuid=332162211609488292; my=YwA%3D; gdpr=0; _ym_uid=1621146945736424170; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; _ym_isad=2; gids=; autoru-visits-count=1; autoru-visits-session-unexpired=1; cycada=A3OZrDhunGBqglrPWUvvLndT3sQMgvERWs6+hb0petI=; from_lifetime=1621148256797; _ym_d=1621148256'''

    headers = headers.strip().split('\n')
    headers_dict = {}
    for header in headers:
        key, value = header.split(': ')
        headers_dict[key] = value
    all_offers = []
    for mrk in tqdm(['BMW',
                     'MERCEDES']):
        for _ in tqdm(range(1, 50)):
            try:
                params = {"catalog_filter": [{"mark": mrk}],
                          "section": "all",
                          "page": _}
                response = requests.post(url,
                                         json=params,
                                         headers=headers_dict)
                data = response.json()
                all_offers.extend(data['offers'])

            except:
                continue
        print(mrk, _, len(all_offers))

    with open(f"autoru_proj_data.pkl", 'wb') as f:
        pickle.dump(all_offers, f)
