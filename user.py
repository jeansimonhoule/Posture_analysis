class User:
    currentUser = ""
    def __init__(self):
        pass

User.currentUser = "jean"

allo = User()
print(allo.currentUser)