class User:
    name: str
    email: str
    password_hash: str
    password_salt: str

    def __init__(self, name, email, password_hash, password_salt):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.password_salt = password_salt

    def __repr__(self):
        return "<User email:%s password_hash:%s password_salt:%s>" % (self.email, self.password_hash, self.password_salt)

