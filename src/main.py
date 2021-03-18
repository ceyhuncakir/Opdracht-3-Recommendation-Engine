import mysql.connector
import sys
import time
import random
from termcolor import colored

colors = ["green", "blue", "yellow", "red", "cyan"]

def mysql_connector(user, password, db_name):
    """
    Hier verbind je met de database aan de hand van een host, username, wachtwoord en database naam. Die aanmeldings informatie sla je op onder een
    variable. Ook maak je een cursor die de vorige variable gebruikt om aan te melden.
    Je returned de variabele met de aanmeldingsgegevens en de cursor.
    :param user:, :param password:, :param db_name:
    """

    db = mysql.connector.connect(host="localhost", user=user, password=password, database=db_name)

    cursor = db.cursor()
    return db, cursor

def sql_closer(db, cursor):
    """
    Sluit de cursor en commit de veranderingen van de database daarna sluit de database.
    :param cursor:, :param db:
    """

    cursor.close()
    db.commit()
    db.close()

def create_tables(database, cursor):
    """
    functie voor het creeren van tables binnen de database
    :param database
    :param cursor
    :return
    """
    cursor.execute("USE " + database)
    cursor.execute("CREATE TABLE content_filtering (id VARCHAR(255) PRIMARY KEY UNIQUE, product_1 VARCHAR(255) NULL, product_2 VARCHAR(255) NULL, product_3 VARCHAR(255) NULL, product_4 VARCHAR(255) NULL)")
    cursor.execute("CREATE TABLE collaborative_filtering (id VARCHAR(255) PRIMARY KEY UNIQUE, product_1 VARCHAR(255) NULL, product_2 VARCHAR(255) NULL, product_3 VARCHAR(255) NULL, product_4 VARCHAR(255) NULL)")

def delete_tables(database, cursor):
    """
    functie voor het verwijderen van tables binnen de database
    :param database
    :param cursor
    :return
    """
    cursor.execute("USE " + database)
    cursor.execute("DROP TABLE content_filtering")
    cursor.execute("DROP TABLE collaborative_filtering")

def get_profiles_content(cursor, profileid):
    """
    functie voor het krijgen van profiel_data
    :return profiel_data
    """

    # mysql sql commando om data te krijgen van de huidge profiel waar recommendation op moet gebeuren
    cursor.execute("SELECT products.id, products.price, products.stock, orders.aantal, main_category.id, brand.brand, gender.id, doelgroep.id, orders.sessions_id_key, sessions.profiles_id_key FROM `products`, `gender`, `brand`, `main_category`, `orders`, `sessions`, `doelgroep` WHERE products.gender_id_key = gender.id AND products.brand_id_key = brand.id AND products.main_category_id_key = main_category.id AND orders.products_id_key = products.id AND orders.sessions_id_key = sessions.id AND products.doelgroep_id_key = doelgroep.id AND profiles_id_key = '%s'" % profileid)
    profile_data = cursor.fetchall()

    return profile_data

def get_content_recommendation(cursor, profileid):
    """
    functie voor het maken van content recommendation gebasseerd op producten die lijken op wat er laats is gekocht
    :param cursor
    :param profielid
    :return profileid, random 4 recommendated products
    """

    prodids = []

    # functie voor het ophalen van data voor de huidige profiel waar de recommendation moet gebeuren
    profile_data = get_profiles_content(cursor, profileid)

    # for loop voor vergelijkbaren producten
    for i in profile_data:
        cursor.execute("SELECT `id`, `main_category_id_key`, `gender_id_key`, `doelgroep_id_key` FROM `products` WHERE main_category_id_key = '{0}' AND gender_id_key = '{1}' AND doelgroep_id_key = '{2}'".format(i[4], i[6], i[7]))
        sim_prod = cursor.fetchall()

    # for loop voor het inzetten van vergelijkbaren producten
    for i in sim_prod:
        prodids.append(i[0])

    print(colored("\n\t" + "Content_filtering Done", "green"))

    return profileid, random.sample(prodids, 4)

def get_collaborative_recommendation(cursor, profileid):
    """
    functie voor het maken van collaborative recommendation gebasseerd op vergelijkbaren profielen
    :param cursor
    :param profileid
    :return profileid, random 4 recommendated products
    """

    prodids = []
    profileids = []

    # functie voor het ophalen van data voor de huidige profiel waar de recommendation moet gebeuren
    profile_data = get_profiles_content(cursor, profileid)

    # for loop voor vergelijkbaren profielen met de zelfde main_category, brand, doelgroep
    for i in profile_data:
        cursor.execute("SELECT products.id, products.main_category_id_key, products.gender_id_key, products.doelgroep_id_key, sessions.profiles_id_key FROM `products`, `orders`, `sessions`, `profiles` WHERE orders.products_id_key = products.id AND orders.sessions_id_key = sessions.id AND sessions.profiles_id_key = profiles.id AND main_category_id_key = '{0}' AND gender_id_key = '{1}' AND doelgroep_id_key = '{2}'".format(i[4], i[6], i[7]))
        sim_prod = cursor.fetchall()

    # for loop voor de profielen met de zelfde gekochte items binnen de categorien main_category, brand, doelgrpe
    for i in sim_prod:
        profileids.append(i[4])

    # sql execute voor een random profiel
    cursor.execute("SELECT products.id, products.price, products.stock, orders.aantal, main_category.id, brand.brand, gender.id, doelgroep.id, orders.sessions_id_key, sessions.profiles_id_key FROM `products`, `gender`, `brand`, `main_category`, `orders`, `sessions`, `doelgroep` WHERE products.gender_id_key = gender.id AND products.brand_id_key = brand.id AND products.main_category_id_key = main_category.id AND orders.products_id_key = products.id AND orders.sessions_id_key = sessions.id AND products.doelgroep_id_key = doelgroep.id AND profiles_id_key = '%s'" % ''.join(random.sample(profileids, 1)))
    profile_data = cursor.fetchall()

    # for loop voor de producten binnen de random vergelijkbaren profiel
    for i in profile_data:
        prodids.append(i[0])

    print(colored("\n\t" + "Collaborative_filtering Done", "green"))

    return profileid, random.sample(prodids, 4)


def insert_values(direction, profile, list_value, db, cursor, table, *column):
    """
    Connect aan de database en loop door de verschillende waardes in de list en voeg ze die dan toe aan de table collums.
    Execute deze command en commit het naar de sql database.
    :param direction:, :param profile, :param list_value:, :param db:, :param cursor:, :param table:, :param *column:, :return:,
    """

    if direction == 0:
        category_list_sql = "INSERT IGNORE INTO " + table + " (" + column[0] + ", " + column[1] + ", " + column[2] + ", " + column[3] + ", " + column[4] +") VALUES (%s, %s, %s, %s, %s)"
        category_list_sql_value = (str(profile), str(list_value[0]), str(list_value[1]), str(list_value[2]), str(list_value[3]))
        cursor.execute(category_list_sql, category_list_sql_value)
        db.commit()

def recommendation_engine(mysql_username, mysql_password, mysql_database):
    """
    functie voor de process van de recommendation engine
    :param mysql_username
    :param mysql_password
    :param mysql_database
    :return
    """

    db, cursor = mysql_connector(mysql_username, mysql_password, mysql_database)

    delete_tables(mysql_database, cursor)
    create_tables(mysql_database, cursor)

    cursor.execute("SELECT `profiles_id_key` FROM `sessions`")
    profiles = cursor.fetchall()

    profile_collab, recommendation_collab = get_collaborative_recommendation(cursor, '5a3e2f8ba82561000176c70a')
    insert_values(0, profile_collab, recommendation_collab, db, cursor, "collaborative_filtering", "id", "product_1", "product_2", "product_3", "product_4")

    profile_content, recommendation_content = get_content_recommendation(cursor, '5a3e2f8ba82561000176c70a')
    insert_values(0, profile_content, recommendation_content, db, cursor, "content_filtering", "id", "product_1", "product_2", "product_3", "product_4")

    sql_closer(db, cursor)

    sys.exit(0)
