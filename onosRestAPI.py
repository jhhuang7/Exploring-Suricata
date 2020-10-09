import urllib
import requests
import json 
import os

pay_load_to_post = {
  "flows": [
    {
  "priority": 41000,
  "timeout": 0,
  "isPermanent": True,
  "deviceId": "of:0000000000000001",
  "treatment": {

    }, "selector": {
        "criteria": [
        {
            "type": "IPV4_SRC",
            "ip": "10.0.0.1/32"
        },
        {
            "type": "ETH_TYPE",
            "ethType": "0x0800"
        },
        ]
        }
    },
        {
  "priority": 41000,
  "timeout": 0,
  "isPermanent": True,
  "deviceId": "of:0000000000000001",
  "treatment": {

  }, "selector": {
    "criteria": [
      {
        "type": "IPV4_SRC",
        "ip": "10.0.0.2/32"
      },
       {
        "type": "ETH_TYPE",
        "ethType": "0x0800"
      },
      {
        "type": "IN_PORT",
        "port": "1"
      },
    ]
    }
}
  ]
}

postTo = requests.post("http://127.0.0.1:8181/onos/v1/flows/", data = json.dumps(pay_load_to_post) , auth=('onos','rocks'))
print(postTo.content)

# a = requests.delete("http://127.0.0.1:8181/onos/v1/flows/of:0000000000000001/1")
# print(a)
# x = requests.get("http://127.0.0.1:8181/onos/v1/flows/of:0000000000000001/", auth=('onos','rocks'))
# print(x.content)

# print('---------------')
# x = requests.get("http://127.0.0.1:8181/onos/v1/hosts", auth=('onos','rocks'))
# print(x.content)


# '{"hosts":[{"id":"E2:74:D0:58:74:AD/None","mac":"E2:74:D0:58:74:AD","vlan":"None","configured":false,
# "ipAddresses":["10.0.0.1"],"location":{"elementId":"of:0000000000000001","port":"1"}},


# {"id":"CA:D0:89:F7:44:77/None","mac":"CA:D0:89:F7:44:77","vlan":"None","configured":false,"ipAddresses":["10.0.0.5"],
# "location":{"elementId":"of:0000000000000003","port":"3"}}]}'


# b'{"links":
# [



# {"src":{"port":"4","device":"of:0000000000000001"},
# "dst":{"port":"1","device":"of:0000000000000002"},"type":"DIRECT","state":"ACTIVE"},

# {"src":{"port":"2","device":"of:0000000000000002"},
# "dst":{"port":"1","device":"of:0000000000000003"},"type":"DIRECT","state":"ACTIVE"},

# {"src":{"port":"3","device":"of:0000000000000002"},
# "dst":{"port":"1","device":"of:0000000000000004"},"type":"DIRECT","state":"ACTIVE"},

# {"src":{"port":"1","device":"of:0000000000000002"},
# "dst":{"port":"4","device":"of:0000000000000001"},"type":"DIRECT","state":"ACTIVE"},


# {"src":{"port":"1","device":"of:0000000000000003"},
# "dst":{"port":"2","device":"of:0000000000000002"},"type":"DIRECT","state":"ACTIVE"}]}'

# {"src":{"port":"1","device":"of:0000000000000004"},
# "dst":{"port":"3","device":"of:0000000000000002"},"type":"DIRECT","state":"ACTIVE"},
