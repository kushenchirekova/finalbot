import sqlite3
import config


def create_users_db():
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # try to create
    try:
        cursor.execute(f"CREATE TABLE {config.users_table}(id varchar, name varchar, age varchar, sex varchar, rating int, reg_stage int, current int, budget varchar, category varchar, pair_id varchar, lat varchar, lon varchar)")
    except:
        pass

    # close connection
    conn.commit()
    cursor.close()
    conn.close()

def create_estabs_db():
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # try to create
    try:
        cursor.execute(f"CREATE TABLE {config.estabs_table}(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, holder_id varchar, name varchar, avcheck varchar, address varchar, category varchar, photo_id varchar, lat varchar, lon varchar)")
    except:
        pass
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
