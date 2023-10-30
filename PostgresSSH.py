import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import dotenv_values
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
            while(alreadyExisting != True):
                usernm = input("Username: ")
                if(PostgresFunctions.alreadyExistingUser(curs, usernm)):
                    alreadyExisting = True
                else:
                    print("This username does not exist, please try again or make a new account")
            while(confirmPass != True):
                psswrd = input("Password: ")
                if(PostgresFunctions.userMatchPassword(curs, usernm, psswrd)):
                    confirmPass = True
                else:
                    print("password does not match, try again")
            return usernm
        elif cmdlnInput == '2':
            alreadyExisting = True
            passConfirmation = False
            usernm = ""
            psswrd = ""
            while(alreadyExisting):
                usernm = input("Username: ")
                if(PostgresFunctions.alreadyExistingUser(curs, usernm) == False):
                    alreadyExisting = False
                else:
                    print("Username taken, please choose a different one")

            while(passConfirmation != True):
                psswrd = input("Password: ")
                psswrdconf = input("Confirm Password: ")
                if(psswrd == psswrdconf):
                    passConfirmation = True
                else:
                    print("Passwords do not match, try again")

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
    bookId = input("Give Books ID")
    #check for valid bookID if invalid go back to filter
    #SQL Query to show users Collections
    print("Select a collection to add to")
    collectionId = input("Give Collection ID")
    #check for valid collectionID if invalid go back to filter
    #SQL Query to add the book to given collection

def printSearchQuery(searchQuery): 
    for key in searchQuery.keys():
        print(key + ": " + searchQuery[key], end=" ")
    print("")

def bookFilterPrompt(originalQuery):
    #takes the original query and then adds on filters
    while (True):
        print("Filter by Name: 1")
        print("Filter by Release Date: 2")
        print("Filter by Publisher: 3")
        print("Filter by Genre: 4")
        print("Add book to your collection: 5")
        print("Back to search: q")
        cmdlnInput = input(":")
        if (cmdlnInput == '1'):
            #filter query by name and reprint query
            #printSearchQuery(newQuery)
            #same stuff for 234
            pass
        elif (cmdlnInput == '2'):
            pass
        elif (cmdlnInput == '3'):
            pass
        elif (cmdlnInput == '4'):
            pass
        elif (cmdlnInput == '5'):
            addBookToCollectionPrompt()
        elif (cmdlnInput == 'q'):
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
        print("Author: 3")
        print("Publisher: 4")
        print("Genre: 5")
        print("Enter Search: 6")
        print("Clear Search: 7")
        print("Back to main: q")
        print("Current Search: ", end="")
        printSearchQuery(searchQuery)
        cmdlnInput = input(":")
        if (cmdlnInput == "1"):
            searchQuery["Name"] = input("Title: ")
        elif (cmdlnInput == "2"):
            searchQuery["Release"] = input("Release Date: ")
        elif (cmdlnInput == "3"):
            searchQuery["Author"] = input("Author: ")
        elif (cmdlnInput == "4"):
            searchQuery["Release"] = input("Publisher: ")
        elif (cmdlnInput == "5"):
            searchQuery["Genre"] = input("Genre: ")
        elif (cmdlnInput == "6"):
            #Check for valid search
            #Search filter/ordering menu
            bookFilterPrompt(searchQuery)
            pass
        elif (cmdlnInput == "7"):
            searchQuery = dict()  
        elif (cmdlnInput == "q"):
            break

def followUserPrompt():
    global currentUsername
    print("Give the user you want to follow")
    otherUsername = input("Give username: ")
    #check if its a valid username

def unfollowUserPrompt():
    global currentUsername
    print("Give the user you want to unfollow")
    otherUserName = input("Give username: ")
    #check if its a valid username      

def userSearchPrompt():
    global currentUsername
    while (True):
        print("Search username\email: 1")
        print("Follow User: 2")
        print("Unfollow User: 3")
        print("Back to main: q")
        cmdlnInput = input(":")
        if (cmdlnInput == "1"):
            #SQL User Query
            pass
        elif (cmdlnInput == "2"):
            followUserPrompt()
            pass
        elif (cmdlnInput == "3"):
            unfollowUserPrompt()
            pass
        elif (cmdlnInput == "q"):
            break
        else:
            print("Invalid Input")

def collectionsPrompt():
    global currentUsername
    while (True):
        print("Show your collections: 1")
        print("Create Collection: 2")
        print("Delete Collection: 3")
        print("Back to main: q")
        cmdlnInput = input(":")
        if (cmdlnInput == "1"):
            #SQL Query show users collections
            pass
        elif (cmdlnInput == "2"):
            newCollectionName = input("Name your collection: ")
            #SQL Query Create Collection
            pass
        elif (cmdlnInput == "3"):
            delCollectionId = input("CollectionId to delete: ")
            #SQL Query Delete Collection
            pass
        if (cmdlnInput == "q"):
            break

def mainPrompt():
    while (True):
        print("Search Books: 1")
        print("Search Users: 2")
        print("Go To Collections: 3")
        print("Go To Followers: 4")
        print("Exit and log out: q")
        cmdlnInput = input(":")
        if (cmdlnInput == "1"):
            bookSearchPrompt()
        elif (cmdlnInput == "2"):
            userSearchPrompt()
        elif (cmdlnInput == "3"):
            collectionsPrompt()
        elif (cmdlnInput == "q"):
            break

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