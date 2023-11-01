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
    curs.execute("DELETE FROM users WHERE username = %s", (username))
    return

def searchUsers(curs, username, email):
    if (username == None):
        curs.execute("SELECT * FROM users WHERE email = %s", (email))
    if (email == None):
        curs.execute("SELECT * FROM users WHERE username = %s", (username))
    return curs.fetchall()

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

def createCollection(curs, books, name, username):
    curs.execute("INSERT INTO collection (name, username) VALUES (%s, %s)", (name, username))
    curs.execute("SELECT FROM collection WHERE name = %s AND username = %s", (name, username))
    collectionId = curs.fetchone()[0]
    for book in books:
        curs.execute("INSERT INTO belongsto (collectionid, book) values (%s, %s)", (collectionId, book))
    return

def showCollections(curs, username):
    curs.execute("SELECT FROM collection WHERE username = %s" , (username))
    return curs.fetchall()

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

def rateBook(curs, username, bookId, rating):
    curs.execute("INSERT INTO rates (username, bookid, rating) values (%s, %s, %s)", username, bookId, rating)
    return

def searchBooks(curs, searchDict):
    # query = """SELECT B.bookid, B.title,
    #             (SELECT string_agg(CONCAT(firstname, ' ', lastname), ', ') FROM contributor C, writes W
    #                 WHERE (C.contributorid = W.contributorid) AND (W.bookid = B.bookid)
    #                 GROUP BY B.bookid) AS "authors",
    #             (SELECT string_agg(CONCAT(firstname, ' ', lastname), ', ') FROM contributor C, publishes P
    #                 WHERE (C.contributorid = P.contributorid) AND (P.bookid = B.bookid)
    #                 GROUP BY B.bookid) AS "publishers",
    #             B.length AS pages, B.audience,
    #             (SELECT AVG(rating) FROM rates R WHERE B.bookid = R.bookid) AS "Average Rating"
    #             FROM book B"""
    start = """SELECT B.bookid, B.title, """
    author = """(SELECT string_agg(CONCAT(firstname, ' ', lastname), ', ') FROM contributor C, writes W
                    WHERE (C.contributorid = W.contributorid) AND (W.bookid = B.bookid)
                    GROUP BY B.bookid) AS "authors", """
    publisher = """(SELECT string_agg(CONCAT(firstname, ' ', lastname), ', ') FROM contributor C, publishes P
                    WHERE (C.contributorid = P.contributorid) AND (P.bookid = B.bookid)
                    GROUP BY B.bookid) AS "publishers", """
    genre = """"""
    pagesAudience= """B.length AS pages, B.audience, """
    where = "FROM book B WHERE "
    for key, value in searchDict.items():
        if key == "title":
            where += "B." + key + " LIKE '%" + value + "%'"
        if key == "releasedate":
            where += "B." + key + " = '" + value + "'"
        if key == "author":
            author.replace("")
        if key == "publisher":
            publisher.replace("")
        if key == "genre":
            genre.replace("")
    query = start + author + publisher + pagesAudience + genre + where
    # query += " ORDER BY title ASC, releasedate ASC"
    # print(curs.mogrify(query + " ORDER BY B.title ASC, B.releasedate ASC"))
    curs.execute(query + " ORDER BY B.title ASC, B.releasedate ASC")
    return curs.fetchall(), query

def sortBooks(curs, query, sorter, ascending):
    if (sorter == 'releasedate'):
        query += " ORDER BY YEAR(B." + sorter + ") " + ascending + ", " 
    else:
        query += " ORDER BY B." + sorter + " " + ascending + ", "
    curs.execute(query + "B.title ASC, B.releasedate ASC")
    return curs.fetchall()

def addBookToCollection(curs, collectionId, book):
    curs.execute("INSERT INTO belongsto (collectionid, book) values (%s, %s)", (collectionId, book))
    return

def deleteBookFromCollection(curs, collectionId, book):
    curs.execute("DELETE FROM belongsto WHERE collectionid=%s AND book=%s", (collectionId, book))
    return