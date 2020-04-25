from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
import utils


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

        print('Total Row(s):', cursor.rowcount)
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


if __name__ == '__main__':
    # connect()
    # query_with_fetchone()
    # names = utils.read_names("names.txt")
    # names = utils.read_names("items.txt")
    # utils.make_singleton_tuples(names)
    # print(names)
    # insert_items(names)
    names_list_from_db = query_with_fetchall("god")
