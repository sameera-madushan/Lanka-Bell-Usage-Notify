import os
import json
import time
import base64
import requests
import win32gui, win32con
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

credentials = {
    'username' : '',
    'password' : ''
}

while True:
    try:
        if os.path.exists('creds.json'):
            with open('creds.json', 'r') as f:
                data = json.load(f)

                username = data['username']
                password = data['password']

                dec_username = base64.b64decode(username.encode())
                dec_password = base64.b64decode(password.encode())

                url = 'https://www.lankabell.com/lte/home1.jsp'
                data = {'logName': dec_username, 'redirectFUP': 'null','password': dec_password, 'logtype': 'login', 'submit': 'Sign In'}

                session = requests.session()
                response = session.post(url,data=data).content.decode('utf-8')
                x = session.cookies.get_dict()
                soup = BeautifulSoup(response, 'lxml')
                error = soup.find('div', {'id':'result'})

                if not error:
                    try:
                        frgrnd_wndw = win32gui.GetForegroundWindow();
                        wndw_title  = win32gui.GetWindowText(frgrnd_wndw);
                        if wndw_title.endswith("lankabell_usage_notify.exe"):
                            win32gui.ShowWindow(frgrnd_wndw, win32con.SW_HIDE);
                    except Exception:
                        pass

                    toaster = ToastNotifier()
                    span = soup.find_all('span', {'class':'styleCommon'})

                    days = span[10].text

                    url2 = 'https://www.lankabell.com/lte/usage.jsp'

                    t = requests.post(url2, cookies=x).content.decode('utf-8')

                    soup = BeautifulSoup(t, 'lxml')

                    spans = soup.find_all('span', {'class' : 'styleCommon'})

                    monthly_anytime = spans[0].text
                    monthly_offpeak = spans[1].text

                    m_combine = monthly_anytime + "\n" + monthly_offpeak

                    remaining_anytime = spans[2].text
                    remaining_offpeak = spans[3].text

                    r_combine = remaining_anytime + "\n" + remaining_offpeak + "\n" + "Data Validity Period: " + days

                    toaster.show_toast("Monthly Usage",
                                    m_combine,
                                    icon_path="fav.ico",
                                    duration=6,
                                    )

                    toaster.show_toast("Remaining Data",
                                    r_combine,
                                    icon_path="fav.ico",
                                    duration=6,
                                    )

                    time.sleep(60)

                else:
                    username = str(input("Username: "))
                    password = str(input("Password: "))
                    
                    enc_username = base64.b64encode(username.encode())
                    enc_passwprd = base64.b64encode(password.encode())

                    credentials['username'] = enc_username.decode()
                    credentials['password'] = enc_passwprd.decode()

                    with open('creds.json', 'w') as f:
                       json.dump(credentials, f)
        else:
            username = str(input("Username: "))
            password = str(input("Password: "))

            enc_username = base64.b64encode(username.encode())
            enc_passwprd = base64.b64encode(password.encode())

            credentials['username'] = enc_username.decode()
            credentials['password'] = enc_passwprd.decode()

            with open('creds.json', 'w') as f:
                json.dump(credentials, f)

    except Exception:
        quit()
