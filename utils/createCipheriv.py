import sys
import logging

from hashlib import md5
from Crypto.Cipher import AES
from dotenv import dotenv_values

config = dotenv_values(".env")
logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s",
    level=int(config["VERBOSE"]),
    stream=sys.stdout,
)

"""
Encryption based on aes-256-cbc algorithm
This is made to be compatible with node "crypto.createCipheriv"
The returned crypto is a hex to allow it to be used in links etc
"""

CRYPTO_KEY: str = "12345678901234567890123456789012"
INT_VECTOR: str = "1234567890123456"


class AES_Encoder:
    """
    The class takes a key: str and init vector (iv:string), these must be the same in the node createCipheriv
    The class can then be used with encrypt_token and decrypt_token to get the information

    The key MUST BE 32 bits / characters long
    The initVector must be 16 bits / characters long
    """

    def __init__(self, key: str = None, iv: str = None) -> None:
        if key is not None and iv is not None:
            self.key = key
            self.iv = iv
        else:
            self.key = CRYPTO_KEY
            self.iv = INT_VECTOR

    def _pad(self, s):  # padding to ensure the length is correct
        return s + (AES.block_size - len(s) % AES.block_size) * chr(
            AES.block_size - len(s) % AES.block_size
        )

    def _cipher(self):
        return AES.new(key=self.key, mode=AES.MODE_CBC, IV=self.iv)

    def unpad(self, s):
        return s[: -ord(s[len(s) - 1 :])]

    def encrypt_token(self, data: str):
        return self._cipher().encrypt(self._pad(data)).hex()

    def decrypt_token(self, data: str):
        data = bytes.fromhex(data)
        return self._cipher().decrypt(data).decode("utf-8")


if __name__ == "__main__":
    encoders = AES_Encoder()
    encrypted_data = encoders.encrypt_token("Testing Encryption")
    logging.info(encrypted_data)

    decrypted_data = encoders.decrypt_token(encrypted_data)
    logging.info(decrypted_data)
