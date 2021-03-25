#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import zoloz
import json
import logging

zoloz.set_logger_level(logging.DEBUG)
# production host is https://sg-production-api.zoloz.com
# change the clientId to your clientId
# input your merchantPrivateKey Base64 String and your ZOLOZPublicKey Base64 String here.
zoloz_api_client = zoloz.ApiClient("https://sg-sandbox-api.zoloz.com",
                               "2188455383736145",
                               "yourMerchantPrivateKeyBase64String",
                               "yourZOLOZPublicKeyBase64String"
                            )
# change the request content and api to the real one you are going to use.
request = {
    "title": "hello",
    "description": "just for demonstration."
}
response = zoloz_api_client.call_api("v1.zoloz.authentication.test", json.dumps(request))
print(response)







