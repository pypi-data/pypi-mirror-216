import random
import time

import requests,json
from aishu.public import urlJoin
from aishu.public.operationJson import OperetionJson
from aishu.setting import header


class date(object):
    def getPort(self):
        # 系统合法参数 20010-20099、162，514，5140
        portList = [port for port in range(20010, 20100)]
        portList.append(162)
        portList.append(514)
        portList.append(5140)
        port = random.choice(portList)
        return port

    def getEtlPort(self):
        path = "/etl/input/list?start=0&limit=-1"
        payload = {}
        headers = header
        response = requests.request("GET", urlJoin.url(path), headers=headers, data=payload)
        date = response.json()
        a = OperetionJson(date)
        value = a.get_value('port')
        if value:
            return value
        else:
            return []

    def getEtlPortOld(self):
        data = self.getEtlPort()
        if len(data) == 0:
            port = 0
            return port
        else:
            port = random.choice(data)
            return port

    def getEtlPortNew(self):
        oldNew = self.getEtlPort()
        count = 0
        flag = True
        while flag or count >= 10:
            newPort = self.getPort()
            count = count + 1
            if newPort not in oldNew:
                flag = False
                return newPort
        return ''

    def getEtlPortIll(self):
        portList = [port for port in range(10000, 20000)]
        port = random.choice(portList)
        return port

    def getOpenlogPort(self):
        path = "/etl/input/list?start=0&limit=-1"
        payload = {}
        headers = header
        res = requests.request("GET", urlJoin.url(path), headers=headers, data=payload)
        data = res.json()
        # 从AR中找到对应的端口，若没找到，则生成对应端口，并返回端口号。
        for port_info in data:
            if port_info['type'] == 'testtransfer' and port_info['protocol'] == 'tcp' and port_info['status'] == 1:
                return port_info['port']
        new_port = self.getEtlPortNew()
        create_input_data = {
            "community": [],
            "port": f"{new_port}",
            "protocol": "tcp",
            "ruleName": None,
            "status": 1,
            "tagsID": [],
            "tags": [],
            "timezone": "Asia/Shanghai",
            "type": "testtransfer",
            "charset": "UTF-8"
        }

        path1 = "/etl/input"
        res1 = requests.request("POST", urlJoin.url(path1), headers=headers, data=json.dumps(create_input_data))
        time.sleep(60)
        if res1.status_code != 200:
            return ''
        return new_port
if __name__ == '__main__':
    print(date().getOpenlogPort())