import requests
import xml.etree.ElementTree as ET

def instrument(username, password):
    url = "http://service.tsetmc.com/WebService/TsePublicV2.asmx"
    querystring = {"WSDL":""}
    payload = \
        """<?xml version="1.0" encoding="utf-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
        <soap12:Body>
        <Instrument xmlns="http://tsetmc.com/">
            <UserName>""" + username + """</UserName>
            <Password>""" + password + """</Password>   
            <Flow>0</Flow>
        </Instrument> 
    </soap12:Body>
    </soap12:Envelope>"""
    headers = {
    'content-type': "application/soap+xml",
    'charset': "utf-8",
    'cache-control': "no-cache"
    }
    try:
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        root = ET.fromstring(response.text)
        instruments = []
        for child in root[0][0][0][1][0]:
            data = dict()
            for ch in child:
                data[ch.tag]= ch.text
            instruments.append(data)
        if instruments != None:
            with open('instruments.txt', 'w') as f:
                f.write(str(instruments))
            return instruments
        else:
            instrument(username, password)
    except Exception as err:
        print("error message: " + str(err))
        print("Attempt again ...")
        instrument(username, password)

def inst_trade(username, password, ins_code, date_from, date_to):
    url = "http://service.tsetmc.com/WebService/TsePublicV2.asmx"
    querystring = {"WSDL":""}
    payload = \
    '''<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
        <soap12:Body>
            <InstTrade xmlns="http://tsetmc.com/">
                <UserName>''' + username + '''</UserName>
                <Password>''' + password + '''</Password>
                <Inscode>''' + str(ins_code) + '''</Inscode>
                <DateFrom>''' + str(date_from) + '''</DateFrom>
                <DateTo>''' + str(date_to) + '''</DateTo>
            </InstTrade>
        </soap12:Body>
    </soap12:Envelope>'''
    headers = {
        'content-type': "application/soap+xml",
        'charset': "utf-8",
        'cache-control': "no-cache"
    }
    try:
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        trade_tree = ET.fromstring(response.text)
        data = []
        for child in trade_tree[0][0][0][1][0]:
            a = []
            for ch in child:
                a.append((ch.tag, ch.text))
            data.append(a)
        return data
    except Exception as err:
        print(str(err))
    