"""
故事4:
1. 全站-寄站內信
2. 紅包沖銷
"""
from connenction.HttpRequest import Master_Http
import os

master_url = 'http://ma.jp777.net'
Post_Master_Headers = {'Content-Type': "application/json", 'X-Requested-With': "XMLHttpRequest"}
Get_Mater_Headers = {'X-Requested-With': "XMLHttpRequest"}
upload_Mater_Headers = {'X-Requested-With': "XMLHttpRequest"}


class UploadFile(object):
    # 上傳檔案
    def __init__(self, path, upload_name, filename):
        file_path = 'D:/story/' + path  # 檔案路徑
        self.path = os.path.abspath(file_path)
        self.upload_name = upload_name  # 上傳欄位
        self.filename = filename  # 上傳檔名
        self.open_file = open(self.path, 'rb')  # 開啟檔案
        self.file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 上傳類型

    def Upload_file(self):  # 上傳檔案-方法
        data = {self.upload_name: (self.filename, self.open_file, self.file_type, {'Expires': '0'})}
        return data

    def Close_file(self):  # 檔案關閉-方法
        self.open_file.close()


class story4:
    def __init__(self):
        self.http = Master_Http()
        self.cookie = self.http.post(master_url + '/Account/ValidateAccount',
                                     {'account': 'hugo', 'password': 'a123456'},
                                     Post_Master_Headers, {})
        self.connectionId = self.http.post(master_url + '/signalr/negotiate', {}, Post_Master_Headers, {})

    def siteMail(self):
        data = {"SendMailType": 4,
                "MailRecievers": " ",
                "BatchParam": " ",
                "SearchParam": " ",
                "SuperSearchRequest": " ",
                "ResendMailID": " ",
                "Subject": "測試站內信(發送對象--全站)",
                "MailBody": "<p>"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "</p>\n", "ExcelFilePath": " "}
        self.http.post(master_url + '/SiteMail/SendMail', data, Post_Master_Headers, self.cookie[2])

    def revoke_redEnvelope(self):
        data = {"take": 100, "skip": 0, "search": {}, 'connectionId': self.connectionId[1]}
        response_data = self.http.post(master_url + '/RedEnvelopeManagement/GetList', data, Post_Master_Headers,
                                       self.cookie[2])
        Id = response_data[1]['ReturnObject'][1]['Id']
        data = {"Id": Id, "RevokePortalMemo": "@QA_automation-RevokeRedEnvelope", "Password": 'a123456'}
        self.http.post(master_url + '/RedEnvelopeManagement/Revoke', data, Post_Master_Headers, self.cookie[2])


def main():
    story4().siteMail()
    story4().revoke_redEnvelope()


if __name__ == '__main__':
    main()
