from connenction.HttpRequest import Master_Http
import time
import re

master_url = 'http://ma.jp777.net'
portal_url = 'http://www.jp777.net'
Post_Master_Headers = {'Content-Type': "application/json", 'X-Requested-With': "XMLHttpRequest"}
Get_Mater_Headers = {'X-Requested-With': "XMLHttpRequest"}
portal_code = 'e5466e48e20e4944a0bdaa6bac351c8d'


class Master(object):
    def __init__(self):
        self.http = Master_Http()
        self.cookie = self.http.post(master_url + '/Account/ValidateAccount',
                                     {'account': 'QAautomation', 'password': 'a123456'},
                                     Post_Master_Headers, {})
        self.connectionId = self.http.post(master_url + '/signalr/negotiate', {}, Post_Master_Headers, {})

    def DTPP_success(self):
        while True:
            data = {"count": 25, "query": {"isDTPP": 'true', "search": 'null'}}
            response_data = self.http.post(master_url + '/ThirdPartyPayment/LoadNew', data, Post_Master_Headers,
                                           self.cookie[2])
            for i in range(0, 25):
                print(response_data[1]['Data'][i]['ThirdPartyPaymentId'])
                if response_data[1]['Data'][i]['ThirdPartyPaymentId'] == 96:
                    Id = response_data[1]['Data'][i]['Id']
                    headers = {
                        'Accept': 'application/json,text/plain,*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/json;charset=UTF-8',
                        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                    }
                    self.http.dtpp_get('http://pay.jp777.net/DTPP/Money_96/ServerCallback?Id=' + str(Id) + '&amount=1',
                                       headers)


def DTPP_success():
    Master().DTPP_success()


if __name__ == '__main__':
    DTPP_success()
