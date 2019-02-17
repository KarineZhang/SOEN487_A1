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
    return jsonify({"code": 200, "msg": "success"})


if __name__ == '__main__':
    app.run()
