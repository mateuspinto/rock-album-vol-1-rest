import json
import requests

CFG = json.load(open('config.json'))
SERVER_URL = 'http://' + CFG['HOST'] + ':' + str(CFG['PORT']) + '/'


def is_admin(EMAIL):
    REQUEST = {
        'email': EMAIL
    }

    RESPONSE = requests.post(SERVER_URL + 'user/is_admin/', data=REQUEST).json()

    return not RESPONSE['error']


def login():
    while True:
        REQUEST = {
            'email': input('Digite o seu email: '),
            'password': input('Digite a sua senha: ')
        }

        RESPONSE = requests.post(SERVER_URL + 'user/login/', data=REQUEST).json()

        if RESPONSE['error'] == 1:
            print(f'Erro! {RESPONSE["error_message"]} Tente novamente...\n')
        else:
            return REQUEST['email']


def register():
    while True:
        REQUEST = {
            'email': input('Digite o email a ser cadastrado: '),
            'password': input('Digite a sua senha: ')
        }

        RESPONSE = requests.put(SERVER_URL + 'user/register/', data=REQUEST).json()

        if RESPONSE['error'] == 1:
            print(f'Erro! {RESPONSE["error_message"]} Tente novamente...\n')
        else:
            return REQUEST['email']


def admin__create_giftcard(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'giftcard_key': input('Insira a chave do cartão presente: ')
    }

    RESPONSE = requests.put(SERVER_URL + 'admin/create_giftcard/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def admin__create_stickers(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'sticker_name': input('Insira o nome da figurinha: '),
        'sticker_number': int(input('Insira a quantidade de figurinhas: '))
    }

    RESPONSE = requests.put(SERVER_URL + 'admin/create_stickers/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def admin__draw_lucky_prize(EMAIL):
    REQUEST = {
        'email': EMAIL,
    }

    RESPONSE = requests.put(SERVER_URL + 'admin/draw_lucky_prize/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def admin__op(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'target_email': input('Insira o email a ser tornado administrador: '),
    }

    RESPONSE = requests.put(SERVER_URL + 'admin/op/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def admin__unop(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'target_email': input('Insira o email a ser removido de administrador: '),
    }

    RESPONSE = requests.put(SERVER_URL + 'admin/unop/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def album__get_album(EMAIL):
    REQUEST = {
        'email': EMAIL,
    }

    RESPONSE = requests.post(SERVER_URL + 'album/get_album/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Figurinhas:')
        for sticker in RESPONSE['stickers']:
            print(sticker)


def album__get_free_stickers(EMAIL):
    REQUEST = {
        'email': EMAIL,
    }

    RESPONSE = requests.post(SERVER_URL + 'album/get_free_stickers/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Id - Nome da figurinhas:')
        for sticker in RESPONSE['stickers']:
            print(f'{sticker["id"]} - {sticker["sticker_name"]}')


def album__paste_sticker(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'sticker_id': input('Insira o ID da figurinha: '),
    }

    RESPONSE = requests.put(SERVER_URL + 'album/paste_sticker/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def community_market__buy_sticker(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'sticker_name': input('Insira o nome da figurinha: '),
    }

    RESPONSE = requests.put(SERVER_URL + 'community_market/buy_sticker/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def community_market__get_sticker_price(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'sticker_name': input('Insira o nome da figurinha: '),
    }

    RESPONSE = requests.post(SERVER_URL + 'community_market/get_sticker_price/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print(f'A figurinha custa {RESPONSE["price"]}')


def community_market__get_stickers_waiting_for_sale(EMAIL):
    REQUEST = {
        'email': EMAIL,
    }

    RESPONSE = requests.post(SERVER_URL + 'community_market/get_stickers_waiting_for_sale/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Preço - Nome da figurinhas')
        for sticker in RESPONSE['stickers']:
            print(f'{sticker["price"]} - {sticker["sticker_name"]}')


def community_market__put_sticker_to_sell(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'sticker_id': input('Insira o ID da figurinha: '),
        'price': int(input('Insira o preço (em número inteiro) desejado na figurinha: '))
    }

    RESPONSE = requests.put(SERVER_URL + 'community_market/put_sticker_to_sell/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def user__get_coins(EMAIL):
    REQUEST = {
        'email': EMAIL,
    }

    RESPONSE = requests.post(SERVER_URL + 'user/get_coins/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print(f'Você tem {RESPONSE["coins"]}')


def user__retrieve_giftcard(EMAIL):
    REQUEST = {
        'email': EMAIL,
        'giftcard_key': input('Insira a chave do cartão presente: ')
    }

    RESPONSE = requests.put(SERVER_URL + 'user/retrieve_giftcard/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')


def official_market__buy_sticker_pack(EMAIL):
    REQUEST = {
        'email': EMAIL,
    }

    RESPONSE = requests.put(SERVER_URL + 'official_market/buy_sticker_pack/', data=REQUEST).json()

    if RESPONSE['error'] == 1:
        print(f'Erro! {RESPONSE["error_message"]}')
    else:
        print('Feito!')
