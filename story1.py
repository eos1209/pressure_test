"""
故事1:前置作業
1. 全站-寄站內信
2. 優惠匯入
3.10萬紅包匯入
"""
from connenction.HttpRequest import Master_Http
import os
from datetime import datetime, timedelta

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


class story1:
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

    def red_Envelope(self):
        self.upload = UploadFile('file/red.xlsx',  # 檔案路徑
                                 'fileBase',  # 上傳欄位
                                 'red.xlsx'  # 上傳檔名
                                 )  # 先實例上傳檔案物件
        startTime = (datetime.now() + timedelta(hours = -11.98)).strftime("%Y/%m/%d %H:%M:%S")  # 開始時間-美東時間
        endTime = (datetime.now() + timedelta(hours = +11)).strftime("%Y/%m/%d %H:%M:%S")  # 結束時間 - 後天
        data = {'Name': (None, 'QA_automation_redEnvelope'),
                'Password': (None, 'a123456'),
                'StartTime': (None, startTime),  # 有其他參數上傳用這種mode
                'EndTime': (None, endTime), 'Description': (None, 'QA_automation'),
                self.upload.upload_name: (
                    self.upload.filename, self.upload.open_file, self.upload.file_type, {'Expires': '0'})}
        self.http.uploadFile(master_url + '/RedEnvelopeManagement/AddRedEnvelope', data,
                             upload_Mater_Headers,
                             self.cookie[2])


def main():
    story1().siteMail()
    story1().red_Envelope()


if __name__ == '__main__':
    main()
