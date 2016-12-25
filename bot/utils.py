# coding: utf-8
import logging
import json
import urllib3
import urllib.parse
import  urllib.request
from . import *
BOT_TOKEN = '308125138:AAFltHYK_wgKgSmxMzgCC60UL7Er1D14jlE'
BASE_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'
START = '/start'
REGISTER_USER = u'Я пользователь'
REGISTER_SHAWARMA_POINT_MAN = u'Я хозяин шаурмы'
SHAWARMA_POINT_LOCATION = u'Локация'
SHAWARMA_POINT_NAME = u'SHAWARMA_POINT_NAME'
SHAWARMA_POINT_TIME_WORK = u'SHAWARMA_POINT_TIME_WORK'
SHAWARMA_POINT_PRICE = u'SHAWARMA_POINT_PRICE'
SHAWARMA_POINT_AWAIT_ORDER = u'SHAWARMA_POINT_AWAIT_ORDER'
USER_WANTS_SHAWARMA = u'Хочу шаверму'

cursor = None


class Button:
    def __init__(self, text, request_location=False, request_contact=False):
        self.text = text
        self.request_location = request_location
        self.request_contact = request_contact


def reply(chat_id, msg=None, parse_mode=None, *keyboard_buttons):
    if msg:
        dct = {
            'chat_id': str(chat_id),
            'text': msg,
            'disable_web_page_preview': 'true',
        }
        if parse_mode:
            dct['parse_mode'] = parse_mode

        if keyboard_buttons:
            dct['reply_markup'] = json.dumps({'keyboard': [[{'text': item.text,
                                                             'request_location': item.request_location,
                                                             'request_contact': item.request_contact}
                                                            for item in keyboard_buttons]]})
        else:
            dct['reply_markup'] = json.dumps({'hide_keyboard': True})
        _data = {}
        for k, v in dct.items():
            _data[k] = v
        logging.debug(json.dumps(_data))
        url = urllib.parse.urlencode(_data)
        resp = urllib.request.urlopen(BASE_URL + 'sendMessage',  url.encode('utf-8'))
    else:
        logging.error('No message')
        resp = None

    logging.info('send response:')
    logging.info(resp)


def start(chat_id):
    mes = u'Привет! Я бот, который помогает найти шаверму.\n ' \
          u'Если ты обычный человек и ищешь шаверму -  нажми "%s". ' \
          u'Если у тебя свой пункт продаже шаурмы - нажми "%s".' % (REGISTER_USER, REGISTER_SHAWARMA_POINT_MAN)
    btn_user = Button(REGISTER_USER)
    btn_point = Button(REGISTER_SHAWARMA_POINT_MAN)
    reply(chat_id, mes, None, *[btn_user, btn_point])


def register_shawarma_point_man(chat_id):
    add_sale_point_owner(cursor, chat_id)
    update_sale_point_owner_stage(cursor, chat_id, REGISTER_SHAWARMA_POINT_MAN)
    mes = u'Пришли свои контактные данные.'
    btn = Button(u'Прислать', request_contact=True)
    reply(chat_id, mes, None,  *[btn])

def register_user(chat_id):
    add_user(cursor, chat_id)
    update_user_stage(cursor, chat_id, REGISTER_USER)
    mes = u'Пришли свои контактные данные.'
    btn = Button(u'Прислать', request_contact=True)
    reply(chat_id, mes, None, *[btn])


def shawarma_point_location(chat_id):
    update_sale_point_owner_stage(cursor, chat_id, SHAWARMA_POINT_LOCATION)
    mes = u'Пришли геопозицию своего пункта продажи шаурмы.'
    btn = Button(u'Геопозиция', request_location=True)
    reply(chat_id, mes, None,  *[btn])


def shawarma_point_name(chat_id):
    update_sale_point_owner_stage(cursor, chat_id, SHAWARMA_POINT_NAME)
    mes = u'Пришли название своей торговой точки'
    reply(chat_id, mes, None)


def shawarma_point_time_work(chat_id):
    update_sale_point_owner_stage(cursor, chat_id, SHAWARMA_POINT_TIME_WORK)
    mes = u'Пришли время работы точки через пробел'
    reply(chat_id, mes, None)


def shawarma_point_price(chat_id):
    update_sale_point_owner_stage(cursor, chat_id, SHAWARMA_POINT_PRICE)
    mes = u'Пришли цену шавермы в рублях'
    reply(chat_id, mes, None)


def shawarma_point_await_order(chat_id):
    update_sale_point_owner_stage(cursor, chat_id, SHAWARMA_POINT_AWAIT_ORDER)
    mes = u'Ожидайте заказа'
    reply(chat_id, mes, None)


def user_can_list_shawarma_points(chat_id):
    update_user_stage(cursor, chat_id, USER_WANTS_SHAWARMA)
    mes = u'Если хочешь шаверму - нажми "Хочу шаверму"'
    btn = Button(USER_WANTS_SHAWARMA)
    reply(chat_id, mes, None, *[btn])


def process(chat_id, message=None, location=None, contact=None):
    if message == START:
        start(chat_id)
    elif message == REGISTER_SHAWARMA_POINT_MAN:
        register_shawarma_point_man(chat_id)
    elif message == REGISTER_USER:
        register_user(chat_id)
    elif contact:
        if is_chat_id_in_shawarma_point_owner(cursor, chat_id):
            update_sale_point_owner_personal_data(cursor, chat_id, contact['phone_number'], contact['first_name'],
                                                  contact['last_name'] if 'last_name' in contact else None)
            shawarma_point_location(chat_id)
        if is_chat_id_in_user(cursor, chat_id):
            update_user_personal_data(cursor, chat_id, contact['phone_number'], contact['first_name'],
                                                  contact['last_name'] if 'last_name' in contact else None)
            user_can_list_shawarma_points(chat_id)
    elif location:
        if is_chat_id_in_shawarma_point_owner(cursor, chat_id):
            update_sale_point_location(cursor, chat_id, location['latitude'], location['longitude'])
            shawarma_point_name(chat_id)
    elif is_chat_id_in_shawarma_point_owner(cursor, chat_id):
        stage = get_sale_point_owner_stage(cursor, chat_id)
        if stage == SHAWARMA_POINT_NAME:
            update_sale_point_name(cursor, chat_id, message)
            shawarma_point_time_work(chat_id)
        if stage == SHAWARMA_POINT_TIME_WORK:
            open, close = message.split()
            update_sale_point_time_work(cursor, chat_id, open, close)
            shawarma_point_price(chat_id)
        if stage == SHAWARMA_POINT_PRICE:
            update_sale_point_price(cursor, chat_id, message)
            shawarma_point_await_order(chat_id)
    elif is_chat_id_in_shawarma_point_owner(cursor, chat_id):
        stage = get_user_stage(cursor, chat_id)
