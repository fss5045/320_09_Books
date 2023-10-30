from datetime import date
def showBook(curs):
    curs.execute("SELECT * FROM book")
    return curs.fetchall()

def createNewUser(curs, username, password, firstname, lastname, email):
    today = date.today()
    #print(curs.mogrify("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, firstname, lastname, email, today, today, password)))
    curs.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, firstname, lastname, email, today, today, password))
    return

def deleteUser(curs, username):
    #print(curs.mogrify("DELETE FROM users WHERE username = %s", (username,)))
    curs.execute("DELETE FROM users WHERE username = %s", (username,))
    return

def followUser(curs, username1, username2):
    #print(curs.mogrify("INSERT INTO userfollow VALUES (%s, %s)", (username1, username2)))
    curs.execute("INSERT INTO userfollow VALUES (%s, %s)", (username1, username2))
    return

def unfollowUser(curs, username1, username2):
    #print(curs.mogrify("DELETE FROM userfollow WHERE usernamefollowed = %s AND usernamefollower = %s", (username1, username2)))
    curs.execute("DELETE FROM userfollow WHERE usernamefollowed = %s AND usernamefollower = %s", (username1, username2))
    return

def createCollection(curs, books, name):
    return

def showCollections(curs, username):
    return

def modifyCollectionName(curs, collectionId, username):
    return

def deleteCollection(curs, collectionId, username):
    return

def searchBooks(curs, searchDict):
    query = "SELECT B.bookid, B.title, B.authors, B.publishers, B.length, B.audience FROM book B UNION SELECT R.bookid, R.rating FROM rates R WHERE B.bookid = R.bookid"
    for key, value in searchDict.items():
        query += " AND B." + key + " = '" + value + "'"
    query += " ORDER BY title ASC, releasedate ASC"
    # print(curs.mogrify(query))
    curs.execute(query)
    return curs.fetchall(), query

def sortBooksByName(curs, query, name, ascending: bool):
    return

def sortBooksByPublisher(curs, query, publisher, ascending: bool):
    return

def sortBooksByGenre(curs, query, genre, ascending: bool):
    return

def sortBooksByReleaseYear(curs, quey, ascending: bool):
    return

def addBookToCollection(curs, collectionId, book):
    return

def deleteBookFromCollection(curs, collectionId, book):
    return