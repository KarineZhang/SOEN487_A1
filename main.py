from flask import jsonify, make_response, request
from app import app

import sqlalchemy
import models


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    return jsonify({"title": "SOEN487 Assignment 1",
                    "student": {"id": "Your id#", "name": "Your name"}})


@app.route("/user", methods={"PUT"})
def put_user():
    # get the name first, if no name then fail

    card = request.form.get("card")
    dob = request.form.get("dob")
    name = request.form.get("name")
    address = request.form.get("address")
    telephone = request.form.get("telephone")
    email = request.form.get("email")
    limit_books = request.form.get("limit_books")

    if not name and not card and not address and not telephone and not dob and not limit_books and not email:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put user. Missing mandatory fields."}), 403)
    user_id = request.form.get("id")
    if not user_id:
        p = models.User(name=name, card=card, address=address, telephone=telephone, dob=dob,
                        limit_books=limit_books, email=email)
    else:
        p = models.User(id=user_id, name=name, card=card,
                        address=address, telephone=telephone, dob=dob, limit_books=limit_books,
                        email=email)

    models.db.session.add(p)
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put user. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "Successfully added user."})


@app.route("/user")
def get_all_user():
    user_list = models.User.query.all()
    return jsonify([models.row2dict(user) for user in user_list])


@app.route("/user/<user_id>")
def get_user(user_id):
    # id is a primary key, so we'll have max 1 result row
    user = models.User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(models.row2dict(user))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this user id."}), 404)


@app.route("/user/<user_id>", methods={"DELETE"})
def delete_user(user_id):
    models.db.session.query(models.User).filter(models.User.id == user_id).delete()
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete this user. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "successfully deleted user."})


@app.route("/user", methods={"DELETE"})
def delete_all_user():
    models.db.session.query(models.User).delete()
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete this user. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "successfully deleted all users."})


@app.route("/book", methods={"PUT"})
def put_book():

    book_code = request.form.get("book_code")
    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")

    if not book_code and not title and not author and not year:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put book. Missing mandatory fields."}), 403)
    book_id = request.form.get("id")
    if not book_id:
        p = models.Book(book_code=book_code, title=title, author=author, year=year)
    else:
        p = models.Book(id=book_id, book_code=book_code, title=title, author=author, year=year)

    models.db.session.add(p)
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put book. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "Successfully added book."})


@app.route("/book")
def get_all_book():
    book_list = models.Book.query.all()
    return jsonify([models.row2dict(book) for book in book_list])


@app.route("/book/<book_id>")
def get_book(book_id):
    # id is a primary key, so we'll have max 1 result row
    book = models.Book.query.filter_by(id=book_id).first()
    if book:
        return jsonify(models.row2dict(book))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this book id."}), 404)


@app.route("/book/<book_id>", methods={"DELETE"})
def delete_book(book_id):
    models.db.session.query(models.Book).filter(models.Book.id == book_id).delete()
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete this book. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "successfully deleted book."})


@app.route("/book", methods={"DELETE"})
def delete_all_book():
    models.db.session.query(models.Book).delete()
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete this book. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "successfully deleted all books."})


@app.route("/library", methods={"POST"})
def put_library():

    name = request.form.get("name")
    address = request.form.get("address")
    telephone = request.form.get("telephone")
    email = request.form.get("email")

    if not name and not address and not telephone and not email:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put library. Missing mandatory fields."}), 403)
    library_id = request.form.get("id")
    if not library_id:
        p = models.Library(name=name, address=address, telephone=telephone, email=email)
    else:
        p = models.Library(id=library_id, name=name, address=address, telephone=telephone, email=email)

    models.db.session.add(p)
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put library. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "Successfully added library."})


@app.route("/library")
def get_all_library():
    library_list = models.Library.query.all()
    return jsonify([models.row2dict(library) for library in library_list])


@app.route("/library/<library_id>")
def get_library(library_id):
    # id is a primary key, so we'll have max 1 result row
    library = models.Library.query.filter_by(id=library_id).first()
    if library:
        return jsonify(models.row2dict(library))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this library id."}), 404)


@app.route("/library/<library_id>", methods={"DELETE"})
def delete_library(library_id):
    models.db.session.query(models.Library).filter(models.Library.id == library_id).delete()
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete this library. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "successfully deleted library."})


@app.route("/library", methods={"DELETE"})
def delete_all_library():
    models.db.session.query(models.Library).delete()
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete this library. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "successfully deleted all libraries."})


if __name__ == '__main__':
    app.run()
