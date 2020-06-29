import requests
import abc


class HttpRequest_interface(metaclass = abc.ABCMeta):  # 建立http介面
    @abc.abstractmethod
    def get(self, *args):
        pass

    @abc.abstractmethod
    def post(self, *args):
        pass


class Master_Http(HttpRequest_interface):  # Master的http方法繼承(inherit) http介面
    def get(self, *args):
        r = requests.get(args[0], params = args[1], headers = args[2], cookies = args[3])
        status_code = r.status_code  # 獲取返回狀態碼
        response_text = r.text
        return str(status_code), response_text, r.cookies  # 返回響應碼，内容

    def post(self, *args):
        r = requests.post(args[0], json = args[1], headers = args[2], cookies = args[3])
        status_code = r.status_code  # 獲取返回狀態碼
        if r.content:
            response_json = r.json()  # 響應内容，json類型轉化成python數據類型
        else:
            response_json = r.content
        return str(status_code), response_json, r.cookies  # 返回響應碼，内容

    @staticmethod
    def uploadFile(*args):
        r = requests.post(args[0], files = args[1], headers = args[2], cookies = args[3])
        status_code = r.status_code  # 獲取返回狀態碼
        if r.content:
            response_json = r.json()  # 響應内容，json類型轉化成python數據類型
        else:
            response_json = r.content
            print(status_code, response_json)
        return str(status_code), response_json, r.cookies  # 返回響應碼，内容

    def dtpp_get(self, *args):
        try:
            requests.get(args[0], headers = args[1])
        except requests.exceptions.RequestException:
            pass

# class Portal_Http(HttpRequest_interface):  # Portal的http方法繼承(inherit) http介面
#     response_data = {}  # 設定post 接收的屬性
#
#     def get(self, *args):  # get 必須得要加上處理header的部分，以方便post去引用該參數
#         r = requests.get(args[0], params = {}, headers = {}, cookies = args[1])
#         status_code = r.status_code  # 獲取返回狀態碼
#         response_text = r.text
#         get_headers_info = [str(status_code), response_text, r.cookies]  # 返回響應碼，内容 # 設定為一個list ，後續處理
#         getToken = re.search('(_RequestVerificationToken" type="hidden" value=")(.*?)(" />)', get_headers_info[1])
#         token = getToken.group(2)
#         cookies = self.add_cookie(args[1], get_headers_info[2])
#         Portal_Headers_request = {
#             'Accept': 'application/json,text/plain,*/*',
#             'Accept-Encoding': 'gzip, deflate',
#             'Connection': 'keep-alive',
#             'c8763': token,
#             'Content-Type': 'application/json;charset=UTF-8',
#             'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
#             'X-Requested-With': "XMLHttpRequest",
#         }
#         return Portal_Headers_request, cookies
#
#     def post(self, *args):
#         self.response_data = self.get(args[0], args[3])
#         r = requests.post(args[1], json = args[2], headers = self.response_data[0], cookies = self.response_data[1])
#         status_code = r.status_code  # 獲取返回狀態碼
#         if r.content:
#             response_json = r.json()  # 響應内容，json類型轉化成python數據類型
#         else:
#             response_json = r.content
#         return str(status_code), response_json, r.cookies  # 返回響應碼，内容
#
#     @staticmethod  # 設定為靜態方法
#     def cookie_process(cookie_jar):  # 處理登入後的cookie
#         cookie = requests.utils.dict_from_cookiejar(cookie_jar)
#         return cookie
#
#     @staticmethod  # 設定為靜態方法
#     def add_cookie(login_cookie, get_cookie):  # 上一頁假的RequestVerificationToken必須加在新的cookie一起回傳
#         set_RequestVerificationToken_value = get_cookie['__RequestVerificationToken']
#         set_request = requests.cookies.RequestsCookieJar()
#         set_request.set('__RequestVerificationToken', set_RequestVerificationToken_value)
#         login_cookie.update(set_request)
#         return login_cookie
