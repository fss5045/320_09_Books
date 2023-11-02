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
    if username == None:
        curs.execute(f"SELECT * FROM users WHERE email = \'{email}\'")
    if email == None:
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
    #print(curs.mogrify(f"SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = \'{username}\')"))
    curs.execute(f"SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = \'{username}\')")
    if curs.fetchone() == None:
        return False
    return True

def userMatchPassword(curs, username, password):
    #print(curs.mogrify(f"SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = \'{username}\' AND users.password = \'{password}\')"))
    curs.execute(f"SELECT * FROM users WHERE EXISTS (SELECT 1 FROM users WHERE users.username = \'{username}\' AND users.password = \'{password}\')", (username,password))
    if curs.fetchone() == None:
        return False
    return True

def getBookID(curs, bookTitle):
    curs.execute("SELECT bookid FROM book WHERE title = %s", (bookTitle,))
    result = curs.fetchone()
    if result == None:
        return result
    return result[0]

def createCollection(curs, bookids, name, username):
    collectionId = getNextId(curs, "collection")
    curs.execute(f"INSERT INTO collection (collectionid, name, username) VALUES (\'{collectionId}\', \'{name}\', \'{username}\')")
    curs.execute(f"SELECT * FROM collection WHERE name = \'{name}\' AND username = \'{username}\'")
    for bookid in bookids:
        curs.execute(f"INSERT INTO belongsto (collectionid, bookid) values (\'{collectionId}\', \'{bookid}\')")
    return

def getNextId(curs, table):
    id = table+"id"
    query = "SELECT MAX("+id+") FROM " + table
    #print(curs.mogrify(query))
    curs.execute(query)
    result = curs.fetchone()
    return result[0] + 1

def showCollections(curs, username):
    curs.execute(f"SELECT * FROM collection WHERE username = \'{username}\'")
    return curs.fetchall()

def showSelectedCollection(curs, username, collectionId):
    curs.execute(f"SELECT * FROM book LEFT JOIN belongsto ON book.bookid = belongsto.bookid WHERE belongsto.collectionid = {collectionId}")
    return curs.fetchall()

def modifyCollectionName(curs, collectionId, newName):
    curs.execute(f"UPDATE collection SET name = \'{newName}\' WHERE collectionId = \'{collectionId}\'")
    return

def deleteCollection(curs, collectionId):
    curs.execute(f"DELETE FROM collection WHERE collectionId = \'{collectionId}\'")
    return

def getCollectionId(curs, title, currentUsername):
    curs.execute(f"SELECT collectionid FROM collection WHERE name = \'{title}\' AND username = \'{currentUsername}\'")
    result = curs.fetchone()
    if result == None:
        return result
    return result[0]

def searchBooks(curs, searchDict):
    query = """WITH books_refined AS
        (SELECT B.bookid, B.title,
        (SELECT string_agg(CONCAT(firstname, ' ', lastname), ', ') FROM contributor C, writes W
                WHERE (C.contributorid = W.contributorid) AND (W.bookid = B.bookid)
                GROUP BY B.bookid) AS "authors",
        (SELECT string_agg(CONCAT(firstname, ' ', lastname), ', ') FROM contributor C, publishes P
            WHERE (C.contributorid = P.contributorid) AND (P.bookid = B.bookid)
            GROUP BY B.bookid) AS "publishers",
         B.length AS pages, B.audience, B.releasedate,
        (SELECT string_agg(genrename, ', ') FROM genre G, bookgenre BG WHERE (G.genreid = BG.genreid) AND (BG.bookid = B.bookid)) AS genre,
        (SELECT AVG(rating) FROM rates R WHERE B.bookid = R.bookid) AS "Average Rating"
        FROM book B) """
    where = """SELECT * FROM books_refined"""
    firstWhere = False
    for key, value in searchDict.items():
        if not firstWhere:
            where += " WHERE "
            firstWhere = True
        else:
            where += " AND "
        if key == "releasedate":
            where += "CAST(" + key + " AS VARCHAR) LIKE '%" + value + "%'"
        else:
            where += key + " LIKE '%" + value + "%'"
        
    query += where
    # query += " ORDER BY title ASC, releasedate ASC"
    # print(curs.mogrify(query + " ORDER BY title ASC, releasedate ASC"))
    curs.execute(query + " ORDER BY title ASC, releasedate ASC")
    return curs.fetchall(), query

def sortBooks(curs, query, sorter, ascending):
    if sorter == 'releasedate':
        query += " ORDER BY date_trunc('year', " + sorter + ") " + ascending + ", " 
    else:
        query += " ORDER BY " + sorter + " " + ascending + ", "
    print(curs.mogrify(query + " ORDER BY title ASC, releasedate ASC"))
    # curs.execute(query + "title ASC, releasedate ASC")
    return curs.fetchall()

def addBookToCollection(curs, collectionId, book):
    curs.execute(f"INSERT INTO belongsto (collectionid, bookid) values (\'{collectionId}\', \'{book}\')")
    return

def readBooks(curs, currentUsername, bookId, pagesRead):
    curs.execute("SELECT NOW()")
    current_time = curs.fetchOne()
    curs.execute(f"INSERT INTO reads (username , bookid, readdatetime, pages) values (\'{currentUsername}\', \'{bookId}\', \'{current_time}\', \'{pagesRead}\')")

def rateBook(curs, username, bookId, rating):
    curs.execute(f"INSERT INTO rates (username, bookid, rating) values (\'{username}\', \'{bookId}\', \'{rating}\')")
    return

def deleteBookFromCollection(curs, collectionId, book):
    curs.execute(f"DELETE FROM belongsto WHERE collectionid  = \'{collectionId}\' AND book= \'{book}\'")
    return