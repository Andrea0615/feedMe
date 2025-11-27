import bcrypt

def hash_password(password_str: str) -> bytes:
    # Byte converting
    passwd_bytes = password_str.encode()

    # Generate salt and hash
    salt = bcrypt.gensalt() 
    generated_hash = bcrypt.hashpw(passwd_bytes, salt)

    # This is the thing we should store in the database
    return generated_hash.decode() #el decode para guardarlo como string

def verify_password(password_str: str, stored_hash: str) -> bool:
    passwd_bytes = password_str.encode()
    stored_hash_bytes = stored_hash.encode()
    return bcrypt.checkpw(passwd_bytes, stored_hash_bytes)
