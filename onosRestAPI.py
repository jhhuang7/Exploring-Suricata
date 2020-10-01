import urllib
import requests

payload = {'user': 'onos:rocks'}

x = requests.get("http://127.0.0.1:8181/onos/v1/links", auth=('onos','rocks'))
print(x.content)