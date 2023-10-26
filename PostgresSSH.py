import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import dotenv_values
import PostgresFunctions

config = dotenv_values("LoginCredentials.env")

username = config["USERNAME"]
password = config["PASSWORD"]
dbName = "p320_09"

try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('127.0.0.1', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }


        conn = psycopg2.connect(**params)
        conn.autocommit = True
        curs = conn.cursor()
        print("Database connection established")

        #print(PostgresFunctions.showBook(curs))
        #PostgresFunctions.followUser(curs, "fcostard0", "aalexander1")
        #PostgresFunctions.unfollowUser(curs, "fcostard0", "aalexander1")
        #PostgresFunctions.createNewUser(curs, "tester", "fakepass", "ethan", "nunez", "ern1274@rit.edu")
        #PostgresFunctions.deleteUser(curs, "tester")


        conn.close()
except Exception as e:
    print(e)
    print("Connection failed")