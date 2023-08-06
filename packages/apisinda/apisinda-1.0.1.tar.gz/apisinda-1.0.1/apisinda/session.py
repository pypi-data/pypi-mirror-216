import requests

url = "https://apisinda.dev.coene.inpe.br/usuarios/"

class Session:    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.refresh = None

    def get_token(self):
        try:
            if self.token == None:
                self.login()
            else:
                if self.token_invalid():
                    if not self.refresh_token():
                        self.login()
            return self.token
        except:
            return("Connection error")
    
    def login(self):
        session = requests.post(url + 'logout/')
        credentials = {'username': self.username, 'password': self.password}
        session = requests.post(url + 'login/', json=credentials)
        if session.status_code == 200:
            self.token = session.json()['access']
            self.refresh = session.json()['refresh']
        else:
            print(session.text)

    def token_invalid(self):
        token = {'token': self.token}
        req = requests.post(url + 'token/verify/', json=token)
        return False if req.status_code == 200 else True

    def refresh_token(self):
        refresh = {'refresh': self.refresh}
        req = requests.post(url + 'token/refresh/', json=refresh)
        if req.status_code == 401:
            return False
        else:
            self.token = req.json()['access']
            return True