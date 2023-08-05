import requests

class Bot:

    def __init__(self , token:str):
        self.token = token
    

    def send_Message(self , chat_id:int , text:str):
        self.chat_id = chat_id
        self.text == text
        requests.post(url=f"https://tapi.bale.ai/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={self.text}")
    
    def getupdate(self):
        site = f"https://tapi.bale.ai/bot{self.token}/getupdates"
        a = requests.get(url=site)
        a = a.json()
        a = a['result']
        print(a)

    def getlastupdate(self):
        while True:
            site = f"https://tapi.bale.ai/bot{self.token}/getupdates"
            a = requests.get(url=site)
            a = a.json()
            a = a['result']
            ac = len(a)
            ac = ac - 1
            a = a[ac]
            return a
    def getme(self):
        site = f"https://tapi.bale.ai/bot{self.token}/getme"
        respons = requests.get(url=site)
        print(respons.text)
    def getchat(self , chat_id):
        site = f"https://tapi.bale.ai/bot{self.token}/getchat?chat_id={self.chat_id}"
        respons = requests.get(url=site)
        print(respons.text)

Bot("310410542:l6pRTSCYn9TRZYf8DgYzd3qWUyRNhzDMXGXBEKvP").getlastupdate()