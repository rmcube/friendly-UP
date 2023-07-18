import bcrypt
password=b'asdf'
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print(salt)
print(hashed)