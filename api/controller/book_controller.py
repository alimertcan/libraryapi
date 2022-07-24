from ..mongoclient import MongoClient
from ..model import schema_user, schema_book, schema_take_book,schema_drop_book
from jsonschema import validate, exceptions

mongoclient = MongoClient.get_instance()


def user_register_controller(data):
    db_client = mongoclient['Library']['users']
    try:
        validate(data, schema_user)
        ack = db_client.insert_one(data)
        return ack.acknowledged
    except exceptions.ValidationError as ex:
        print(ex)

    return False


def take_book_controller(data):

    db_client = mongoclient['Library']['books']
    db_client2 = mongoclient['Library']['users']
    try:
        validate(data, schema_take_book)
        username = data["user"]
        book_name = data["book_name"]
        check = db_client2.find({"username": username})
        user_data = list(check)
        check2 = db_client.find({"name": book_name})
        book_data = list(check2)
        reserve_list = []
        if len(user_data) > 0 and len(book_data) > 0:
            if book_data[0]['is_taken'] == False:
                if "list_of_books" not in user_data[0]:
                    reserve_list.append(book_name)
                else:
                    reserve_list = user_data[0]['list_of_books']
                    if book_data not in reserve_list:
                        reserve_list.append(book_name)
                db_client2.update_many({"username": data["user"]}, {"$set": {"list_of_books": reserve_list}})
                db_client.update_one({"name": book_name}, {"$set": {"is_taken": True}})
                return True,"OK"
            else:
                return False,"Book is already taken"
        else:
            return False,"User or book does not exist"
    except exceptions.ValidationError as ex:
        print(ex)

    return False,"Error in data"


def book_register_controller(data):
    db_client = mongoclient['Library']['books']
    if "is_taken" not in data:
        data['is_taken'] = False
    try:
        validate(data, schema_book)
        ack = db_client.insert_one(data)
        return ack.acknowledged
    except exceptions.ValidationError as ex:
        print(ex)

    return False


def drop_book_controller(data):
    db_client = mongoclient['Library']['books']
    db_client2 = mongoclient['Library']['users']
    try:
        validate(data, schema_drop_book)
        username = data["user"]
        book_name = data["book_name"]
        check = db_client2.find({"username": username})
        user_data = list(check)
        if len(user_data) > 0:
            reserve_list = user_data[0]['list_of_books']
            if book_name in reserve_list:
                check2 = db_client.find({"name": book_name})
                book_data = list(check2)
                reserve_list.remove(book_name)
                if len(book_data)>0:
                    db_client.update_one({"name": book_name}, {"$set": {"is_taken": False}})
                    db_client2.update_many({"username": data["user"]}, {"$set": {"list_of_books": reserve_list}})
                    return True,"Ok"
            else:
                return False,"book is not belong to user"
        else:
            return False,"Error in data"

    except exceptions.ValidationError as ex:
        print(ex)

    return False,"Error in data"
