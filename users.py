class User:
    def __init__(self, name=None, password=None, birth=None, gender=None, home=None, phone=None, email=None, monthly=None):
        self.name = name
        self.ID
        self.password = password
        self.birth = birth
        self.gender = gender
        self.home = home
        self.phone = phone
        self.email = email
        self.monthly = monthly

class Client(User):
    def __init__(self, name=None, birth=None, gender=None, home=None, phone=None, email=None,
                 height=None, weight=None, meta=None, initDate=None):
        super().__init__(name, birth, gender, home, phone, email)
        self.height = height
        self.weight = weight
        self.meta = meta
        self.initDate = initDate

class Trainer(User):
    def __init__(self, name=None, birth=None, gender=None, home=None, phone=None, email=None):
        super().__init__(name, birth, gender, home, phone, email)
        self.skillArea

class Excercise:
    def __init__(self, name=None, muscle=None, item=None, series=0, retps=0, kg=0):
        self.name = name
        self.muscle = muscle
        self.item = item 
        self.series = series
        self.repts = retps
        self.kg = kg