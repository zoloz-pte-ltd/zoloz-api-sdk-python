#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5  # for sign and check sign
from Crypto.Cipher import PKCS1_v1_5  # for encrypt and decrypt
import random
from Crypto import Hash
from urllib import parse
import time
import logging.handlers


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create handler
fh = logging.handlers.TimedRotatingFileHandler(filename='zoloz-api.log', when='D', interval=1, backupCount=7, encoding='utf-8')
fh.setLevel(logging.INFO)
fh.suffix="%Y%m%d.log"
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def set_logger_level(level):
    logger.setLevel(level)
    fh.setLevel(level)
    ch.setLevel(level)

# RSA encrypt
def rsa_encrypt(data_bytes, public_key_base64):
    public_key = base64.b64decode(public_key_base64)

    cipher = PKCS1_v1_5.new(RSA.importKey(public_key))
    encrypt_bytes = cipher.encrypt(data_bytes)

    encrypt = str(base64.b64encode(encrypt_bytes), "utf-8")
    url_encode_encrypt = parse.quote(encrypt, "utf-8")

    return url_encode_encrypt


# sign by RSA private key
def to_sign_with_private_key(plain_text, private_key_base64):
    private_key = base64.b64decode(private_key_base64)

    # 私钥签名
    signer_pri_obj = sign_PKCS1_v1_5.new(RSA.importKey(private_key))
    rand_hash = Hash.SHA256.new()
    rand_hash.update(plain_text.encode("utf-8"))
    sign_bytes = signer_pri_obj.sign(rand_hash)

    signature = str(base64.b64encode(sign_bytes), "utf-8")
    url_encode_signature = parse.quote(signature, "utf-8")

    return url_encode_signature


# build content to sign
def build_sign_content(api, merchant_id, request_time, data):
    signature_content = "POST /api/" + api.replace(".", "/") + "\n" \
                   + merchant_id + "." + request_time + "." + data

    return signature_content


# AES/ECB/PKCS5Padding
# AES encrypt
def aes_encrypt(key, content):
    BLOCK_SIZE = 16  # Bytes
    # fill pad，不足16*N个字节，填充字符为chr(填充个数)
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

    message = pad(content)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypt_bytes = cipher.encrypt(message)
    result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')

    return result


# AES decrypt
def aes_decrypt(key, content):
    BLOCK_SIZE = 16  # Bytes
    # remove pad
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    cipher = AES.new(key, AES.MODE_ECB)
    aessource = cipher.decrypt(base64.b64decode(content))

    return unpad(aessource).decode('utf8')


# generate AES key
def generate_aes_key(n):
    c_length = int(n / 8)
    source = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    length = len(source) - 1
    result = ''
    for i in range(c_length):
        result += source[random.randint(0, length)]

    return bytes(result, "utf-8")


# ZOLOZ OpenAPI Client
class ApiClient:
    server_url = ""
    merchant_id = ""
    merchant_rsa_private_key_base64 = ""
    server_rsa_public_key_base64 = ""
    signed = True
    encrypted = True

    def __init__(self, server_url, merchant_id, merchant_rsa_private_key_base64, server_rsa_public_key_base64):
        self.server_url = server_url
        self.merchant_id = merchant_id
        self.merchant_rsa_private_key_base64 = merchant_rsa_private_key_base64
        self.server_rsa_public_key_base64 = server_rsa_public_key_base64

    def call_api(self, api, request, timeout=10):
        headers = {}
        url = self.server_url + "/api/" + api.replace(".", "/")
        logger.info("api url=%s", url)
        request_time = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())

        data = ""
        # encrypt
        if self.encrypted:
            aes_key = generate_aes_key(128)
            encrypt = rsa_encrypt(aes_key, self.server_rsa_public_key_base64)
            data = aes_encrypt(aes_key, request)
            headers["Encrypt"] = "algorithm=RSA_AES, symmetricKey=" + encrypt
            headers["Content-Type"] = "text/plain; charset=UTF-8"
        else:
            headers["Content-Type"] = "application/json; charset=UTF-8"

        # signature
        if self.signed:
            signature_content = build_sign_content(api, self.merchant_id, request_time, data)
            signature = to_sign_with_private_key(signature_content, self.merchant_rsa_private_key_base64)
            headers["Signature"] = "algorithm=RSA256, signature=" + signature

        # set headers
        headers["Client-Id"] = self.merchant_id
        headers["Request-Time"] = request_time
        for k, v in headers.items():
            logger.debug("Request header. %s=%s", k, v)
        logger.debug("Request data=%s", data)

        # send request
        start_time = int(round(time.time() * 1000))
        resp = requests.post(url, data, headers=headers, timeout=timeout)
        used_time = int(round(time.time() * 1000)) - start_time
        logger.info("Received response. api=%s used_time=%d", api, used_time)
        for k, v in resp.headers.items():
            logger.debug("Response header. %s=%s", k, v)
        response = resp.text
        logger.debug("Request data=%s", data)

        # decrypt response
        if self.encrypted:
            response = aes_decrypt(aes_key, resp.text)
            logger.debug("Decrypted response=%s", response)

        return response