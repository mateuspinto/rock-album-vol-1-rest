from flask import Flask, request, g
import json
import sqlite3

CFG = json.load(open('config.json'))
DATABASE_FILENAME = CFG['SQLITE_FILE']
APP = Flask(__name__)


def get_database():
    DATABASE = getattr(g, '_database', None)
    if DATABASE is None:
        DATABASE = g._database = sqlite3.connect(DATABASE_FILENAME)
    return DATABASE


@APP.teardown_appcontext
def close_connection(_):
    DATABASE = getattr(g, '_database', None)
    if DATABASE is not None:
        DATABASE.close()


def __exist_email_registered():
    DB_CUR = get_database().cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM users WHERE email="{request.form["email"]}"'))[0][0] == 1 else 0


def __exist_giftcard():
    DB_CUR = get_database().cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM giftcards WHERE key="{request.form["giftcard_key"]}"'))[0][0] == 1 else 0


def __exist_sticker():
    DB_CUR = get_database().cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{request.form["sticker_id"]}"'))[0][0] == 1 else 0


def __get_coins():
    DB_CUR = get_database().cursor()
    return int(list(DB_CUR.execute(f'SELECT coins FROM users WHERE email="{request.form["email"]}"'))[0][0])


def __is_this_sticker_model_pasted():
    DB_CUR = get_database().cursor()
    STICKER_NAME = list(DB_CUR.execute(f'SELECT name FROM stickers WHERE id={request.form["sticker_id"]}'))[0][0]
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE name="{STICKER_NAME}" AND owner_email="{request.form["email"]}" AND is_pasted=1'))[0][0] == 1 else 0


def __is_this_sticker_owned_by_the_user():
    DB_CUR = get_database().cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{request.form["sticker_id"]}" AND owner_email="{request.form["email"]}"'))[0][0] == 1 else 0


def __is_this_sticker_waiting_for_sale():
    DB_CUR = get_database().cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{request.form["sticker_id"]}" AND is_for_sale=1'))[0][0] == 1 else 0


@APP.route('/admin/create_giftcard/', methods=['PUT'])
def admin__create_giftcard():
    if __exist_giftcard() == 1:
        return {'error': 1, 'error_message': 'Falha na criação do Giftcard! Já existe um Giftcard com essa chave.'}

    DB_CUR = get_database().cursor()
    DB_CUR.execute(f'INSERT INTO giftcards VALUES ("{request.form["giftcard_key"]}")')
    get_database().commit()
    return {'error': 0}


@APP.route('/admin/create_stickers/', methods=['PUT'])
def admin__create_stickers():
    DB_CUR = get_database().cursor()
    for _ in range(request.form["sticker_number"]):
        DB_CUR.execute(f'INSERT INTO stickers (name, owner_email, is_pasted, is_for_sale, price) VALUES ("{request.form["sticker_name"]}", "", 0, 0, 0)')
    get_database().commit()
    return {'error': 0}


@APP.route('/admin/draw_lucky_prize/', methods=['PUT'])
def admin__draw_lucky_prize():
    DB_CUR = get_database().cursor()
    DB_CUR.execute('UPDATE users SET coins=coins+50 WHERE email=(SELECT email FROM users ORDER BY RANDOM() LIMIT 1)')
    get_database().commit()
    return {'error': 0}


@APP.route('/admin/op/', methods=['PUT'])
def admin__op():
    if __exist_email_registered() == 0:
        return {'error': 1, 'error_message': 'Não é possível tornar esse usuário um administrador! Email não encontrado.'}

    DB_CUR = get_database().cursor()
    DB_CUR.execute(f'UPDATE users SET is_admin = 1 WHERE email="{request.form["target_email"]}"')
    get_database().commit()
    return {'error': 0}


@APP.route('/admin/unop/', methods=['PUT'])
def admin__unop():
    if __exist_email_registered() == 0:
        return {'error': 1, 'error_message': 'Não é possível tornar esse usuário um administrador! Email não encontrado.'}

    DB_CUR = get_database().cursor()
    DB_CUR.execute(f'UPDATE users SET is_admin = 0 WHERE email="{request.form["target_email"]}"')
    get_database().commit()
    return {'error': 0}


@APP.route('/album/get_album/', methods=['POST'])
def album__get_album():
    DB_CUR = get_database().cursor()
    return {'error': 0, 'stickers': [x[0] for x in list(DB_CUR.execute(f'SELECT name FROM stickers WHERE owner_email="{request.form["email"]}" AND is_pasted=1'))]}


@APP.route('/album/get_free_stickers/', methods=['POST'])
def album__get_free_stickers():
    DB_CUR = get_database().cursor()
    return {'error': 0, 'stickers': [{'id': x[0], 'sticker_name': x[1]} for x in list(DB_CUR.execute(f'SELECT id, name FROM stickers WHERE owner_email="{request.form["email"]}" AND is_pasted=0 AND is_for_sale=0'))]}


@APP.route('/album/paste_sticker/', methods=['PUT'])
def album__paste_sticker():
    if __exist_sticker() == 0:
        return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! A figurinha não existe.'}

    if __is_this_sticker_model_pasted() == 1:
        return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! O modelo de figurinha já está colado.'}

    if __is_this_sticker_waiting_for_sale() == 1:
        return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! Ela está na fila para a venda.'}

    if __is_this_sticker_owned_by_the_user() == 0:
        return {'error': 1, 'error_message': 'Erro ao colar figurinha! O usuário não é dono desta figurinha.'}

    DB_CUR = get_database().cursor()
    DB_CUR.execute(f'UPDATE stickers SET is_pasted=1 WHERE id="{request.form["sticker_id"]}"')
    get_database().commit()
    return {'error': 0}


@APP.route('/community_market/buy_sticker/', methods=['PUT'])
def community_market__buy_sticker():
    DB_CUR = get_database().cursor()
    QUERRY_RESULT = list(DB_CUR.execute(f'SELECT id, price FROM stickers WHERE price=(SELECT MIN(price) FROM stickers WHERE name="{request.form["sticker_name"]}" AND is_for_sale=1 AND owner_email!="{request.form["email"]}")'))

    if len(QUERRY_RESULT) == 0:
        return {'error': 0, 'error_message': 'Não foi possível retornar preço da figurinha! Não há nenhuma figurinha desse modelo a venda!'}

    DESIRED_CARD = QUERRY_RESULT[0]

    if __get_coins() < DESIRED_CARD[1]:
        return {'error': 1, 'error_message': 'Não foi possível comprar a figurinha! Usuário sem moedas o suficiente'}

    DB_CUR.execute(f'UPDATE users SET coins=coins-{DESIRED_CARD[1]} WHERE email="{request.form["email"]}"')
    DB_CUR.execute(f'UPDATE stickers SET owner_email="{request.form["email"]}", is_for_sale=0, price=0 WHERE id={DESIRED_CARD[0]}')
    get_database().commit()
    return {'error': 0}


@APP.route('/community_market/get_sticker_price/', methods=['POST'])
def community_market__get_sticker_price():
    DB_CUR = get_database().cursor()
    QUERRY_RESULT = list(DB_CUR.execute(f'SELECT price FROM stickers WHERE price=(SELECT MIN(price) FROM stickers WHERE name="{request.form["sticker_name"]}" AND is_for_sale=1 AND owner_email!="{request.form["email"]}")'))

    if len(QUERRY_RESULT) == 0:
        return {'error': 1, 'error_message': 'Não foi possível retornar preço da figurinha! Não há nenhuma figurinha desse modelo a venda!'}

    return {'error': 0, 'price': QUERRY_RESULT[0][0]}


@APP.route('/community_market/get_stickers_waiting_for_sale/', methods=['POST'])
def community_market__get_stickers_waiting_for_sale():
    DB_CUR = get_database().cursor()
    return {'error': 0, 'stickers': [{'sticker_name': x[0], 'price':x[1]} for x in list(DB_CUR.execute(f'SELECT name, price FROM stickers WHERE owner_email="{request.form["email"]}" AND is_for_sale=1'))]}


@APP.route('/community_market/put_sticker_to_sell/', methods=['PUT'])
def community_market__put_sticker_to_sell():
    if __exist_sticker() == 0:
        return {'error': 1, 'error_message': 'Não é possível vender esta figurinha! A figurinha não existe.'}

    if __is_this_sticker_owned_by_the_user() == 0:
        return {'error': 1, 'error_message': 'Erro ao colocar figurinha a venda! O usuário não é dono desta figurinha.'}

    DB_CUR = get_database().cursor()
    DB_CUR.execute(f'UPDATE stickers SET is_for_sale=1, price={request.form["price"]} WHERE id="{request.form["sticker_id"]}"')
    get_database().commit()
    return {'error': 0}


@APP.route('/user/get_coins/', methods=['POST'])
def user__get_coins():
    return {'error': 0, 'coins': __get_coins()}


@APP.route('/user/is_admin/', methods=['POST'])
def user__is_admin():
    DB_CUR = get_database().cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT is_admin FROM users WHERE email="{request.form["email"]}"')
    if next(QUERY_RESULT)[0] == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Usuário não é administrador!'}


@APP.route('/user/login/', methods=['POST'])
def user__login():
    DB_CUR = get_database().cursor()
    if list(DB_CUR.execute(f'SELECT COUNT(*) FROM users WHERE email="{request.form["email"]}" AND password="{request.form["password"]}"'))[0][0] == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Usuário não encontrado!'}


@APP.route('/user/register/', methods=['PUT'])
def user__register():
    if __exist_email_registered() == 1:
        return {'error': 1, 'error_message': 'Falha no cadastro! Email já está em uso.'}

    DB_CUR = get_database().cursor()
    DB_CUR.execute(f'INSERT INTO users VALUES ("{request.form["email"]}", "{request.form["password"]}", 0, 0)')
    get_database().commit()
    return {'error': 0}


@APP.route('/user/retrieve_giftcard/', methods=['PUT'])
def user__retrieve_giftcard():
    if __exist_giftcard() == 0:
        return {'error': 1, 'error_message': 'Falha no resgate do Giftcard! Não existe um Giftcard com essa chave.'}

    DB_CUR = get_database().cursor()
    DB_CUR.execute(f'UPDATE users SET coins=coins+100 WHERE email="{request.form["email"]}"')
    DB_CUR.execute(f'DELETE FROM giftcards WHERE key="{request.form["giftcard_key"]}"')
    get_database().commit()
    return {'error': 0}


@APP.route('/official_market/buy_sticker_pack/', methods=['PUT'])
def official_market__buy_sticker_pack():
    DB_CUR = get_database().cursor()

    if list(DB_CUR.execute('SELECT COUNT(*) FROM stickers WHERE owner_email=""'))[0][0] < 2:
        return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Não existe figurinhas impressas sem dono suficientes'}

    if __get_coins() < 10:
        return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Você não tem moedas o suficiente!'}

    DB_CUR.execute(f'UPDATE users SET coins=coins-10 WHERE email="{request.form["email"]}"')
    for _ in range(2):
        DB_CUR.execute(f'UPDATE stickers SET owner_email="{request.form["email"]}" WHERE id=(SELECT id FROM stickers WHERE owner_email="" ORDER BY RANDOM() LIMIT 1)')

    get_database().commit()

    return {'error': 0}
