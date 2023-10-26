def showBook(curs):
    curs.execute("SELECT * FROM book")
    return curs.fetchall()

def createNewUser(username, password):
    return

def followUser(username1, username2):
    return

def unfollowUser(username1, username2):
    return

def createCollection(books, name):
    return

def showCollections(username):
    return

def modifyCollectionName(collectionId, username):
    return

def deleteCollection(collectionId, username):
    return

def searchBooks(name, releaseDate, authors, publishers, genre):
    return

def filterBooksByName(books):
    return

def filterBooksByReleaseDate(books, ascending: bool):
    return

def filterBooksByGenre(books, genre):
    return

def addBookToCollection(collectionId, book):
    return

def deleteBookFromCollection(collectionId, book):
    return