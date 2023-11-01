from datetime import date
def showBook(curs):
    curs.execute("SELECT * FROM book")
    return curs.fetchall()

def createNewUser(curs, username, password, firstname, lastname, email):
    today = date.today()
    #print(curs.mogrify("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, firstname, lastname, email, today, today, password)))
    curs.execute(f"INSERT INTO users VALUES (\'{username}\', \'{firstname}\', \'{lastname}\', \'{email}\', \'{today}\', \'{today}\', \'{password}\')", (username, firstname, lastname, email, today, today, password))
    return

def deleteUser(curs, username):
    #print(curs.mogrify("DELETE FROM users WHERE username = %s", (username,)))
    curs.execute(f"DELETE FROM users WHERE username = \'{username}\'")
    return

def searchUsers(curs, username, email):
    if (username == None):
        curs.execute(f"SELECT * FROM users WHERE email = \'{email}\'")
    if (email == None):
        curs.execute(f"SELECT * FROM users WHERE username = \'{username}\'")
    return curs.fetchall()

def followUser(curs, username1, username2):
    #print(curs.mogrify("INSERT INTO userfollow VALUES (%s, %s)", (username1, username2)))
    curs.execute(f"INSERT INTO userfollow VALUES (\'{username1}\', \'{username2}\')")
    return

def unfollowUser(curs, username1, username2):
    #print(curs.mogrify("DELETE FROM userfollow WHERE usernamefollowed = %s AND usernamefollower = %s", (username1, username2)))
    curs.execute(f"DELETE FROM userfollow WHERE usernamefollowed = \'{username1}\' AND usernamefollower = \'{username2}\'")
    return

def alreadyExistingUser(curs, username):
    print(curs.mogrify(f"SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = \'{username}\')"))
    curs.execute(f"SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = \'{username}\')")
    if(curs.fetchone() == None):
        return False
    return True

def userMatchPassword(curs, username, password):
    print(curs.mogrify(f"SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = \'{username}\' AND users.password = \'{password}\')"))
    curs.execute(f"SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = \'{username}\' AND users.password = \'{password}\')", (username,password))
    if (curs.fetchone() == None):
        return False
    return True

def createCollection(curs, books, name, username):
    curs.execute(f"INSERT INTO collection (name, username) VALUES (\'{name}\', \'{username}\')")
    curs.execute(f"SELECT FROM collection WHERE name = \'{name}\' AND username = \'{username}\'")
    collectionId = curs.fetchone()[0]
    for book in books:
        curs.execute(f"INSERT INTO belongsto (collectionid, book) values (\'{collectionId}\', \'{book}\')")
    return

def showCollections(curs, username):
    curs.execute(f"SELECT FROM collection WHERE username = \'{username}\'")
    return curs.fetchall()

def modifyCollectionName(curs, collectionId, newName, currentUsername):
    curs.execute(f"SELECT username FROM collection WHERE collectionId = \'{collectionId}\'")
    if (curs.fetchone() == currentUsername):
        curs.execute(f"UPDATE collection SET username = \'{newName}\' WHERE collectionId = \'{collectionId}\'")
    return

def deleteCollection(curs, collectionId, currentUsername):
    curs.execute(f"SELECT username FROM collection WHERE collectionId = \'{collectionId}\'")
    if (curs.fetchone() == currentUsername):
        curs.execute(f"DELETE FROM collection WHERE collectionId = \'{collectionId}\'")
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

def readBooks(curs, currentUsername, bookId, pagesRead):
    curs.execute("SELECT NOW()")
    current_time = curs.fetchOne()
    curs.execute("INSERT INTO reads (username , bookid, readdatetime, pages) values (%s, %s, %s, %s)", (currentUsername, bookId, current_time, pagesRead))

def rateBook(curs, username, bookId, rating):
    curs.execute("INSERT INTO rates (username, bookid, rating) values (%s, %s, %s)", username, bookId, rating)
    return

def deleteBookFromCollection(curs, collectionId, book):
    curs.execute("DELETE FROM belongsto WHERE collectionid=%s AND book=%s", (collectionId, book))
    return