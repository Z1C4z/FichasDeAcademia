class User:
    def __init__(self, name=None, birth=None, gender=None, home=None, phone=None, email=None):
        self.name = name
        self.birth = birth
        self.gender = gender
        self.home = home
        self.phone = phone
        self.email = email

class Client(User):
    def __init__(self, name=None, birth=None, gender=None, home=None, phone=None, email=None,
                 height=None, weight=None, meta=None, initDate=None):
        super().__init__(name, birth, gender, home, phone, email)
        self.height = height
        self.weight = weight
        self.meta = meta
        self.initDate - initDate

class Trainer(User):
    def __init__(self, name=None, birth=None, gender=None, home=None, phone=None, email=None):
        super().__init__(name, birth, gender, home, phone, email)
        self.skillArea