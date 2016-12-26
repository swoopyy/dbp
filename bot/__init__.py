user_stage = ''
sale_point_owner_stage = ''


def get_json_from_row(cursor, row):
    json_result = {}
    for i, column in enumerate(row):
        json_result[cursor.description[i][0]] = column
    return json_result


def add_user(cursor, chat_id):
    cursor.execute('insert into User (chat_id)' +
                   'values (\'' + str(chat_id) + '\')')


def update_user_personal_data(cursor, chat_id, phone_number, first_name, last_name):
    cursor.execute('update User set name = \'' + first_name + '\', last_name = \'' + (last_name if last_name else 'NULL') + '\', tel = \'' + str(
        phone_number) + '\' where chat_id = \'' + str(chat_id) + '\'')


def update_sale_point_owner_personal_data(cursor, chat_id, phone_number, first_name, last_name):
    cursor.execute(
        'update SalePointOwner set name = \'' + first_name + '\', last_name = \'' + (last_name if last_name else 'NULL') + '\', tel = \'' + str(
            phone_number) + '\' where chat_id = \'' + str(chat_id) + '\'')


def add_sale_point_owner(cursor,  chat_id):
    cursor.execute('insert into SalePointOwner (chat_id)'
                   'values (\'' + str(chat_id) + '\')')


def update_sale_point_location(cursor, chat_id, lat, lon):
    cursor.execute(
        'UPDATE SalePoint SET Latitude_WGS84 = {0}, Longitude_WGS84 = {1} WHERE system_id = {2}'.format(
            lat,
            lon,
            get_sale_point_id_by_chat_id(cursor, chat_id)
        )
    )


def update_sale_point_name(cursor, chat_id, name):
    cursor.execute(
        "UPDATE SalePoint SET Name = '{0}' WHERE system_id = {1}".format(
            name,
            get_sale_point_id_by_chat_id(cursor, chat_id),
        )
    )


def update_sale_point_time_work(cursor, chat_id, open_time, close_time):
    cursor.execute(
        'UPDATE SalePoint SET open_time = {0}, close_time = {1} WHERE system_id = {2}'.format(
            open_time,
            close_time,
            get_sale_point_id_by_chat_id(cursor, chat_id),
        )
    )


def get_sale_point_id_by_chat_id(cursor, chat_id):
    cursor.execute('USE shaw_test')
    cursor.execute(
        'SELECT point.system_id FROM SalePointOwner owner, SalePoint point WHERE owner.chat_id = {0};'.format(str(chat_id)))
    sale_point = cursor.fetchone()
    return int(sale_point[0])


def get_user_id_by_chat_id(cursor, chat_id):
    cursor.execute('select system_id from User where chat_id = \'' + str(chat_id) + '\'')
    fetch = cursor.fetchall()
    return get_json_from_row(cursor, fetch)


def add_order(cursor, user_id, sale_point_id):
    cursor.execute(
        'INSERT INTO ShawarmaOrder (SP_id, U_id) values ({0}, {1});'.format(str(sale_point_id), str(user_id))
    )


def update_order_time(cursor, user_id, time):
    cursor.execute(
        'UPDATE ShawarmaOrder SET time = {0} WHERE U_id = {1}'.format(
            time,
            user_id
        )
    )


def update_order_description(cursor, user_id, description):
    cursor.execute(
        "UPDATE ShawarmaOrder SET description = '{0}' WHERE U_id = {1}".format(
            description,
            user_id
        )
    )


def get_all_orders_of_sale_point(cursor, chat_id):
    cursor.execute(
        'SELECT * FROM SalePoint WHERE system_id = {0};'.format(str(get_sale_point_id_by_chat_id(cursor, chat_id))))
    orders = cursor.fetchall()
    return [get_json_from_row(cursor, order) for order in orders]


def update_order_status(cursor, order_id, status):
    cursor.execute(
        "UPDATE ShawarmaOrder SET sh_status = '{0}' WHERE system_id = {1}".format(
            status,
            order_id
        )
    )


def update_user_stage(cursor, chat_id, stage):
    global user_stage
    user_stage = stage
    cursor.execute('update User set stage = \'' + str(stage) + '\' where chat_id = \'' + str(chat_id) + '\'')


def get_user_stage(cursor, chat_id):
    cursor.execute('select stage from User where chat_id = \'' + str(chat_id) + '\'')
    return cursor.fetchone()[0]


def get_sale_point_owner_stage(cursor, chat_id):
    cursor.execute('select stage from SalePointOwner where chat_id = \'' + str(chat_id) + '\'')
    fetch = cursor.fetchone()
    return fetch[0]


def update_sale_point_owner_stage(cursor, chat_id, stage):
    cursor.execute('update SalePointOwner set stage = \'' + str(stage) + '\' where chat_id = \'' + str(chat_id) + '\'')


def update_sale_point_price(cursor, chat_id, price):
    cursor.execute(
        "UPDATE SalePoint SET price = {0} WHERE system_id = {1}".format(
            price,
            get_sale_point_id_by_chat_id(cursor, chat_id)
        )
    )


def is_chat_id_in_shawarma_point_owner(cursor, chat_id):
    cursor.execute('select * from SalePointOwner where chat_id = ' + str(chat_id))
    fetch = cursor.fetchall()
    if not fetch:
        return False
    return True



def is_chat_id_in_user(cursor, chat_id):
    cursor.execute('select * from User where chat_id = \'' + str(chat_id) + '\'')
    fetch = cursor.fetchall()
    if not fetch:
        return False
    return True


def get_closes(cursor, lat, lon):
    buf = 0.0
    max_buf = 10
    temp_res = ()

    while buf <= max_buf:
        buf += 0.1
        cursor.execute('select * from (select SalePoint.*, (6371 * acos(cos(radians(\'' + str(lat) + '\'))\
        * cos(radians(Latitude_WGS84)) * cos(radians(Longitude_WGS84) - radians(\'' + str(lon) + '\'))\
        + sin(radians(\'' + str(lat) + '\')) * sin(radians(Latitude_WGS84)))) as Distance from SalePoint) t\
        where t.Distance < 10 order by Distance asc;')
        temp_res = cursor.fetchall()
        if len(temp_res) != 0:
            break
    return [get_json_from_row(cursor, tr) for tr in temp_res]


def get_user_by_chat_id(cursor, chat_id):
    cursor.execute(
        'SELECT * FROM User WHERE chat_id = {0};'.format(
            str(chat_id)
        )
    )
    user = cursor.fetchone()
    user_dict = get_json_from_row(cursor, user)
    result_dict = {}
    for key, value in user_dict.items():
        result_dict[key.lower()] = value
    return result_dict
