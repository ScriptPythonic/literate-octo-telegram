from .mongo import users_collection, uploads_collection, messages_collection
from datetime import datetime, timedelta

class User:
    def __init__(self, matric_no, full_name, phone_number, email, password, picture=None, address=None, reg_officer_no=None, department=None, level=None, last_update=None, is_active=True):
        self.matric_no = matric_no
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.picture = picture or 'https://th.bing.com/th/id/R.d8be3ebdc1ed3c6b13ffbeee0b20fa3c?rik=h%2bwbaNZzYT67Gg&pid=ImgRaw&r=0'
        self.address = address
        self.reg_officer_no = reg_officer_no
        self.department = department
        self.level = level
        self.last_update = last_update or datetime.utcnow()
        self.is_active = is_active

    def save(self):
        return users_collection.insert_one(self.__dict__)

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({'email': email})

    def can_update_profile(self):
        if self.last_update is None:
            return True
        return datetime.utcnow() >= self.last_update + timedelta(weeks=1)

class Upload:
    def __init__(self, title, description, category, file_url, user_id):
        self.title = title
        self.description = description
        self.category = category
        self.file_url = file_url
        self.user_id = user_id

    def save(self):
        return uploads_collection.insert_one(self.__dict__)

class Message:
    def __init__(self, sender_id, receiver_id, content, timestamp=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.timestamp = timestamp or datetime.utcnow()

    def save(self):
        return messages_collection.insert_one(self.__dict__)
