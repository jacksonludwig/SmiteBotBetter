from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
import utils

CATEGORIES = ["god_has_item_in_core",
              "god_has_item_in_offensive", "god_has_item_in_defensive"]


def connect():
    """ Test connect to MySQL database """
    db_config = read_db_config()
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')

    except Error as error:
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')


def query_with_fetchone():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM god")

        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def query_with_fetchall(db):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {db}")
        rows = cursor.fetchall()

       # print('Total Row(s):', cursor.rowcount)
        names = []
        for row in rows:
            names.append(row[0])

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return names


def insert_gods(names):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        query = "INSERT INTO god(god_name) VALUE(%s)"
        cursor.executemany(query, names)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def insert_items(names):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        query = "INSERT INTO item(item_name) VALUE(%s)"
        cursor.executemany(query, names)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def insert_into_build(name, category, item):
    query = f"INSERT INTO {CATEGORIES[category]}(god_id, item_id) VALUES({name}, {item})"
    #args = (name, item)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def query_items_for_build(god_id, category):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(f"""
                       SELECT god_name, item_name FROM {CATEGORIES[category]}
                       JOIN god ON {CATEGORIES[category]}.god_id=god.god_id
                       JOIN item ON {CATEGORIES[category]}.item_id=item.item_id
                       WHERE god.god_id={god_id}
                       """)
        rows = cursor.fetchall()
        items = [row[1] for row in rows]
       # print('Total Row(s):', cursor.rowcount)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return items


def query_build_by_name(name_dict, name):
    god_id = utils.find_id_by_name(name_dict, name)
    core = query_items_for_build(god_id, 0)
    offensive = query_items_for_build(god_id, 1)
    defensive = query_items_for_build(god_id, 2)
    return [core, offensive, defensive]


if __name__ == '__main__':
    # connect()
    # query_with_fetchone()
    # names = utils.read_names("names.txt")
    # names = utils.read_names("items.txt")
    # utils.make_singleton_tuples(names)
    # print(names)
    # insert_items(names)
    # names_list_from_db = query_with_fetchall("god")
    # print(names_list_from_db[0])
    a = query_items_for_build(109, 0)
    print(a)
    b = query_items_for_build(109, 1)
    print(b)
    c = query_items_for_build(109, 2)
    print(c)
