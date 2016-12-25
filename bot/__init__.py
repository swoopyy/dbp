user_stage = ''
sale_point_owner_stage = ''


def add_user(cursor, chat_id):
    pass


def update_user_personal_data(cursor, chat_id, phone_number, first_name, last_name):
    pass


def update_sale_point_owner_personal_data(cursor, chat_id, phone_number, first_name, last_name):
    pass


def add_sale_point_owner(cursor,  chat_id):
    pass



def update_sale_point_location(cursor, chat_id, lat, lon):
    pass


def update_sale_point_name(cursor, chat_id, name):
    pass


def update_sale_point_time_work(cursor, chat_id, open_time, close_time):
    pass


def get_sale_point_id_by_chat_id(cursor, chat_id):
    pass


def get_user_id_by_chat_id(cursor, chat_id):
    pass


def add_order(cursor, user_id, sale_point_id):
    pass


def update_order_time(cursor, user_id, time):
    pass


def update_order_description(cursor, user_id, description):
    pass


def get_all_orders_of_sale_point(cursor, chat_id):
    pass


def update_order_status(cursor, order_id, status):
    pass


def update_user_stage(cursor, chat_id, stage):
    global user_stage
    user_stage = stage


def get_user_stage(cursor, chat_id):
    return user_stage


def get_sale_point_owner_stage(cursor, chat_id):
    return sale_point_owner_stage


def update_sale_point_owner_stage(cursor, chat_id, stage):
    global sale_point_owner_stage
    sale_point_owner_stage = stage

def update_sale_point_price(cursor, chat_id, price):
    pass


def is_chat_id_in_shawarma_point_owner(cursor, chat_id):
    return True

def is_chat_id_in_user(cursor, chat_id):
    return False