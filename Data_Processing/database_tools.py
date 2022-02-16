import psycopg2
import configparser

cursor = None
config = configparser.ConfigParser()
config.sections()
config.read("properties.ini")


def connect():
    global cursor

    try:
        connection = psycopg2.connect(
            user=config["POSTGRES"]["user"],
            password=config["POSTGRES"]["password"],
            host=config["POSTGRES"]["host"],
            port=config["POSTGRES"]["port"],
            database=config["POSTGRES"]["database"],
        )
        cursor = connection.cursor()
        cursor.execute("SET search_path TO mimiciii;")

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def query(query):
    try:

        if(type(cursor) is psycopg2.cursor):
            cursor.execute(query)
            print("Quering database")
            return cursor.fetchall()
        else:
            print("Error while fetching data from PostgreSQL")

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

