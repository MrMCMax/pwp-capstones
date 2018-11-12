class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}         #Book:rating

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print(self.name + "'s email has been updated")

    def __repr__(self):
        return str(self.name) + ", user of Tome Rater. Email: " + str(self.email) + ", books read: " + str(len(self.books))

    def __eq__(self, other_user):
        return ((type(other_user) == type(self)) and (other_user.email == self.email)) and (other_user.name == self.name)
    
    #other methods
    
    def read_book(self, book, rating=None):
        self.books[book] = rating
    
    def get_average_rating(self):
        avg = 0
        number_of_ratings = 0
        for i in self.books.values():
            if (i != None):
                avg += i
                number_of_ratings += 1
        if (number_of_ratings == 0):
            return 0
        else:
            return (avg / number_of_ratings)
    
    
#Class Book
class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []       #List of ratings for this book
        
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self, isbn):
        self.isbn = isbn
        print("Book {} has changed its isbn".format(self.title))
        
    def add_rating(self, rating):
        if rating == None:
            pass
        elif (rating < 0) or (rating > 4):
            print("Invalid rating")
        else:
            self.ratings.append(rating)
            
    def __repr__(self):
        return "\"{title}\", ISBN: {isbn}".format(title = self.title, isbn = self.isbn)
    
    def __eq__(self, other):
        return ((type(self) == type(other)) and (self.title == other.title)) and (self.isbn == other.isbn)
    
    #other_methods
    
    def get_average_rating(self):
        if (len(self.ratings) == 0):
            return 0
        else:
            total_sum = 0
            for i in self.ratings:
                total_sum += i
            return (total_sum / len(self.ratings))
    
    def __hash__(self):
        return hash((self.title, self.isbn))
    
    
#Class Fiction, inherits from Book
class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author
    
    def get_author(self):
        return self.author
    
    def __repr__(self):
        return "\"{title}\" by {author}".format(title = self.title, author = self.author)
    
    
    
#Class Non_Fiction, inherits from Book
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level
        
    def get_subject(self):
        return self.subject
    
    def get_level(self):
        return self.level
    
    def __repr__(self):
        #Custom modification to write the plural form correctly
        ch = self.level[0].lower()
        n = ""
        if (ch == 'a') or (ch == 'e') or (ch == 'i') or (ch == 'o') or (ch == 'u'):
            n = "n"
        return "\"{title}\", a{n} {level} manual on {subject}".format(title = self.title, n=n, level = self.level, subject = self.subject)
    
    
#Class TomeRater
class TomeRater(object):
    def __init__(self):
        self.users = {}     #email:User
        self.books = {}     #Book:Nº of times read
    
    def create_book(self, title, isbn):
        book = Book(title, isbn)
        return book
    
    def create_novel(self, title, author, isbn):
        novel = Fiction(title, author, isbn)
        return novel
    
    def create_non_fiction(self, title, subject, level, isbn):
        book = Non_Fiction(title, subject, level, isbn)
        return book
    
    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email)
        if user == None:
            print("No user with email {}".format(email))
        elif (not(book in self.books.keys()) and book.get_isbn() in [b.get_isbn() for b in self.books.keys()]):
            print("There is already a book with the given isbn")
        else:
            user.read_book(book, rating)
            book.add_rating(rating)
            #If it exists, gets the value and adds one. If it doesn`t,
            #gets a 0 and adds one to it.
            self.books[book] = self.books.get(book, 0) + 1
    
    def add_user(self, name, email, user_books=None):
        if (email in self.users):
            print("This user already exists. Please use this function to add new users only.")
        elif not("@" in email) or not((".com" in email) or (".org" in email) or (".edu" in email)):
            print("Not a valid email: {email}".format(email=email))
        else:
            new_user = User(name, email)
            self.users[email] = new_user
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)
            
            
    #Analysis methods
    def print_catalog(self):
        for book in self.books.keys():
            print(book)
            
    def print_users(self):
        for user in self.users.values():
            print(user)
            
    def get_most_read_book(self):
        maxBook = None
        maxRead = 0
        for key, value in self.books.items():
            if value > maxRead:
                maxBook = key
                
        return maxBook
    
    def highest_rated_book(self):
        maxBook = None
        #Rating will never be negative: [0..4].
        #Zero is the lowest value possible
        maxRating = 0
        for book in self.books.keys():
            rating = book.get_average_rating()
            if rating > maxRating:
                maxRating = rating
                maxBook = book
                
        return maxBook
    
    def most_positive_user(self):
        maxUser = 0
        maxRating = 0
        for user in self.users.values():
            rating = user.get_average_rating()
            if rating > maxRating:
                maxRating = rating
                maxUser = user
                
        return maxUser
    
    #Custom methods
    #Print Tome_Rater!
    def __repr__(self):
        text = "List of users: \n"
        string_users = [str(user) for user in self.users.values()]
        text += '\n'.join(string_users)
        text += "\nBooks in TomeRater: \n"
        for book, n in self.books.items():
            text += str(book) + ", {} times read\n".format(n)
        return text
    
    
            
            
            
            