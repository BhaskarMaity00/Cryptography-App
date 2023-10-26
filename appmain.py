from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os,random

def generate_key():
    import main_genalgo
    try:
        return main_genalgo.gen_algo.genetic_algorithm(os.urandom(16).decode('cp1252'))
    except:
        return generate_key()
    
def ciphertext(key):
    
    iv = b'\xc7\xe5\xe1\x17\x1f\xfb\xca\xa6\x7fR>\xa4\xe7\xab\x88a'
    # print("iv: ",iv.decode('cp1252'))
    cipher = Cipher(algorithms.AES(key.encode('cp1252')), modes.CBC(iv), backend=default_backend())
    return cipher
        
def encrypt(plaintext,cipher):
    plaintext=plaintext.encode("cp1252")
    # Create a padder for PKCS7 padding
    padder = padding.PKCS7(128).padder()
    # Pad the plaintext
    padded_data = padder.update(plaintext) + padder.finalize() 
        # Create an encryptor object
    encryptor = cipher.encryptor()

        # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

def decrypt(ciphertext,cipher):
    # ciphertext=ciphertext.encode("cp1252")
        # Create an unpadder for PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()
        # Create a decryptor object
    decryptor = cipher.decryptor()
        # Decrypt the ciphertext
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        # Unpad the decrypted data
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext.decode()

def run_encryption(plaintext):
    try:
        key = generate_key()
        cip = ciphertext(key)
        enc_txt = encrypt(plaintext,cip)
        return key,enc_txt
    except:
        return run_encryption(plaintext)


def run_decrypt(key,enc_txt):
    cip=ciphertext(key)
    return decrypt(enc_txt,cip)


