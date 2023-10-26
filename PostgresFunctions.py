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

def searchBooks(curs, name, releaseDate, authors, publishers, genre):
    return

def filterBooksByName(curs, books):
    return

def filterBooksByReleaseDate(curs, books, ascending: bool):
    return

def filterBooksByGenre(curs, books, genre):
    return

def addBookToCollection(curs, collectionId, book):
    return

def deleteBookFromCollection(curs, collectionId, book):
    return