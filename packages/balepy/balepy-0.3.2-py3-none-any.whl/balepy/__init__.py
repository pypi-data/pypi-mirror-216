from requests import *
from colorama import Fore


print(f"""Wellcom to{Fore.MAGENTA} balepy {Fore.RESET} library version:{Fore.LIGHTBLUE_EX} 0.1 {Fore.RESET}
{Fore.GREEN}Mohammad Mehrabi Rad{Fore.RESET} and {Fore.RED}Erfan Bafandeh{Fore.RESET}{Fore.LIGHTMAGENTA_EX} <github.com/OnlyRad>{Fore.RESET}""")

class Bot:

    def __init__(self , token:str):
        self.token = token
    

    def send_Message(self , chat_id:int , text:str):
        self.chat_id = chat_id
        self.text = text
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
        self.chat_id = chat_id
        site = f"https://tapi.bale.ai/bot{self.token}/getchat?chat_id={self.chat_id}"
        respons = requests.get(url=site)
        print(respons.text)