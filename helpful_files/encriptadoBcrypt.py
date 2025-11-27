import bcrypt

def encrypt_password(password_str: str) -> bytes:
    # Byte converting
    passwd_bytes = password_str.encode()

    # Generate salt and hash
    salt = bcrypt.gensalt() 
    generated_hash = bcrypt.hashpw(passwd_bytes, salt)

    # This is the thing we should store in the database
    return generated_hash

def verify_password(password_str: str, stored_hash: bytes) -> bool:
    passwd_bytes = password_str.encode()
    return bcrypt.checkpw(passwd_bytes, stored_hash)

password = "holaaa"
hash_for_db = encrypt_password(password) #this will be stored in the database

password_login = "holiii"   # what I try to insert as a password

if verify_password(password_login, hash_for_db):
    print("Contraseña correcta")
else:
    print("Contraseña incorrecta")
