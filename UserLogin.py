from flask_login import UserMixin

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    # def is_authenticated(self): #метод за замовченням реалізовані в класі UserMixin
    #     return True
    #
    # def is_active(self): #метод за замовченням реалізовані в класі UserMixin
    #     return True
    #
    # def is_anonymous(self): #метод за замовченням реалізовані в класі UserMixin
    #     return False

    def get_id(self):
        return str(self.__user['id'])
