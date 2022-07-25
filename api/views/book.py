from flask import jsonify, Blueprint, request,current_app
from ..controller import user_register_controller, take_book_controller, book_register_controller, drop_book_controller
from celery.utils.log import get_task_logger
from api import celery


logger = get_task_logger(__name__)
book = Blueprint("book", __name__)


#data example {"username":"ali","email":"ali@ali.com"}
@book.route('/user_register', methods=['POST'])
def user_register():
    data = request.get_json()
    flag = user_register_controller(data)
    if flag:
        return jsonify({'result': "OK"})
    return jsonify({'result': "error in data"}), 400

#data example {"name":"book1"}
@book.route('/book_register', methods=['POST'])
def book_register():
    data = request.get_json()
    flag = book_register_controller(data)
    if flag:
        return jsonify({'result': "OK"})
    return jsonify({'result': "error in data"}), 400

#data example {"book_name":"book1","user":"ali"}
@book.route('/take_book', methods=['POST'])
def take_book():
    data = request.get_json()
    flag, error_msg = take_book_controller(data)
    if flag:
        return jsonify({'result': "OK"})
    return jsonify({'result': error_msg}), 400

#data example {"book_name":"book1","user":"ali"}
@book.route('/drop_book', methods=['POST'])
def drop_book():
    data = request.get_json()
    flag, error_msg = drop_book_controller(data)
    if flag:
        return jsonify({'result': "OK"})
    return jsonify({'result': error_msg}), 400

#data example {"book_name":"book1","user":"ali"}
@book.route('/take_book_with_celery', methods=['POST'])
def send_book():
    data = request.get_json()
    send_book.delay(data)
    return jsonify({'result': "task added queue"})


@celery.task(name="book.send_book")
def send_book(data):
    flag, error_msg = take_book_controller(data)
    return error_msg

