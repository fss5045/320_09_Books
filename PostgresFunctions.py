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

def alreadyExistingUser(curs, username):
    print(curs.mogrify("SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = %s)", (username,)))
    curs.execute("SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = %s)", (username,))
    if(curs.fetchone() == None):
        return False
    return True

def userMatchPassword(curs, username, password):
    print(curs.mogrify("SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = %s AND users.password = %s)", (username,password)))
    curs.execute("SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = %s AND users.password = %s)", (username,password))
    if (curs.fetchone() == None):
        return False
    return True
def createCollection(curs, books, name):
    curs.execute("INSERT INTO collection VALUES (%s, %s)", (books, name) )
    return

def showCollections(curs, username):
    curs.execute("SELECT FROM collection WHERE username = %s" , (username))
    return

def modifyCollectionName(curs, collectionId, newName, currentUsername):
    curs.execute("SELECT username FROM collection WHERE collectionId = %s" , (collectionId))
    if (curs.fetchone() == currentUsername):
        curs.execute("UPDATE collection SET username = %s WHERE collectionId = %s", (newName, collectionId))
    return

def deleteCollection(curs, collectionId, currentUsername):
    curs.execute("SELECT username FROM collection WHERE collectionId = %s" , (collectionId))
    if (curs.fetchone() == currentUsername):
        curs.execute("DELETE FROM collection WHERE collectionId = %s", (collectionId))
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
    curs.execute("INSERT INTO belongsto (collectionid, book) values (%s, %s)", (collectionId, book))
    return

def deleteBookFromCollection(curs, collectionId, book):
    curs.execute("DELETE FROM belongsto WHERE collectionid=%s AND book=%s", (collectionId, book))
    return