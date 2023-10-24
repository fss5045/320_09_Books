def showBook(curs):
    curs.execute("SELECT * FROM book")
    return curs.fetchone()