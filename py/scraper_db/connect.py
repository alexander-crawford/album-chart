import mysql.connector
from mysql.connector import errorcode
import config

if __name__ == '__main__':
    connect()

def connect():
    # create table dictionary
    TABLES = {}

    # add artist table
    TABLES['artist'] = (
        "CREATE TABLE IF NOT EXISTS artist ("
        "id int UNSIGNED NOT NULL AUTO_INCREMENT,"
        "name varchar(256) NOT NULL,"
        "PRIMARY KEY (id),"
        "UNIQUE KEY (name)"
        ") ENGINE=InnoDB"
    )

    # add album table
    TABLES['album'] = (
        "CREATE TABLE IF NOT EXISTS album ("
        "id smallint UNSIGNED NOT NULL AUTO_INCREMENT,"
        "artist_id int UNSIGNED NOT NULL,"
        "title varchar(256) NOT NULL,"
        "year YEAR,"
        "image varchar(256),"
        "resized BOOLEAN DEFAULT FALSE,"
        "PRIMARY KEY (id),"
        "UNIQUE KEY (image),"
        "FOREIGN KEY (artist_id)"
        "REFERENCES artist (id)"
        ") ENGINE=InnoDB"
    )

    # add source table
    TABLES['source'] = (
        "CREATE TABLE IF NOT EXISTS source ("
        "id int UNSIGNED NOT NULL AUTO_INCREMENT,"
        "title varchar(256) NOT NULL,"
        "url varchar(256) NOT NULL,"
        "container_tag varchar(20) NOT NULL,"
        "container_class varchar(256) NOT NULL,"
        "artist_tag varchar(20) NOT NULL,"
        "artist_class varchar(256) NOT NULL,"
        "album_tag varchar(20) NOT NULL,"
        "album_class varchar(256) NOT NULL,"
        "PRIMARY KEY (id)"
        ") ENGINE=InnoDB"
    )

    # add source_album table
    TABLES['source_album'] = (
        "CREATE TABLE IF NOT EXISTS source_album ("
        "source_id int UNSIGNED NOT NULL,"
        "album_id smallint UNSIGNED NOT NULL,"
        "FOREIGN KEY (source_id)"
        "REFERENCES source (id),"
        "FOREIGN KEY (album_id)"
        "REFERENCES album (id),"
        "PRIMARY KEY (source_id, album_id)"
        ") ENGINE=InnoDB"
    )

    # add api table
    TABLES['api'] = (
        "CREATE TABLE IF NOT EXISTS api ("
        "id tinyint UNSIGNED NOT NULL AUTO_INCREMENT,"
        "name varchar(256) NOT NULL,"
        "PRIMARY KEY (id),"
        "UNIQUE KEY (name)"
        ") ENGINE=InnoDB"
    )

    # add album_api table
    TABLES['album_api'] = (
        "CREATE TABLE IF NOT EXISTS album_api ("
        "album_id smallint UNSIGNED NOT NULL,"
        "api_id tinyint UNSIGNED NOT NULL,"
        "FOREIGN KEY (album_id)"
        "REFERENCES album (id),"
        "FOREIGN KEY (api_id)"
        "REFERENCES api (id),"
        "PRIMARY KEY (album_id, api_id)"
        ") ENGINE=InnoDB"
    )

    # create main table
    TABLES['main'] = (
        "CREATE TABLE IF NOT EXISTS main AS "
        "SELECT ROW_NUMBER() OVER (ORDER BY COUNT(source_album.album_id) DESC, "
        "album.year DESC,artist.name ASC, album.title ASC) position, "
        "artist.id AS artist_id, "
        "album.id AS album_id, "
        "IFNULL(CONCAT('./img/',album.image),'./blank.svg') AS image, "
        "album.title AS title, "
        "artist.name AS artist, "
        "album.year AS year "
        "FROM album "
        "LEFT JOIN source_album ON album.id = source_album.album_id "
        "INNER JOIN artist ON album.artist_id = artist.id "
        "GROUP BY album.id;"
    )

    # create connection to mysql database
    cnx = mysql.connector.connect(user=config.mysql_username,password=config.mysql_password)

    # create cursor
    cursor = cnx.cursor()

    # set database name
    DB_NAME = "scraper_db"

    # create database if not existing
    try:
        cursor.execute("USE {}".format(DB_NAME))
        print(DB_NAME," OK")
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
                exit()
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(' error ',err)
            exit()


    # loop over create table statements
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("{} table ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            print(' error ',err)
            exit()
        else:
            print("OK")

    # reset cursor
    cursor.close()

    # reutrn connection to db
    return cnx
