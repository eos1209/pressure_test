"""
故事5:
1. 新增會員 - 更新會員銀行資料
2. 批次會員 - 修改標籤
"""
from connenction.HttpRequest import Master_Http

master_url = 'http://ma.jp777.net'
Post_Master_Headers = {'Content-Type': "application/json", 'X-Requested-With': "XMLHttpRequest"}
Get_Mater_Headers = {'X-Requested-With': "XMLHttpRequest"}
upload_Mater_Headers = {'X-Requested-With': "XMLHttpRequest"}


class story5:
    def __init__(self):
        self.http = Master_Http()
        self.cookie = self.http.post(master_url + '/Account/ValidateAccount',
                                     {'account': 'QA3', 'password': 'a123456'},
                                     Post_Master_Headers, {})
        self.connectionId = self.http.post(master_url + '/signalr/negotiate', {}, Post_Master_Headers, {})

    def batch_member(self):
        data = {"search": {"MemberLevelSettingIds": ["5"]}, "isSuper": 'false', "batchParam": {"isAll": 'true'},
                "newTags": ['QA'],
                "addTagIds": [31], "deleteTagIds": [32]}
        self.http.post(master_url + '/MemberTag/BatchAddOrDeleteMemberTags', data, Post_Master_Headers, self.cookie[2])


def main():
    story5().batch_member()


if __name__ == '__main__':
    main()
