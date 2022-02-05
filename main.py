# importing the core pacakges for the development 
from operator import le
import re
import sqlite3, sys, string, random

# Class User Deals with all of the Stuff Related to User Credentials and Authentication 
class User:
    # here we have the constructor
    def __init__(self):
        self.getCursor()

    #method for creating the connection and the cursor 
    def getCursor(self):
        self.connection = sqlite3.connect("Users.db")
        self.cursor = self.connection.cursor() 

    #method for commiting and closing the dB Connection after insertion, updation, and deletion.
    def commitCloseconn(self):
        self.connection.commit()
        self.connection.close()

    # method for creating a new db table 
    def createTable(self):

        query = f"""CREATE TABLE Users(
            Name Text,
            Email Text,
            Number integer,
            Password Text,
            BorrowedBooks BLOB,
            ReservedBooks BLOB)"""

        self.cursor.execute(query)

        self.commitCloseconn()

    # method for storing the lists of special chars, numbers and alphabets:-
    def getCharList(self):
        self.lst_chrs = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
        self.lst_small_alphabets = [i for i in string.ascii_lowercase]
        self.lst_big_alphabets = [i for i in string.ascii_uppercase]
        self.lst_numbers = [str(i) for i in range(10)]

    # method for checking password's strength:-
    def checkPasswordStrength(self, password):
        self.getCharList()
        count = 0
        for char in password:
            if (char in self.lst_chrs) or (char in self.lst_small_alphabets) or (char in self.lst_big_alphabets) or (char in self.lst_numbers):
                count += 1
        if count < 8:
            return False
        else:
            return True

    # method for generating a Random Password:- 
    def generateRandomPassword(self):
        self.getCharList()
        special_chars = ''.join([random.choice(self.lst_chrs) for i in range(int(len(self.lst_chrs)/3))])
        small_words = ''.join([random.choice(self.lst_small_alphabets) for i in range(int(len(self.lst_small_alphabets)/5))])
        big_words = ''.join([random.choice(self.lst_big_alphabets) for i in range(int(len(self.lst_big_alphabets)/5))])
        numbers = ''.join([random.choice(self.lst_numbers) for i in range(int(len(self.lst_numbers)/3))])
        return special_chars+small_words+big_words+numbers


    # method for taking all the info of user 
    def takeCredentials(self):
        self.name = input(f'Enter your Full Name: ')

        self.email = input(f'Enter your valid Email Address: ')
        # assert '@' in self.email, "Invalid Email"

        self.number = int(input(f'Enter your cell number with country code: '))
        # assert len(str(self.number)) == 12, "Phone Number does not meet the requirements"

        message = f"The Password Must Contain At Least: \n1-Two Special Characters\n2-Three Lower Case Letters\n3-One Upper Case Letter\n4-Two Numbers"
        print(message)
        while True:
            self.password = input(f'Enter your Password: ')
            if self.checkPasswordStrength(self.password):
                print(f'Account Has Been Successfully Created')
                break
            else:
                print(f'The Password Donot Meet the Requirements, Enter it Again or Press (Y) to Generate a Random Password or any other key to enter the Password Again: ')
                choice = input(f'Do you want to Generate a Random Password ?\n [Y/N]: ')
                if choice.upper() == 'Y':
                    self.password = self.generateRandomPassword()
                    print(f'Your Password is: {self.password}. Save it somewhere.')
                    break
                else:
                    continue

    # method for traversing through all the records of DB
    def TraverseDb(self):
        count = 1
        users = self.cursor.fetchall()
        for user in range(len(users)):
            if user == 0:
                continue
            print(f'\nUser {count}: {"-"*20}')
            for i in range(len(users[user])):
                if i == 0:
                    print(f'\n1-Name: {users[user][i]}')
                elif i == 1:
                    print(f'2-Email: {users[user][i]}')
                elif i == 2:
                    print(f'3-Phone Number: {users[user][i]}')
                elif i == 3:
                    print(f'4-Password: {users[user][i]}')
                elif i == 4:
                    print(f'5-Borrowed Books: {users[user][i]}')
                elif i == 5:
                    print(f'6-Reserved Books: {users[user][i]}')
            print(f'{"-"*60}')
            count += 1

    #methods for all the CRUD Operations:-
    # 1- Method for inserting a new record i.e User
    def insertRecord(self):
        self.takeCredentials()
        self.getCursor()
        # Registering the New User 
        query = f"INSERT INTO Users VALUES (?,?,?,?,?,?)"
        userInfo = (self.name, self.email, self.number, self.password, '', '')
        self.cursor.execute(query, userInfo)

        self.commitCloseconn()

    def insert_borrowBooks(self):
        book = 'Atomic Habbits'
        self.getCursor()
        query = f"SELECT * FROM Users"
        self.cursor.execute(query)
        book_ = ""
        for user in self.cursor.fetchall():
            book_ = eval(user[4])
        book_.append(book)

        query_1 = f"UPDATE Users SET BorrowedBooks = (?) WHERE Email = (?)"
        str_lst = f"[{','.join(str(i) for i in book_)}]"
        email = "raffayadmin@gmail.com"
        data_1 = (str_lst,email)
        self.cursor.execute(query_1, data_1)
        self.commitCloseconn()

    #testing method to update the reserved books column
    def delReservedBooks(self):
        self.getCursor()
        email = "alikhan@gmail.com"
        new_book = ''
        query_2 = f"UPDATE Users SET ReservedBooks = (?) WHERE Email = (?)"
        data_2 = (new_book, email)
        self.cursor.execute(query_2, data_2)
        self.commitCloseconn()
        print(f'Success/......')

    # method for displaying all the emails:-
    def showAllEmails(self):
        self.getCursor()
        query = f"SELECT * FROM Users"
        self.cursor.execute(query)
        emails = []
        for user in self.cursor.fetchall():
            emails.append(user[1])
        for i in range(len(emails)):
            if i == 0:
                continue
            print(f'{i}- {emails[i]}')

    # [(araga, aaha), (araga, aaha), (araga, aaha)] users
    # method for validating the email in the database:-
    def checkEmail(self, email):
        self.getCursor()
        query = f"SELECT * FROM Users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        for i in range(len(users)):
            # for admin record:-
            if i == 0:
                continue
            else:
                if users[i][1] == email:
                    return True
        return False

    # method for validating the password in the database:-
    def checkPassword(self, password):
        self.getCursor()
        query = f"SELECT * FROM Users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        for i in range(len(users)):
            # for admin record:-
            if i == 0:
                continue
            else:
                if users[i][3] == password:
                   return True
        return False

    # method for validating the Admin Email:-
    def checkAmdinEmail(self, email):
        self.getCursor()
        query = f"SELECT * FROM Users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        for i in range(len(users)):
            # for admin record:-
            if i == 0:
                if users[i][1] == email:
                   return True
            else:
                continue
        return False

    #method for showing all the records as a list:-
    def showAllRecords(self):
        self.getCursor()
        query = f"SELECT * FROM Users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        for i in range(len(users)):
            if i == 0:
                continue
            else:
                if users[i][1] == "tester@gmail.com":
                    return True
        return False
                
    # method for validating the Admin Password:-
    def checkAmdinPassword(self, password):
        self.getCursor()
        query = f"SELECT * FROM Users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        for i in range(len(users)):
            # for admin record:-
            if i == 0:
                if users[i][3] == password:
                   return True
            else:
                continue
        return False

    #method for changing the admin password and email:-
    def changeAdminPasswordEmail(self):
        self.updateRecord()
  
    # 2- Method for update an existing record:-
    def updateRecord(self):
        self.getCursor()
        email = input(f'Enter your email to update your Credentials: ')

        if self.checkEmail(email) or self.checkAmdinEmail(email):
            query = f"SELECT * FROM Users WHERE Email = (?)"
            self.cursor.execute(query, (email,))
            self.TraverseDb()
            while 1:
                choice = input(f'Press: |(1) to update Name| |(2) to update Email| |(3) to update Number| |(4) to update Password| |(5) to exit|')
                if choice == '1':
                        self.getCursor()
                        new_name = input(f'Enter the new Name: ')
                        query = f"UPDATE Users SET Name = (?) WHERE Email = (?)"
                        self.cursor.execute(query, (new_name, email))
                        self.commitCloseconn()
                        print(f'Name has been updated to --> {new_name}')

                elif choice == '2':
                        self.getCursor()
                        new_email = input(f'Enter the new Email: ')
                        query = f"UPDATE Users SET Email = (?) WHERE Email = (?)"
                        self.cursor.execute(query, (new_email, email))
                        self.commitCloseconn()
                        print(f'Email has been updated to --> {new_email}')


                elif choice == '3':
                        self.getCursor()
                        new_number = int(input(f'Enter the new phone number:'))
                        query = f"UPDATE Users SET Number = (?) WHERE Email = (?)"
                        self.cursor.execute(query, (new_number, email))
                        self.commitCloseconn()
                        print(f'Number has been updated to --> {new_number}')


                elif choice == '4':
                        while 1:
                            self.getCursor()
                            new_password = input(f'Enter the new password: ')
                            if (self.checkPasswordStrength(new_password)):
                                query = f"UPDATE Users SET Password = (?) WHERE Email = (?)"
                                self.cursor.execute(query, (new_password, email))
                                self.commitCloseconn()
                                print(f'Number has been updated to --> {new_password}')
                            else:
                                print(f'The New Password Donot Meet the Requirements:( Try Again: ')
                                continue    
                elif choice == '5':
                    break

                else:
                    print(f'Please Enter a Valid Option!!')      
            
        else:
            print('Please Enter Valid Email')
    
    
    # 3- Method for showing all the records:-
    def showRecords(self):
        print(f'{"-"*60}')
        print(f'All Registered Members')
        print(f'{"-"*60}')
        self.getCursor()
        query = f"SELECT * FROM Users"
        self.cursor.execute(query)
        self.TraverseDb()

         
    # 4 Method for deleting an existing record (For Admin):-
    def deleteRecord(self, email):
        self.getCursor()
        query = f"DELETE FROM Users WHERE Email = (?)"
        data = (email, )
        self.cursor.execute(query, data)
        self.commitCloseconn()
        print(f"User's Membership has been cancelled and account has been deleted!")

    # Method for deleting an existing record (For LayMan):-
    def deleteUser(self):
        print(f'{"-"*60}')
        print(f'{"-"*30}Delete Your Account{"-"*30}')
        print(f'{"-"*60}')
        email = input(f'Enter your email to delete your account: ')
        if self.checkEmail(email):
            while 1:
                choice = input(f'Are you sure to delete your account: [Y/N]')
                if choice.upper() == "Y":
                    self.getCursor()
                    query = f"DELETE FROM Users WHERE Email = (?)"
                    data = (email, )
                    self.cursor.execute(query, data)
                    self.commitCloseconn()
                    print(f"{'Your Account has been permanently deleted'.title()}")
                    return True
                elif choice.upper() == "N":
                    print(f'Thank You For Staying:))')
                    return False
                else:
                    print(f'Please Enter a Valid Option: ')
                    continue
        else:
            print('Please Enter a Valid Email and Try Again Then!!')

    #Function for Sign Up:-
    def signUp(self):
        print(f'{"-"*20}Create Your Account{"-"*20}')
        self.insertRecord()
        print(f'Account has been successfully created!!!')
        return
        
    #Functions for login:-
    def logInUser(self):
        print(f'{"-"*30}Login To Your Account{"-"*30}')
        print(f'Enter your Log in Credentials')
        while 1:
            email = input(f'Enter your Email: ')
            password = input(f'Enter your password: ')
            if self.checkEmail(email) and self.checkPassword(password):
                # Method Calls to Show the Main Menu To the User.
                print(f'You are logged in as a User')
                return email
            else:
                print(f'Invalid Email or Password\nDo you want to continue and Try Again? [Y/N]')
                choice = input(f'Enter your choice: ')
                if choice.upper() == 'Y':
                    continue
                elif choice.upper() == 'N':
                    return None
                else:
                    print(f'Invalid Input Try Again')
                    continue

    def logInAdmin(self):
        print(f'Enter your Log in Credentials')
        while 1:
            email = input(f'Enter your Email: ')
            password = input(f'Enter your password: ')

            if self.checkAmdinEmail(email) and self.checkAmdinPassword(password):
                print("Welcome Admin You're In !!")
                # Method Call to Show the Main Menu To the Admin.
                return True
            else:
                print(f'Invalid Email or Password\nDo you want to continue and Try Again? [Y/N]')
                choice = input(f'Enter your choice: ')
                if choice.upper() == 'Y':
                    continue
                elif choice.upper() == 'N':
                    sys.exit()

    # Function for Logout:
    def logOut(self):
        pass

# Class Book will have all of the stuff related to the Books in the Library:-
class Book:
    # here we have the constructor
    def __init__(self):
        self.getCursor()
        # making an object of class Algorithm in order to implement merge sort on the list of books
        self.algorithm = Algorithm()

    #method for creating the connection and the cursor 
    def getCursor(self):
        self.connection = sqlite3.connect("Books.db")
        self.cursor = self.connection.cursor() 

    #method for commiting and closing the dB Connection after insertion, updation, and deletion.
    def commitCloseconn(self):
        self.connection.commit()
        self.connection.close()

    # method for creating a new db table 
    def createTable(self):
        query = f"""CREATE TABLE Books(
            Quantity integer,
            Price integer,
            Title Text,
            Author Text,
            Subject Text,
            PubDate Text)"""

        self.cursor.execute(query)
        self.commitCloseconn()

    #method for taking all the info of the book from the admin:-
    def takeBookInfo(self):
        self.quantity = int(input(f'Enter the Quantity of the Book: '))
        self.price = int(input(f'Enter the Price of the Book: '))
        self.name = input(f'Enter the Title of the Book: ')
        self.author = input(f'Enter the name of the Author of the Book: ')
        self.subject = input(f'Enter the subject of the Book: ')
        self.publication_date = input(f'Enter the Publication Date of the Book: ')
    
    #method for validating the book name in the Database:-
    def checkName(self, name):
        self.getCursor()
        query = f"SELECT * FROM Books"
        self.cursor.execute(query)
        books = self.cursor.fetchall()
        for book in books:
            if book[2] == name:
                return True
        return False

    #method to add a book in the dB:-
    def insertBook(self):
        print(f'{"-"*30}Add New Book{"-"*30}')
        self.takeBookInfo()
        self.getCursor()
        query = "INSERT INTO Books VALUES (?,?,?,?,?,?)"
        data = (self.quantity, self.price, self.name, self.author, self.subject, self.publication_date)
        self.cursor.execute(query, data)
        self.commitCloseconn()

    #method to traverse the books Db:
    def traverseDb(self, books):
        count = 1
        for book in books:
            print(f'Book Number: {count}: ')
            print(f'{"-"*60}')
            for i in range(len(book)):
                if i == 0:
                    print(f'1-Quantity: {book[i]}')
                elif i == 1:
                    print(f'2-Price: {book[i]}')
                elif i == 2:
                    print(f'3-Title: {book[i]}')
                elif i == 3:
                    print(f'4-Author: {book[i]}')
                elif i == 4:
                    print(f'5-Subject: {book[i]}')
                elif i == 5:
                    print(f'6-Publication Date: {book[i]}')
            print(f'{"-"*60}')
            count += 1

    # method to show all the books 
    def showAllBooks(self):
        self.getCursor()
        query = f"SELECT * FROM Books"
        self.cursor.execute(query)
        books = self.cursor.fetchall()
        print(f'{"-"*30}All Books{"-"*30}')
        self.traverseDb(books)

    # method to get the book by name
    def getBookByName(self, name):
        self.getCursor()
        query = "SELECT * FROM Books WHERE Title = (?)"
        data = (name,)
        self.cursor.execute(query, data)
        return self.cursor.fetchall()

    # method to get all the names of the book
    def getAllNames(self):
        self.getCursor()
        query = "SELECT * FROM Books"
        self.cursor.execute(query)
        names = []
        for book in self.cursor.fetchall():
            names.append(book[2])
        str = ""
        for i in range(len(names)):
            if i >= 0 and i != len(names) - 1:
                str += f'{i+1}-{names[i]}\n'
            elif i == len(names) - 1:
                str += f'{i+1}-{names[i]}'
        return str

    # method for getting the array of names of all the books
    def getNamesArray(self):
        self.getCursor()
        query = "SELECT * FROM Books"
        self.cursor.execute(query)
        names = []
        for book in self.cursor.fetchall():
            names.append(f"{book[2].title()} By ('{book[3]}')")
        return names

    # method to display all the books with author and title
    def getAllBooks(self):
        print(f'{"-"*60}')
        print(f'{"-"*30}All Books{"-"*30}')
        print(f'{"-"*60}')
        self.getCursor()
        query = "SELECT * FROM Books"
        self.cursor.execute(query)
        books = self.cursor.fetchall()
        count = 1
        array = []
        for book in books:
            array.append(f'{book[2]} By {book[3]} --> (Quantity: {book[0]})')
        self.algorithm.merge_sort(array)
        for book in array:
            print(f'{count}- {book}')
            count += 1

    # method to print the filtered books 
    def getFilteredBooks(self, books, message):
        count = 1
        array = []
        if len(books) == 0:
            print(f'\n{"-"*60}')
            print(message)
            print(f'{"-"*60}\n')
        for book in books:
            array.append(f'{book[2]} By {book[3]} --> | Subject: {book[4]} | | Publication Date: {book[5]} |')
        self.algorithm.merge_sort(array)
        if len(books) != 0:
            print(f'The Book(s) for which you make a search are: \n{"-"*60}')
        for book in array:
            print(f'{count}- {book}\n')
            count += 1
        if len(books) != 0:
            print(f'{"-"*60}')
        # print(books)

    # method to update a Book's Info:
    def updateBook(self):
        print(f'{"-"*30}Update a Book{"-"*30}')
        print(self.getAllNames())
        name = input(f'Enter the title of the Book which you want to update: ')
        if self.checkName(name):
            self.traverseDb(self.getBookByName(name))
            while 1:
                choice = input(f'Enter |(1) to update the Quantity| |(2) to update the Price| |(3) to update the Title| |(4) to update the Author Name| |(5) to update the Subject| |(6) to update the Publication Date| |(7) to Exit|')

                if choice == '1':
                    self.getCursor()
                    quantity = int(input(f"Enter the new Quantity of the Book: "))
                    query = f"UPDATE Books SET Quantity = (?) WHERE Title = (?)"
                    data = (quantity, name)
                    self.cursor.execute(query, data)
                    self.commitCloseconn()
                    print(f'Book Quantity Changed to --> {quantity}')

                elif choice == '2':
                    self.getCursor()
                    price = int(input(f"Enter the new Price of the Book: "))
                    query = f"UPDATE Books SET Price = (?) WHERE Title = (?)"
                    data = (price, name)
                    self.cursor.execute(query, data)
                    self.commitCloseconn()
                    print(f'Book Price Changed to --> {price}')

                elif choice == '3':
                    self.getCursor()
                    title = input(f"Enter the new Title of the Book: ")
                    query = f"UPDATE Books SET Title = (?) WHERE Title = (?)"
                    data = (title, name)
                    self.cursor.execute(query, data)
                    self.commitCloseconn()
                    print(f'Book Title Changed to --> {title}')
                    
                elif choice == '4':
                    self.getCursor()
                    author = input(f"Enter the new Author Name of the Book: ")
                    query = f"UPDATE Books SET Author = (?) WHERE Title = (?)"
                    data = (author, name)
                    self.cursor.execute(query, data)
                    self.commitCloseconn()
                    print(f'Book Author Changed to --> {author}')

                elif choice == '5':
                    self.getCursor()
                    subject = input(f"Enter the new Subject of the Book: ")
                    query = f"UPDATE Books SET Subject = (?) WHERE Title = (?)"
                    data = (subject, name)
                    self.cursor.execute(query, data)
                    self.commitCloseconn()
                    print(f'Book Subject Changed to --> {subject}')


                elif choice == '6':
                    self.getCursor()
                    publication_date = input(f"Enter the new Publication Date of the Book: ")
                    query = f"UPDATE Books SET PubDate = (?) WHERE Title = (?)"
                    data = (publication_date, name)
                    self.cursor.execute(query, data)
                    self.commitCloseconn()
                    print(f'Book Publication Date Changed to --> {publication_date}')

                
                elif choice == '7':
                    break

                else:
                    print(f'Please Enter a Valid Option And Try Again :((')
                    continue
        
        else:
            print(f'Enter a Valid Book Name')

    # method to delete the Book:-
    def deleteBook(self):
        print(f'{"-"*30}Delete a Book{"-"*30}')
        print(self.getAllNames())
        name = input(f'Enter the Title which you want to delete: ')
        if self.checkName(name):
            self.getCursor()
            query = f"DELETE FROM Books WHERE Title = (?)"
            data = (name, )
            self.cursor.execute(query, data)
            self.commitCloseconn()
            print(f'The Book {name} Has Been Deleted !!')
        else:
            print(f'Please Enter a Valid Book Name')

    # method for searching for a particular book 
    def searchBooks(self):
        print(f'{"-"*60}')
        print(f'{"-"*30}Search Books{"-"*30}')
        print(f'{"-"*60}')
        self.getCursor()
        while 1:
            choice = input(f'You can search a Book by its Title, Author, Subject, Publication Date\nPress:  | (1) To search by Name | | (2) To search by Author Name |\n\t| (3) To search by Subject | | (4) To search by Publication Date | | (5) To Exit |\nSelect Appropriate Option: ')

            if choice == '1':
                title = input(f'Enter the Name of the Book which you want to search in the Library: ')
                query = f"SELECT * FROM Books WHERE Title = (?)"
                data = (title, )
                self.cursor.execute(query, data)
                message = f'Sorry This Book with Title "{title}" is Not Available'
                self.getFilteredBooks(self.cursor.fetchall(), message)


            elif choice == '2':
                author = input(f'Enter the Author Name of the Book which you want to search in the Library: ')
                query = f"SELECT * FROM Books WHERE Author = (?)"
                data = (author, )
                self.cursor.execute(query, data)
                message = f'Sorry This Book with Author Name "{author}" is Not Available'
                self.getFilteredBooks(self.cursor.fetchall(), message)

            elif choice == '3':
                subject = input(f'Enter the Subject of the Book which you want to search in the Library: ')
                query = f"SELECT * FROM Books WHERE Subject = (?)"
                data = (subject, )
                self.cursor.execute(query, data)
                message = f'Sorry This Book with the Subject "{subject}" is Not Available'
                self.getFilteredBooks(self.cursor.fetchall(), message)
            
            elif choice == '4':
                pub_date = input(f'Enter the Publication Date of the Book which you want to search in the Library: ')
                query = f"SELECT * FROM Books WHERE PubDate = (?)"
                data = (pub_date, )
                self.cursor.execute(query, data)
                message = f'Sorry This Book with the Publication Date "{pub_date}" is Not Available'
                self.getFilteredBooks(self.cursor.fetchall(), message)

            elif choice == '5':
                break

            else:
                print('Please Enter a Valid Option and Try Again: ')
                continue
            
    # method for showing books and their authors
    def showBooksAuthors(self, array):
        for i in range(len(array)):
            print(f"{i+1}- {array[i]}")
    
    # method for sort the books 
    def sortBooks(self):
        # We are using Merge sort algorithm to sort the names of all the books in the record alphabetically.
        namesArray = self.getNamesArray()

        # showing the unsorted books
        print(f'{"-"*60}')
        print(f'The Unsorted Books: ')
        print(f'{"-"*60}')
        self.showBooksAuthors(namesArray)
        print(f'{"-"*60}')

        # Applying merge sort to the list of the names of all the books 
        self.algorithm.merge_sort(namesArray)

        # showing the sorted books 
        print(f'{"-"*60}')
        print(f'\nThe Sorted Books: ')
        print(f'{"-"*60}')
        self.showBooksAuthors(namesArray)
        print(f'{"-"*60}')

    #method to check the quantity of book
    def checkQuantityIsZero(self, book):
        self.getCursor()
        query = f"SELECT * FROM Books WHERE Title = (?)"
        data = (book, )
        self.cursor.execute(query, data)
        for book in self.cursor.fetchall():
            if book[0] == 0:
                return True
            return False

# Class Algorithm will have all the algorithms that have been used:-
class Algorithm:
    def __init__(self):
        pass

    def merge_sort(self, arr):
        if len(arr) <= 1:
            return

        mid = int((0+len(arr))/2)
        left = arr[:mid]
        right = arr[mid:]
        
        self.merge_sort(left)
        self.merge_sort(right)
        self.merge_two_sorted_lists(left, right, arr)
    
    def merge_two_sorted_lists(self, a, b, arr):
        len_a = len(a)
        len_b = len(b)

        i = j = k = 0
        while i < len_a and j < len_b:
            if a[i] <= b[j]:
                arr[k] = a[i]
                i += 1
            else:
                arr[k] = b[j]
                j += 1
            k += 1
        while i < len_a:
            arr[k] = a[i]
            i += 1
            k += 1

        while j < len_b:
            arr[k] = b[j]
            j += 1
            k += 1 

# This Main class controls the whole flow of the Application. It will have objects from the classes Book and User in order to utilize their methods.
class Main():
    
    # here we have our constructor 
    def __init__(self):
        # User class Object 
        self.user = User()
        self.user.getCursor()

        # Book class Object
        self.book = Book()
        self.book.getCursor()

        try:
            self.user.createTable()
            self.book.createTable()

        except sqlite3.OperationalError:
            pass

        # Algo class Object 
        self.algorithm = Algorithm()
    
    #method for borrowing a book from the library:-
    def borrowBook(self, email):
        print(f'{"-"*60}')
        print(f'{"-"*30}Borrow a Book{"-"*30}')
        print(f'{"-"*60}')
        self.book.getAllBooks()
        borrowed_book = input(f'Enter the Title of Book you want to Borrow: ')
        if self.book.checkName(borrowed_book) :
            if not self.book.checkQuantityIsZero(borrowed_book):
                # Updating the Book's Quantity in Books dB 
                self.book.getCursor()
                query = f"SELECT * FROM Books WHERE Title = (?)"
                data = (borrowed_book,)
                self.book.cursor.execute(query, data)
                quantity = 0
                for book in self.book.cursor.fetchall():
                    quantity = book[0]
                quantity -= 1
                query_1 = f"UPDATE Books SET Quantity = (?) WHERE Title = (?)"
                data_1 = (quantity, borrowed_book)
                self.book.cursor.execute(query_1, data_1)
                self.book.commitCloseconn()

                #Adding the Borrowed Book in Users dB:-
                self.user.getCursor()
                query_2 = f"SELECT * FROM Users WHERE Email = (?)"
                data_2 = (email,)
                self.user.cursor.execute(query_2, data_2)
                # BorrowedBooks
                borrowed_books = ""
                for b_book in self.user.cursor.fetchall():
                    borrowed_books = b_book[4] + f",{borrowed_book}"

                query_3 = f"UPDATE Users SET BorrowedBooks = (?) WHERE Email = (?)"
                data_3 = (borrowed_books, email)
                self.user.cursor.execute(query_3, data_3)
                self.user.commitCloseconn()
                print(f'You have successfully borrowed {borrowed_book}')
                return

            else:
                choice = input(f'Sorry This Book is currently out of stock :(\nDo you want to reserve it?[Y/N]')
                if choice.upper() == 'Y':
                    self.reserveBook(email,borrowed_book)
                else:
                    return

        else:
            print(f'Please Enter a Valid Book Name as Mentioned Above')

    #method for seeing all Borrowed Books
    def seeBorrowBook(self, email):
        print(f'{"-"*60}')
        print(f'{"-"*30}Borrowed Books{"-"*30}')
        print(f'{"-"*60}')
        self.user.getCursor()
        array = []
        query = f"SELECT * FROM Users WHERE Email = (?)"
        data = (email,)
        self.user.cursor.execute(query, data)
        books = self.user.cursor.fetchall()
        print(f'These are the following books that you have borrowed: ')
        for b_books in books:
            borrowed_books = b_books[4]
        b_books = borrowed_books.split(',')
        if len(b_books) == 1:
            print(f'{"-"*20}You have No Borrowed Books{"-"*20}')
            return False
        else:
            for i in range(len(b_books)):
                if i == 0:
                    continue
                else:
                    array.append(f'{b_books[i]}')
            self.algorithm.merge_sort(array)
            for i in range(len(array)):
                print(f'{i+1}- {array[i]}')
            return True
    
    # method for having the array of the names of the Borrowed Books 
    def getBorrowedBooksArray(self, email):
        self.user.getCursor()
        array = []
        query = f"SELECT * FROM Users WHERE Email = (?)"
        data = (email,)
        self.user.cursor.execute(query, data)
        books = self.user.cursor.fetchall()
        for b_books in books:
            borrowed_books = b_books[4]
        b_books = borrowed_books.split(',')
        if len(b_books) == 1:
            return False
        else:
            for i in range(len(b_books)):
                if i == 0:
                    continue
                else:
                    array.append(f'{b_books[i]}')
            self.algorithm.merge_sort(array)
            return array


    #method for seeing all the Reserved Books 
    def seeReservedBook(self, email):
        print(f'{"-"*60}')
        print(f'{"-"*30}Reserved Books{"-"*30}')
        print(f'{"-"*60}')
        self.user.getCursor()
        array = []
        query = f"SELECT * FROM Users WHERE Email = (?)"
        data = (email,)
        self.user.cursor.execute(query, data)
        books = self.user.cursor.fetchall()
        print(f'\nThese are the following books that you have reserved: ')
        for b_books in books:
            reserved_books = b_books[5]
        b_books = reserved_books.split(',')
        if len(b_books) == 1:
            print(f'{"-"*20}You have No Reserved Books{"-"*20}')
        else:
            for i in range(len(b_books)):
                if i == 0:
                    continue
                else:
                    array.append(f'{b_books[i]}')
            self.algorithm.merge_sort(array)
            for i in range(len(array)):
                print(f'{i+1}- {array[i]}')

    #method for returning the book
    def returnBook(self, email):
        print(f'{"-"*60}')
        print(f'{"-"*30}Return Books{"-"*30}')
        print(f'{"-"*60}')
        # Increasing the quantity of the book that has been returned by the user 
        self.book.getCursor()
        self.seeBorrowBook(email)
        returned_book = input(f'\nEnter the Title of Book you want to Return: ')

        if self.book.checkName(returned_book):
            query_1 = "SELECT * FROM Books WHERE Title = (?)"
            data_1 = (returned_book,)
            self.book.cursor.execute(query_1, data_1)
            quantity = 0
            for book in self.book.cursor.fetchall():
                quantity = book[0]
            quantity += 1

            query_2 = "UPDATE Books SET Quantity = (?) WHERE Title = (?)"
            data_2 = (quantity, returned_book)
            self.book.cursor.execute(query_2, data_2)
            self.book.commitCloseconn()

            # Removing the returned book from user's BorrowedBooks List
            self.user.getCursor()
            query_2 = f"SELECT * FROM Users WHERE Email = (?)"
            data_2 = (email,)
            self.user.cursor.execute(query_2, data_2)
            for user in self.user.cursor.fetchall():
                borrowedBooks = user[4]
            borrowedBooks = borrowedBooks.split(',')
            borrowedBooks.remove(returned_book)

            newBorrowedBooks = ','.join(borrowedBooks)
            query_3 = f"UPDATE Users SET BorrowedBooks = (?) WHERE Email = (?)"
            data_3 = (newBorrowedBooks,email)
            self.user.cursor.execute(query_3, data_3)
            self.user.commitCloseconn()
            print(f'You have successfully returned {returned_book}')
            return

        else:
            print(f'Please Enter a Valid Book Name')
            return

    #method for reserving a book:-
    def reserveBook(self, email, book):
        self.user.getCursor()
        query_1 = f"SELECT * FROM Users WHERE Email = (?)"
        data_1 = (email, )
        self.user.cursor.execute(query_1, data_1)
        reservedBooks = ""
        for user in self.user.cursor.fetchall():
            reservedBooks = user[5] + f",{book}"
        
        query_2 = f"UPDATE Users SET ReservedBooks = (?) WHERE Email = (?)"
        data_2 = (reservedBooks, email)
        self.user.cursor.execute(query_2, data_2)
        self.user.commitCloseconn()
        print(f'The Book {book} has successfully been added in your Reserved Books. It would be added in your Borrowed Books as soon it will be available.')

    #method for renew a book
    def renewBook(self, email):
        print(f'{"-"*60}')
        print(f'{"-"*30}Renew Books{"-"*30}')
        print(f'{"-"*60}')
        if self.seeBorrowBook(email):
            while 1:
                choice = input(f'\nEnter the Title of the Book from the above list you want to Renew and Press (X) to Exit: ')
                if choice in self.getBorrowedBooksArray(email):
                    print(f'You Have Successfully Renewed the Book: {choice}')
                    break
                elif choice.upper() == "X":
                    break
                else:
                    print('Please Enter Valid Book Name')
                    continue
        else:
            print(f'Please Borrow a Book Before Renewing it!!')
            

    #method for adding the newly arrived book in the BorrowedBooks List of the User
    def addReservedBook(self, email, reserved_book):
        if self.book.checkName(reserved_book) :
            if not self.book.checkQuantityIsZero(reserved_book):
                # Updating the Book's Quantity in Books dB 
                self.book.getCursor()
                query = f"SELECT * FROM Books WHERE Title = (?)"
                data = (reserved_book,)
                self.book.cursor.execute(query, data)
                quantity = 0
                for book in self.book.cursor.fetchall():
                    quantity = book[0]
                quantity -= 1
                query_1 = f"UPDATE Books SET Quantity = (?) WHERE Title = (?)"
                data_1 = (quantity, reserved_book)
                self.book.cursor.execute(query_1, data_1)
                self.book.commitCloseconn()

                #Adding the Borrowed Book in Users dB:-
                self.user.getCursor()
                query_2 = f"SELECT * FROM Users WHERE Email = (?)"
                data_2 = (email,)
                self.user.cursor.execute(query_2, data_2)
                # BorrowedBooks
                borrowed_books = ""
                for b_book in self.user.cursor.fetchall():
                    borrowed_books = b_book[4] + f",{reserved_book}"

                query_3 = f"UPDATE Users SET BorrowedBooks = (?) WHERE Email = (?)"
                data_3 = (borrowed_books, email)
                self.user.cursor.execute(query_3, data_3)
                self.user.commitCloseconn()
                print(f'You have successfully borrowed {reserved_book}')
                return

            else:
                choice = input(f'Sorry This Book is currently out of stock :(\nDo you want to reserve it?[Y/N]')
                if choice.upper() == 'Y':
                    self.reserveBook(email,reserved_book)
                else:
                    return

        else:
            print(f'Please Enter a Valid Book Name as Mentioned Above')


    #method for removing the reserved book when it has arrived again :-
    def removeReservedBooks(self, email, book):
        self.user.getCursor()
        query_1 = f"SELECT * FROM Users WHERE Email = (?)"
        data_1 = (email,)
        self.user.cursor.execute(query_1, data_1)
        for user in self.user.cursor.fetchall():
            reservedBooks = user[5]
        reservedBooks = reservedBooks.split(',')
        reservedBooks.remove(book)

        newReservedBooks = ','.join(reservedBooks)
        query_2 = f"UPDATE Users SET ReservedBooks = (?) WHERE Email = (?)"
        data_2 = (newReservedBooks, email)
        self.user.cursor.execute(query_2, data_2)
        self.user.commitCloseconn()
        self.addReservedBook(email,book)

    
    #method for processing the reserved book i.e when the quantity of an out of stock book is increased by the admin that book is added to the borrowed books of the user
    def processReservedBooks(self, email):
        self.user.getCursor()
        query_1 = f"SELECT * FROM Users WHERE Email = (?)"
        data_1 = (email,)
        self.user.cursor.execute(query_1, data_1)
        for user in self.user.cursor.fetchall():
            reservedBooks = user[5]
        reservedBooks = reservedBooks.split(',')
        for i in range(len(reservedBooks)):
            if i == 0:
                continue
            else:
                book = str(reservedBooks[i])
                if self.book.checkQuantityIsZero(book):
                    pass
                else:
                    self.removeReservedBooks(email,book)
                    print(f"The Book: {book} which you have reserved has been arrived and added to your Borrowed Books")


    #method to display the menu for the admin:-
    def showAdminMenu(self):
        print(f'{"-"*10}WELCOME TO LIBRARY MANAGEMENT SYSTEM{"-"*10}')
    # method to process the admin menu:
    def processAdminMenu(self):
        while 1:
            print(f'{"-"*40}MENU{"-"*40}')
            print(f'Press:\n| (1) See all Books. |\n| (2) Add a Book. |\n| (3) Update a Book |\n| (4) Delete a Book |\n| (5) Search a Book |\n| (6) Sort the Books |\n| (7) See all Members |\n| (8) Delete a Member Account |\n| (9) Logout |')
            choice = input(f'Enter your choice number: ')      
            if choice == '1':
                self.book.showAllBooks()
            elif choice == '2':
                self.book.insertBook()
            elif choice == '3':
                self.book.updateBook()
            elif choice == '4':
                self.book.deleteBook()
            elif choice == '5':
                self.book.searchBooks()
            elif choice == '6':
                self.book.sortBooks()
            elif choice == '7':
                self.user.showRecords()
            elif choice == '8':
                print(f'{"-"*30}Delete a User{"-"*30}')
                (self.user.showAllEmails())
                email = input(f'Enter the email of the user you want to delete: ')
                if self.user.checkEmail(email):
                    self.user.deleteRecord(email)
                    print('User has been deleted!')
                else:
                    print('InValid Email')
            elif choice == '9':
                return
            else:
                print('Please Enter Valid and Try Again:(')

    #method to display the menu to the user:-
    def showUserMenu(self):
        print(f'{"-"*10}WELCOME TO LIBRARY MANAGEMENT SYSTEM{"-"*10}')
    
    #method to process the user menu
    def processUserMenu(self, email):
        while 1:
            print(f'{"-"*40}MENU{"-"*40}')
            print(f'Press:\n| (1) See Book Shelf |\n| (2) See Borrowed Books |\n| (3) Borrow a Book |\n| (4) See Reserved Books |\n| (5) Search a Book |\n| (6) Return a Book |\n| (7) Renew a Book |\n| (8) Logout |\n| (9) Delete the account |')
            choice = input(f'Enter your choice number: ')      
            if choice == '1':
                self.book.getAllBooks()
            elif choice == '2':
                self.seeBorrowBook(email)
            elif choice == '3':
                self.borrowBook(email)
            elif choice == '4':
               self.seeReservedBook(email)
            elif choice == '5':
                self.book.searchBooks()
            elif choice == '6':
                self.returnBook(email)
            elif choice == '7':
                self.renewBook(email)
            elif choice == '8':
                return
            elif choice == '9':
                if self.user.deleteUser():
                    return
                else:
                    continue
                
            else:
                print('Please Enter Valid Option and Try Again:(')
        

    # method to display the 5menu 
    def showMenu(self):
        print(f'{"-"*10}WELCOME TO LIBRARY MANAGEMENT SYSTEM{"-"*10}')
        print(f'Press:\n| (1) to enter as an Admin |\n| (2) to enter as a User |\n| (3) to Exit |')

    
    # this function shows the main interface of our application to the user and based on the user's i/p this method will call the appropriate other methods of classes Main, Book and User.
    def main(self):
        while 1:
            self.showMenu()
            choice = input(f'Enter the appropriate option number: ')
            if choice == '1':
                if self.user.logInAdmin():
                    self.showAdminMenu()
                    self.processAdminMenu()

            elif choice == '2':
                choice_1 = input(f'Do you already have an account? [Y/N]: ')
                if choice_1.upper() == 'Y':
                    email = self.user.logInUser()
                    if email:
                        self.processReservedBooks(email)
                        self.showUserMenu()
                        self.processUserMenu(email)

                elif choice_1.upper() == 'N':
                    self.user.signUp()
                
                
            
            elif choice == '3':
                sys.exit()
            
            else:
                print(f'Please Enter Valid Option:(')
                continue

if __name__ == "__main__":
    m = Main()
    m.main()
