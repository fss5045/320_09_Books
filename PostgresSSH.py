import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import dotenv_values
from random import randrange
import PostgresFunctions

config = dotenv_values("LoginCredentials.env")

username = config["USERNAME"]
password = config["PASSWORD"]
dbName = "p320_09"

def loginPrompt():
    while (True):
        print("Login: 1")
        print("Create New Account: 2")
        print("Exit: q")
        cmdlnInput = input(":")
        if cmdlnInput == '1':
            alreadyExisting = False
            confirmPass = False
            usernm = ""
            psswrd = ""
            maxAttempts = 3
            while alreadyExisting != True:
                usernm = input("Username: ")
                if PostgresFunctions.alreadyExistingUser(curs, usernm):
                    alreadyExisting = True
                else:
                    maxAttempts = maxAttempts - 1
                    print("This username does not exist, please try again or make a new account")
                if maxAttempts == 0:
                    print("Ran out of attempts")
                    break

            maxAttempts = 3
            while confirmPass != True:
                psswrd = input("Password: ")
                if PostgresFunctions.userMatchPassword(curs, usernm, psswrd):
                    confirmPass = True
                else:
                    maxAttempts = maxAttempts - 1
                    print("password does not match, try again")
                if maxAttempts == 0:
                    print("Ran out of attempts")
                    break
            PostgresFunctions.updateUserAccessDate(curs, usernm)
            return usernm

        elif cmdlnInput == '2':
            alreadyExisting = True
            passConfirmation = False
            usernm = ""
            psswrd = ""
            maxAttempts = 3
            while alreadyExisting:
                usernm = input("Username: ")
                if PostgresFunctions.alreadyExistingUser(curs, usernm) == False:
                    alreadyExisting = False
                else:
                    maxAttempts = maxAttempts - 1
                    print("Username taken, please choose a different one")
                if maxAttempts == 0:
                    print("Ran out of attempts")
                    break

            maxAttempts = 3
            while passConfirmation != True:
                psswrd = input("Password: ")
                psswrdconf = input("Confirm Password: ")
                if psswrd == psswrdconf:
                    passConfirmation = True
                else:
                    maxAttempts = maxAttempts - 1
                    print("Passwords do not match, try again")
                if maxAttempts == 0:
                    print("Ran out of attempts")
                    break

            firstnm = input("First Name: ")
            lastnm = input("Last Name: ")
            email = input("Email: ")
            PostgresFunctions.createNewUser(curs, usernm, psswrd, firstnm, lastnm, email)
            return usernm

        elif cmdlnInput == 'q':
            return None
        else:
            print("Invalid Input")

def addBookToCollectionPrompt():
    global currentUsername
    book = input("Give Books Title: ")
    bookId = PostgresFunctions.getBookID(curs, book)
    if bookId == None:
        print("Book does not exist, try again")
        return
    #check for valid bookID if invalid go back to filter
    #SQL Query to show users Collections
    for collection in PostgresFunctions.showCollections(curs, currentUsername):
        print(collection)
    print("Select a collection to add to")
    collectionTitle = input("Give Collection Title: ")
    collectionId = PostgresFunctions.getCollectionId(curs, collectionTitle, currentUsername)
    if collectionId == None:
        print("Collection does not exist")
        return
    #check for valid collectionID if invalid go back to filter
    #SQL Query to add the book to given collection
    PostgresFunctions.addBookToCollection(curs, collectionId, bookId)

def printSearchQuery(searchQuery): 
    for key in searchQuery.keys():
        print(key + ": " + searchQuery[key], end=" ")
    print("")

def bookSortPrompt(originalQuery):
    #takes the original query and then adds on filters
    ascending = 'ASC'
    while True:
        print("Sort Ascending (Default) / Descending: 1")
        print("Sort by Title: 2")
        print("Sort by Release Year: 3")
        print("Sort by Publisher: 4")
        print("Sort by Genre: 5")
        print("Add book to your collection: 6")
        print("Rate a book: 7")
        print("Read a book: 8")
        print("Back to search: q")
        cmdlnInput = input(":")
        if cmdlnInput == '1':
            if ascending == 'ASC':
                ascending = 'DESC'
                print("Sorting Descending")
                # result = PostgresFunctions.sortBooks(curs, originalQuery, 'name', ascending)
                # print(result)
            else:
                ascending = 'ASC'
                print("Sorting Ascending")
                # result = PostgresFunctions.sortBooks(curs, originalQuery, 'name', ascending)
                # print(result)
            continue
        elif cmdlnInput == '2':
            result = PostgresFunctions.sortBooks(curs, originalQuery, 'title', ascending)
            print(result)
        elif cmdlnInput == '3':
            result = PostgresFunctions.sortBooks(curs, originalQuery, 'releasedate', ascending)
            print(result)
        elif cmdlnInput == '4':
            result = PostgresFunctions.sortBooks(curs, originalQuery, 'publisher', ascending)
            print(result)
        elif cmdlnInput == '5':
            result = PostgresFunctions.sortBooks(curs, originalQuery, 'genre', ascending)
            print(result)
        elif cmdlnInput == '6':
            addBookToCollectionPrompt()
        elif cmdlnInput == '7':
            rateBookPrompt()
        elif cmdlnInput == '8':
            readBookPrompt()
        elif cmdlnInput == 'q':
            break
        else:
            print("Invalid Input")

def bookSearchPrompt():
    #searchBooks(name, releaseDate, authors, publishers, genre)
    #Some search/filter prompt
    searchQuery = dict()
    while (True): 
        #part of the prompt might want to be moved outside the loop so it doesn't
        #print everytime a new parameter is added
        print("Enter following search parameters at least 1 must be non empty")
        print("Title: 1")
        print("Release Date: 2")
        print("Authors: 3")
        print("Publishers: 4")
        print("Genre: 5")
        print("Enter Search: 6")
        print("Clear Search: 7")
        print("Back to main: q")
        print("Current Search: ", end="")
        printSearchQuery(searchQuery)
        cmdlnInput = input(":")
        if cmdlnInput == "1":
            searchQuery["title"] = input("Title: ")
        elif cmdlnInput == "2":
            searchQuery["releasedate"] = input("Release Date: ")
        elif cmdlnInput == "3":
            searchQuery["authors"] = input("Author: ")
        elif cmdlnInput == "4":
            searchQuery["publishers"] = input("Publisher: ")
        elif cmdlnInput == "5":
            searchQuery["genre"] = input("Genre: ")
        elif cmdlnInput == "6":
            #Check for valid search
            if len(searchQuery) < 1:
                print("need at least 1 search parameter")
                continue
            #Search filter/ordering menu
            (fetch, query) = PostgresFunctions.searchBooks(curs, searchQuery)
            print(fetch)
            bookSortPrompt(query)
        elif cmdlnInput == "7":
            searchQuery = dict()  
        elif cmdlnInput == "q":
            break

def followUserPrompt():
    global currentUsername
    print("Give the user you want to follow")
    otherUsername = input("Give username: ")
    if PostgresFunctions.alreadyExistingUser(curs, otherUsername):
        # Maybe check if they already follow each other
        PostgresFunctions.followUser(curs, otherUsername, currentUsername)
    else:
        print("The user you want to follow does not exist")

def unfollowUserPrompt():
    global currentUsername
    print("Give the user you want to unfollow")
    otherUsername = input("Give username: ")
    if PostgresFunctions.alreadyExistingUser(curs, otherUsername):
        # Maybe check if they already follow each other
        PostgresFunctions.unfollowUser(curs, otherUsername, currentUsername)
    else:
        print("The user you want to unfollow does not exist")

def userSearchPrompt():
    global currentUsername
    while (True):
        print("Search for user: 1")
        print("Follow User: 2")
        print("Unfollow User: 3")
        print("View user profile: 4")
        print("Back to main: q")
        cmdlnInput = input(":")
        if cmdlnInput == "1":
            searchUsername = None
            searchEmail = None
            print("Search by username: 1")
            print("Search by email: 2")
            searchBy = input(":")
            if searchBy == '1':
                searchUsername = input("Give a username: ")
                print(PostgresFunctions.searchUsers(curs, searchUsername, searchEmail))
            elif searchBy == '2':
                searchEmail = input("Give an email: ")
                print(PostgresFunctions.searchUsers(curs, searchUsername, searchEmail))
        elif cmdlnInput == "2":
            followUserPrompt()
        elif cmdlnInput == "3":
            unfollowUserPrompt()
        elif cmdlnInput == "4":
            username = input("Give a username: ")
            profilePrompt(username)
        elif cmdlnInput == "q":
            break
        else:
            print("Invalid Input")

def readBookPrompt(bookTitle = None):
    global currentUsername
    if bookTitle == None:
        bookTitle = input("Which book do you want to read: ")
    startPage = input("Start page: ")
    endPage = input("End page: ")
    pages = int(endPage) - int(startPage)
    print(pages)
    PostgresFunctions.readBooks(curs, currentUsername, bookTitle, str(pages))
    return

def selectedCollectionPrompt(collectionId):
    global currentUsername
    while (True):
        booksInCollection = PostgresFunctions.showSelectedCollection(curs, username, collectionId)
        for book in booksInCollection:
            print(book)
        print("Rate book from collection: 1")
        print("Read selected book from collection: 2")
        print("Read random book from collection: 3")
        print("Rename Collection: 4")
        print("Add book to collection: 5")
        print("Delete book from collection: 6")
        print("Back to collections: q")
        cmdlnInput = input(":")
        if cmdlnInput == "1":
            rateBookPrompt()
        elif cmdlnInput == "2":
            bookTitle = input ("Which book do you want to read: ")
            readBookPrompt(bookTitle)
        elif cmdlnInput == "3":
            readBookPrompt(booksInCollection[randrange(len(booksInCollection))][1])
        elif cmdlnInput == "4":
            newColName = input("New name for selected collection: ")
            collectionExists = PostgresFunctions.getCollectionId(curs, newColName, currentUsername)
            if collectionExists == None:
                PostgresFunctions.modifyCollectionName(curs, collectionId, newColName)
            else:
                print("Collection already exists")
        elif cmdlnInput == "5":
            bookTitle = input("Which book do you want to add: ")
            bookId = PostgresFunctions.getBookID(curs, bookTitle)
            if bookId == None:
                print("Not a valid book")
            else:
                PostgresFunctions.addBookToCollection(curs, collectionId, bookId)
        elif cmdlnInput == "6":
            bookTitle = input("Which book do you want to delete: ")
            bookId = PostgresFunctions.getBookID(curs, bookTitle)
            (ids, titles, audiences, releasedates, lengths, collectionids, belongstoids) = zip(*booksInCollection)
            if bookId not in ids:
                print("That book isn't in this collection")
            else:
                PostgresFunctions.deleteBookFromCollection(curs, collectionId, bookId)
        elif cmdlnInput == "q":
            break
        else:
            print("Invalid Input")

def collectionsPrompt():
    global currentUsername
    while (True):
        print("Show your collections: 1")
        print("Create Collection: 2")
        print("Delete Collection: 3")
        print("Select A Collections: 4")
        print("Back to main: q")
        cmdlnInput = input(":")
        if cmdlnInput == "1":
            for collection in PostgresFunctions.showCollections(curs, currentUsername):
                print(collection)

        elif cmdlnInput == "2":
            newCollectionName = input("Name your collection: ")
            collectionExists = PostgresFunctions.getCollectionId(curs, newCollectionName, currentUsername)
            if collectionExists != None:
                print("Collection Name already taken")
                continue
            bookIds = []
            print("Give books to add to your new collection, enter q to finish")
            while (True):
                book = input("Enter a name of a book to add: ")
                if book == 'q':
                    break
                else:
                    bookId = PostgresFunctions.getBookID(curs, book)
                    if bookId == None:
                        print("Book does not exist, try again")
                    else:
                        bookIds.append(bookId)
            PostgresFunctions.createCollection(curs, bookIds, newCollectionName, currentUsername)

        elif cmdlnInput == "3":
            delCollectionTitle = input("Collection to delete: ")
            delCollectionId = PostgresFunctions.getCollectionId(curs, delCollectionTitle, currentUsername)
            if delCollectionId == None:
                print("Collection does not exist")
            else:
                PostgresFunctions.deleteCollection(curs, delCollectionId)

        elif cmdlnInput == "4":
            CollectionTitle = input("Collection to select: ")
            CollectionId = PostgresFunctions.getCollectionId(curs, CollectionTitle, currentUsername)
            if CollectionId == None:
                print("Collection does not exist")
            else:
                selectedCollectionPrompt(CollectionId)

        elif cmdlnInput == "q":
            break
        else:
            print("Invalid Input")

def rateBookPrompt():
    global currentUsername
    print("Give a book to rate")
    bookId = input("Book Name: ")
    rating = input("Your rating: ")
    PostgresFunctions.rateBook(curs, currentUsername, bookId, rating)

def profilePrompt(username):
    basic, books = PostgresFunctions.showUserProfile(curs, username)
    print(f"{basic[0]}'s profile:")
    print(f"{basic[1]} collections, {basic[2]} followers, {basic[3]} following")
    print(f"{username}'s top 10 books:")
    for book in books:
        print(book)
    print()

def recommendBookPrompt(username):
    while (True):
        print("Top 20 Most Popular Books in last 90 days: 1")
        print("Top 20 Most Popular Books Among Followers: 2")
        print("Top 5 new Releases This Month: 3")
        print("Recommended books for you (Top 10): 4")
        print("Back to main: q")
        cmdlnInput = input(":")
        if cmdlnInput == "1":
            print("Top 20 Most Popular Books in last 90 days:")
            top20Books = PostgresFunctions.getTopBooks(curs)
            for book in top20Books:
                print(book)
        elif cmdlnInput == "2":
            print("Top 20 Most Popular Books Among Followers:")
            topFollowerBooks = PostgresFunctions.getFollowersTopBooks(curs, username)
            for book in topFollowerBooks:
                print(book)
        elif cmdlnInput == "3":
            print("Top 5 new Releases this month: ")
            top5NewBooks = PostgresFunctions.getTop5OfMonth(curs)
            for book in top5NewBooks:
                print(book)
        elif cmdlnInput == "4":
            print("Recommended books for you (Top 10): ")
            PostgresFunctions.getRecommendedBooks(curs, username)
            # Add function here
        elif (cmdlnInput == "q"):
            break
        else:
            print("Invalid Input")

def mainPrompt():
    while (True):
        print("Search Books: 1")
        print("Recommend Book: 2")
        print("Search Users: 3")
        print("Go To Collections: 4")
        print("View your profile: 5")
        print("Exit and log out: q")
        cmdlnInput = input(":")
        if (cmdlnInput == "1"):
            bookSearchPrompt()
        elif (cmdlnInput == "2"):
            recommendBookPrompt(currentUsername)
        elif (cmdlnInput == "3"):
            userSearchPrompt()
        elif (cmdlnInput == "4"):
            collectionsPrompt()
        elif(cmdlnInput == "5"):
            profilePrompt(currentUsername)
        elif (cmdlnInput == "q"):
            print("Signing Out")
            break
        else:
            print("Invalid Input")

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

        currentUsername = loginPrompt()
        if (currentUsername != None):
            mainPrompt()

        conn.close()
except Exception as e:
    print(e)
    print("Connection failed")