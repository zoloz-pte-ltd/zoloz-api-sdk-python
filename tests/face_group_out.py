#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import zoloz
import json
import logging

zoloz.set_logger_level(logging.DEBUG)
zoloz_api_client = zoloz.ApiClient("http://127.0.0.1:8341",
                               "2189400000000204",
                               "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCWXW4J5Q11/f8TBb0/zDz/FQDMVx5Y4qNxzQR3BAUXzejkDhueeuOsP0NF1B5l3/H55ALAyuVE5SORHudYkL5ITkVnQGLYnvTTKLnSinHNW5A4iLZWWe/0VP/4L+y8wtlTeTakrpLBnvwm/ipk2/GEGjdI68MYRNfKdLljENP5fRbjNMT7Ys8i/SnoPjkGavcZXyYTFqrLqPqCdL2w/ZmNRzLw1BTtqgL90bX83ZPfL4uWjCtgpfpQcsdxr4XOFi1g6iHE6Gi2y5PzascHoMxOKbFc2itC0NIaOuY4LMFHpBSD+D80uXugLpqG/bx3yAbfOM19E7II1r+WxzCNPpkPAgMBAAECggEAHhhTFt3mZNBShj8m0qcRKkjM4RkqtMWfyv4qv5tpXYtT6pk8Q+r6uJXs5AQBlYhOCSLuviGd470s8jXKPfqyawxnbbQAVLTz8XN8Rbx57I0//2C1hfD4SuHcXZNSAbHKB6ACJNHgA6rLcw5587flzfflSs4NPUVCH35fQIm0s4FcGbjVdvTo05+bsWi+xcexs7pjlzIvr8L5QoURpK9yYddXHi5cq6D5JkkpvmoFCMRR0kV1i2r+3SHWWfyZp5Aj1U0N/x13FJkEpNKiOGXR9Te6XYNeo8JvjNzgKfa+Ag0NwQQre9RljrsH6Ti5XtfTMMz8ukxqD5plKlDAlyxJuQKBgQDTiZVTsDeuheXpdxZOsRNk7ma5iAxKXjKTSdtMQxRpXishRaTAnX1H14MvLX4xXuBd8Bgu6IVEellOQgQVmWzpeB7yCHPieQ+LWSiFCUzU842kSg3KqrILAeX6GIQFNfQZXPvmVhcZZ5yV517IpjLOTE8FzJlDXFkdFyJuT6IP/QKBgQC1+EZnZxvonCVCLbyg9cKISMBEsr3kp2oCfGnRurUJ1ALksS/H+BVfuoKYshAta4likV6eeruCzDrbYMFI0WJLgyI0l61BZ5iHMNMNEE1S2OhyiSwLhMIbSLmHu61XVAD6n7ydkXy/fRT2WhcV3TsDq+kbLRHf47vHwvVJTCJc+wKBgQCLlZTIlVYYvlgYtzEsGeKPTlTQhjp99CxxTmH7r6PPZ4kUOm1dgE6D0mzI+77yewWYVu7OPTZ7GjTF0//39LaOVGovEW7OeU3NiLaZGqrtNg035Hm3Su2TH9yOLBEpkxGQju/VbOdvJxSHQhYkVq7dvDLEw946Oby/2l0o5zksTQKBgGhRFfs9LtCggvN3SMV1XbnHCwHW/elQ2ALo07j5scMamTYFJYEbhRVF1Iw4t/FxzmaFM5rifRA0iCEvTF60OgdT+43uzdHK07Pcl4DLsagm1MqkPG22A5ikjkdznaGMdKs4W2Zw+vTDffrkFovgMW6fZJjBs5eH9CRGbVtBnAl1AoGAd4JJ/VHvZUoL9g7iumbcPRn0ihqnaFXl1qe6418wKLgq8yfqD3xJARmTgelBRIUsJYvf4YOKFokheNqx5S0QSZ2zIWFKhjZOOhoVQXVsfxWDUxnrOS3cEKrmkL1ldoZ5tSH3VcMa+9ZLcCSBaCSjvyjOLzSGA7BGLgYbe1Yc1ho=",
                               "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyyUPfCsT5GWzjin/Sz95QGCKU2xFHphHlvTWCt5MO4GFwgHGQl5MK5sDoBvcc5TeK9cExv2br5kE+FGgJm/EUzhZf/OqranxKKcyfEsm0OYiw4i1kP5yL41G1avmU3v0T/eHVz/CoOG39HwXUvCoAF7jLi1+ilOdwzahOIhkslEVSoHHsiotUQPrEdCKzRS0HmCMHK1fh3GC4wnYrRCW3f4LaZk0ZZSd7nOD0NR3c9ibYrL0eP61YSs9b/cgyKuGOFwolFNdav2b+OL/RpN2/pJmCvh7/ZW40MzDwAHEErK63rpoSwvUFIGZKPdITuTd2UrRQhZP/ltQGL/V21v97wIDAQAB"
                            )
request = {
    "uid": "223344",
    "groupId": "default"
}
response = zoloz_api_client.call_api("v1.zoloz.face.groupout", json.dumps(request))
print(response)







