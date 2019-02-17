from app import db


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_code = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text(), nullable=False)
    author = db.Column(db.Text(), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'))

    def __repr__(self):
        return "<Book{}: {}, title: {}, author: {}, year: {}>".format(self.id,
                                                                      self.book_code,
                                                                      self.title,
                                                                      self.author,
                                                                      self.year)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)
    address = db.Column(db.Text(), nullable=False)
    telephone = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    limit_books = db.Column(db.Integer, nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)

    def __repr__(self):
        return "<User{}: {}, dob: {}, name: {}, address: {}, telephone: {}, email: {}, limit_books: {}>".\
            format(self.id,
                   self.card,
                   self.dob,
                   self.name,
                   self.address,
                   self.telephone,
                   self.email,
                   self.limit_books)

    # def return_book(self, library, book):
    #     if self.card_number:
    #         self.books.remove(book)
    #         book.user_id = None
    #         self.limitbooks -= 1
    #         library.books.append(book)
    #         book.library_id = library.id
    #
    def borrow(self, library, book):
        if self.limit_books > 10:
            raise ValueError
        if self.card_number:
            library.books.remove(book)
            book.library_id = None
            self.limitbooks += 1
            self.books.append(book)
            book.user_id = self.id
            db.session.commit()


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False)
    address = db.Column(db.Text(), nullable=False)
    telephone = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    books = db.relationship('Book', backref='library', lazy=True)

    def __repr__(self):
        return "<Library{}: {}, address: {}, telephone: {}, email: {}>".format(self.id,
                                                                               self.name,
                                                                               self.address,
                                                                               self.telephone,
                                                                               self.email)

    def storage(self, book):
        self.books.append(book)
        db.session.commit()

    def lend(self, user, book):
        if user.limit_books > 10:
            raise ValueError
        if user.card_number:
            self.books.remove(book)
            book.library_id = None
            user.limit_books += 1
            user.books.append(book)
            book.user_id = user.id


db.create_all()
db.session.commit()

