#coding: utf8
from datetime import datetime
import requests
import json
import time
nid = 317279
url = 'http://dn.sdo.com/web11/handler/GetNewsContent.ashx'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'sdo_cas_id=10.129.20.231; Hm_lvt_9b769a7a77ea494e116160167dee8955=1578036821,1578976149; userinfo=userid=1087490669-1826515211-1586231636&siteid=SDG-08117-01; ASPSESSIONIDASACDCSA=PLMJFCCBKJIDKLBMMDJPPABC; NSC_HX-EO=ffffffff09884e8a45525d5f4f58455e445a4a423660; CAS_LOGIN_STATE=1; sdo_dw_track=ovspgKXV3mP/MhO7pokz4Q==; LAT=l=93&l_err=6.13; __wftflow=250207694=1&504045206=3&1460288114=2&1855222422=3; RT=cl=1588756993033&r=http%3A%2F%2Fdn.sdo.com%2Fweb11%2Fnews%2FnewsContent.html%3FID%3D316761%26CategoryID%3D103&nu=http%3A%2F%2Fdn.sdo.com%2Fweb11%2Fnews%2FnewsContent.html%3FID%3D316728%26CategoryID%3D103&ul=1588757511700&hd=1588757511849',
    'Host': 'dn.sdo.com',
    'Origin': 'http://dn.sdo.com',
    'Referer': 'http://dn.sdo.com/web11/news/newsContent.html?ID=316761&CategoryID=103',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
r = requests.post(url, data=dict(ID=nid), headers=headers)
rsp = json.loads(r.json()['ReturnObject'])
import pdb; pdb.set_trace()
