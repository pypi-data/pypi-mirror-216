import requests
import json as js


# service_ip = "121.41.5.216"
# service_port = "5555"
# proxies = {
#     "http": "http://{}:{}".format(service_ip, service_port),
#     "https": "https://{}:{}".format(service_ip, service_port),
# }


def getRequest(url=None, params=None, headers=None):
    try:
        response = requests.get(url=url, params=params, headers=headers)
        response.encoding = response.apparent_encoding
        return response
    except:
        print("请求{}失败返回空".format(url))
        return None

# def postRequest(url: object = None, data: object = None, json: object = None, headers: object = None,
#                 resType: object = True) -> object:
#     """
#
#     :rtype:
#     """
#     try:
#         response = requests.post(url=url, data=data, json=json, headers=headers)
#         response.encoding = response.apparent_encoding
#         if resType:
#             return response.json()
#         return js.loads(response.text)
#     except Exception as e:
#         print("{}请求失败,param:{} e:{}".format(url, json if json else data, e))
#         return None
#
#
# def deleteRequest(url=None, params=None, headers=None):
#     try:
#         response = requests.delete(url=url, params=params, headers=headers)
#         response.encoding = response.apparent_encoding
#         return response.json()
#     except:
#         print("{}请求失败返回空".format(url))
#         return None
#
#
# def postRequest_no_json(url=None, data=None, json=None, headers=None):
#     try:
#         response = requests.post(url=url, data=data, json=json, headers=headers)
#         response.encoding = response.apparent_encoding
#         return response.status
#     except Exception as e:
#         print("{}请求失败返回空 e:{}".format(url, e))
#         return None
#
#
# def fileRequest(url=None, data=None, json=None, headers=None, files=None):
#     try:
#         response = requests.post(url=url, data=data, json=json, headers=headers, files=files)
#         response.encoding = response.apparent_encoding
#         return response.json()
#     except Exception as e:
#         print("{}请求失败返回空 e:{}".format(url, e))
#         return None
