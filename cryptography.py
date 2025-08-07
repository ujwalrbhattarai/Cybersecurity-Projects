from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from hashlib import sha256





# Function to pad text using PKCS7
def pad(text):
    pad_len = 16 - (len(text) % 16)
    return text + chr(pad_len) * pad_len





# Function to remove PKCS7 padding
def unpad(text):
    pad_len = ord(text[-1])
    return text[:-pad_len]






# Function to encrypt text using AES
def encrypt_aes(plain_text, key):
    iv = get_random_bytes(16)  # Generate a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Initialize AES cipher in CBC mode
    
    # Pad the text and encrypt
    encrypted = cipher.encrypt(pad(plain_text).encode())

    # Return IV + encrypted text, base64 encoded
    return base64.b64encode(iv + encrypted).decode('utf-8')






# Function to decrypt AES encrypted text
def decrypt_aes(encrypted_text, key):
    try:
        encrypted_data = base64.b64decode(encrypted_text)
        iv = encrypted_data[:16]  # Extract IV
        encrypted_message = encrypted_data[16:]  # Extract encrypted text

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_message).decode('utf-8')

        return unpad(decrypted)
    except Exception:
        return None  # Return None if decryption fails (invalid input)








# Main execution
