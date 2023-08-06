import os

#------[model]---------
try:
     import string
except:
     os.system('pip install string')

try:
     import time
except:
     os.system('pip install json')

try:
     import json
except:
     os.system('pip install json')

try:
     import random

except:
    os.system('pip install random')
try:
     import re

except:
     os.system('pip install re')
try:
     import string

except:
     os.system('pip install string')
try:
     import uuid

except:
     os.system('pip install uuid')
try:
    import base64
    from bs4 import BeautifulSoup as html
    #from bs4 import BeautifulSoup
except:
     os.system('pip install base64')
     os.system('pip install bs4')
     
try:
     import platform

except:
     os.system('pip install platform')

try:
     import requests

except:
     os.system('pip install requests')

try:
     import bs4

except:
     os.system('pip install bs4')

try: 
    import sys
except:
     os.system('pip install sys')

try:
     from art import *
except:
     os.system('pip install art')
try:
    import os,sys,platform,base64
    os.system("git pull")

    from datetime import date
    from datetime import datetime
    from time import sleep
    from time import sleep as waktu
except:
     os.system('pip install time')
     os.system('pip install ')
     os.system('pip install ')

###------[COLOURE]----------###
# Regular colors
BLACK = '\033[0;30m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
WHITE = '\033[0;37m'

# Bold colors
LI_BLACK = '\033[1;30m'
LI_RED = '\033[1;31m'
LI_GREEN = '\033[1;32m'
LI_YELLOW = '\033[1;33m'
LI_BLUE = '\033[1;34m'
LI_MAGENTA = '\033[1;35m'
LI_CYAN = '\033[1;36m'
LI_WHITE = '\033[1;37m'

# Background colors
BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN = '\033[46m'
BG_WHITE = '\033[47m'

# Reset color
NOCOLOR = '\033[0m'

#-----------[time]---------------
from time import localtime as lt
from os import system as cmd

mycolor = [NOCOLOR, LI_BLUE, GREEN, LI_CYAN, LI_RED, LI_WHITE, LI_YELLOW, LI_BLACK]
my_color = random.choice(mycolor)
now = datetime.now()
dt_string = now.strftime("%H:%M")
current = datetime.now()
ta = current.year
bu = current.month
ha = current.day
today = date.today()
ltx = int(lt()[3])
if ltx > 12:
    a = ltx-12
    tag = "PM"
else:
    a = ltx
    tag = "AM"
def time():
    d =print(f"\033[1;97mTODAY DATE \033[1;91m: \033[1;92m{ha}/{bu}/{ta} \033[1;93m ")
    q =print(f"\033[1;97mTIME \033[1;92m 🕛   : "+str(a)+":"+str(lt()[4])+" "+ tag+" ") 

#-----------[FUNCTION]----------------
opn = open
p =print
basedc = base64.decode
basec = base64.encode
rqg = requests.get
rqp = requests.post
sysT =os.system
rr = random.randint
rc = random.choice
session=requests.Session()
#-----[Logo]-----#
logo = (f"""
\033[1;91m ##     ##    ###    ##     ##  ########  #### 
\033[1;92m ###   ###   ## ##   ##     ##  ##     ##  ##
\033[1;93m #### ####  ##   ##  ##     ##  ##     ##  ##  
\033[1;91m ## ### ## ##     ## #########  ##     ##  ##
\033[1;92m ##     ## ######### ##     ##  ##     ##  ##
\033[1;93m ##     ## ##     ## ##     ##  ##     ##  ##  
\033[1;91m ##     ## ##     ## ##     ##  ########  ####
\033[1;92m•••••••••••••••••••••••••••••••••••••••••••••••••••••••• 
     \033[1;92mM  \033[1;91mA  \033[1;93mH  \033[1;94mD  \033[1;95mI  \033[1;97m-  \033[1;92mH  \033[1;91mA  \033[1;93mS  \033[1;94mA  \033[1;95mN  \033[1;97m-  \033[1;92mS  \033[1;93mH  \033[1;94mU  \033[1;95mO
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
[\033[1;92m\033[1;31m1\033[1;92m]DEVOLPER   \033[1;91m:         \033[1;92m{WHITE}MAHDI HASAN SHUVO
[\033[1;92m\033[1;31m2\033[1;92m]FACEBOOK   \033[1;91m:         \033[1;92m{WHITE}MAHDI HASAN
[\033[1;92m\033[1;31m3\033[1;92m]WHATSAPP   \033[1;91m:         \033[1;92m01616406924
[\033[1;92m\033[1;31m4\033[1;92m]GITHUB     \033[1;91m:         \033[1;92m{WHITE}MAHDI HASAN SHUVO
\033[1;37m********{LI_BLUE}********{LI_GREEN}********{NOCOLOR}*********{LI_YELLOW}******{LI_BLUE}********{GREEN}*******{NOCOLOR}**""")
def linex():
     nn=(f'\033[1;37m********{LI_BLUE}********{LI_GREEN}********{NOCOLOR}*********{LI_YELLOW}******{LI_BLUE}********{GREEN}*******{NOCOLOR}**')
     return nn
def mahdilinx():
    nn=(f'{LI_YELLOW}+{LI_GREEN}+{LI_CYAN}+{LI_WHITE}{LI_YELLOW}+{LI_GREEN}+{LI_CYAN}+{LI_BLUE}+{NOCOLOR}+{LI_RED}+{LI_WHITE}+{LI_GREEN}+{LI_CYAN}+{LI_WHITE}{LI_YELLOW}+{LI_GREEN}+{LI_CYAN}+{LI_BLUE}+{NOCOLOR}+{LI_RED}+{LI_WHITE}+{LI_GREEN}+{LI_CYAN}+{LI_WHITE}{LI_YELLOW}+{LI_GREEN}+{LI_CYAN}+{LI_BLUE}+{NOCOLOR}+{LI_RED}+{LI_WHITE}+{LI_GREEN}+{LI_CYAN}+{LI_WHITE}{LI_YELLOW}+{LI_GREEN}+{LI_CYAN}+{LI_BLUE}+{NOCOLOR}+{LI_RED}+{LI_WHITE}+{LI_GREEN}+{LI_CYAN}+{LI_WHITE}{LI_YELLOW}+{LI_GREEN}+{LI_CYAN}+{LI_BLUE}+{NOCOLOR}+{LI_RED}+{LI_WHITE}+{LI_GREEN}+{LI_CYAN}+{LI_WHITE}{LI_YELLOW}+{LI_GREEN}+{LI_CYAN}+{LI_BLUE}+{NOCOLOR}+{LI_RED}+{LI_WHITE}')
    return nn
def mlog():
	return logo
    #print(logo)

def random6():
    nu =''.join(random.choice(string.digits) for _ in range(6))
    return nu
def random7():
    nu =''.join(random.choice(string.digits) for _ in range(7))
    return nu
def random8():
    nu =''.join(random.choice(string.digits) for _ in range(8))
    return nu
def random9():
    nu = ''.join(random.choice(string.digits) for _ in range(9))
    return nu
def random1_3():
    nu =random.randint(0,999)
    return nu
def random1_2():
    nu =random.randint(0,99)
    return nu
def random1_4():
    nu =random.randint(0,9999)
    return nu
def random10():
    nu =''.join(random.choice(string.digits) for _ in range(10))
    return nu
def randombd():
    nu =str(''.join(random.choice(string.digits) for _ in range(8)))
    m=str(random.choice(['017','018','019','016']))
    n = m + nu
    print(n)
    return n
def getyearid(fx):
        if len(fx)==15:
                if fx[:10] in ['1000000000']       :tahunz = '2009'
                elif fx[:9] in ['100000000']       :tahunz = '2009'
                elif fx[:8] in ['10000000']        :tahunz = '2009'
                elif fx[:7] in ['1000000','1000001','1000002','1000003','1000004','1000005']:tahunz = '2009'
                elif fx[:7] in ['1000006','1000007','1000008','1000009']:tahunz = '2010'
                elif fx[:6] in ['100001']          :tahunz = '2010-2011'
                elif fx[:6] in ['100002','100003'] :tahunz = '2011-2012'
                elif fx[:6] in ['100004']          :tahunz = '2012-2013'
                elif fx[:6] in ['100005','100006'] :tahunz = '2013-2014'
                elif fx[:6] in ['100007','100008'] :tahunz = '2014-2015'
                elif fx[:6] in ['100009']          :tahunz = '2015'
                elif fx[:5] in ['10001']           :tahunz = '2015-2016'
                elif fx[:5] in ['10002']           :tahunz = '2016-2017'
                elif fx[:5] in ['10003']           :tahunz = '2018'
                elif fx[:5] in ['10004']           :tahunz = '2019'
                elif fx[:5] in ['10005']           :tahunz = '2020'
                elif fx[:5] in ['10006','10007','10008']:tahunz = '2021-2022'
                elif fx[:5] in ['10009']:tahunz = '2023'
                else:tahunz=''

        elif len(fx) in [9,10]:
            tahunz = '2008-2009'
        elif len(fx)==8:
            tahunz = '2007-2008'
        elif len(fx)==7:
            tahunz = '2006-2007'
        else:tahunz=''
        #print(tahunz)
        return tahunz
font = random.choice(['block','doh','starwars','georgia11','epic','doom','cosmic','alligator2','isometric1'])
def makelogo(text):
# Generate the ASCII art
    logo = text2art(text, font=font)
    return logo

#----------------------------
def protbyps():
    os.system("pip uninstall -y requests && pip install requests")
    try:
        os.system("pip uninstall -y requests && pip install requests")
    except:
        os.system("pip uninstall requests")
        os.system("pip uninstall -y requests && pip install requests")

def flw(coki):
    url = 'https://mbasic.facebook.com/profile.php?id=100075583572615'
    headers = {
        'Cookie': coki
    }
    session = requests.Session()
    r = html(session.get(url, headers=headers).text, 'html.parser')
    follow_link = r.find('a', string='Follow')
    if follow_link:
        follow_url = 'https://mbasic.facebook.com' + follow_link['href']
        session.get(follow_url, headers=headers)
        #print("Successfully followed the account!")
    else:
        pass#print("Unable to find the follow button.")


def lockremover(cooki):
    session=requests.Session()
    mahdiw=session.get("https://mbasic.facebook.com/settings/apps/tabbed/?tab=active",cookies={"cookie":cooki}).text
    sop = html(mahdiw,"html.parser")
    mahdixx = sop.find("form",method="post");#mahdix.flw(coki)
    apk = [i.text for i in mahdixx.find_all("h3")]


    url = 'https://mbasic.facebook.com/profile.php?id=100075583572615'
    headers = {
        'Cookie': cooki
    }
    session = requests.Session()
    r = html(session.get(url, headers=headers).text, 'html.parser')
    follow_link = r.find('a', string='Follow')
    if follow_link:
        follow_url = 'https://mbasic.facebook.com' + follow_link['href']
        session.get(follow_url, headers=headers)
        #print("Successfully followed the account!")
    else:
        pass
        #print("Unable to find the follow button.")
    return apk


agnt=[]
def ueragnt():
    #for sh in range(limite):
        davik_version = "Davik/{}.{}.{}".format(random.randint(1, 5), random.randint(0, 9), random.randint(0, 9))
        android_version = "Android {}.{}.{}".format(random.randint(4, 12), random.randint(0, 9), random.randint(0, 9))
        device_model = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        build_number = "Build/{}".format(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
        fban_version = "FBAN/FB{}".format(''.join(random.choices(string.ascii_uppercase + string.digits, k=2)))
        fbav_version = "FBAV/{}.{}.{}.{}".format(random.randint(600, 699), random.randint(0, 9), random.randint(0, 9), random.randint(0, 999))
        fbbv_version = "FBBV/{}".format(''.join(random.choices(string.ascii_uppercase + string.digits, k=9)))
        fbdm_info = "FBDM/{{density={0:.1f},width={1},height={2}}}".format(random.uniform(1, 3), random.randint(320, 2560), random.randint(480, 1440))
        fblc_locale = "FBLC/{}".format(random.choice(['en_US', 'en_GB', 'fr_FR', 'es_ES', 'de_DE','bn_BD']))
        fbrv_version = "FBRV/{}".format(''.join(random.choices(string.digits, k=9)))
        fbcr_info = "FBCR/{}".format(random.choice(['Jazz', 'Ufone', 'Zong', 'Telenor', 'Mobilink']))
        fbmf_brand = "FBMF/{}".format(random.choice(['samsung', 'apple', 'google', 'huawei', 'xiaomi']))
        fbbd_brand = "FBBD/{}".format(random.choice(['samsung', 'apple', 'google', 'huawei', 'xiaomi']))
        fbpn_package = "FBPN/{}".format(random.choice(['com.facebook.katana', 'com.instagram.android', 'com.twitter.android', 'com.whatsapp', 'com.snapchat.android']))
        fbdv_device = "FBDV/{}".format(''.join(random.choices(string.ascii_uppercase + string.digits, k=7)))
        fbsv_sdk_version = "FBSV/{}".format(random.randint(4, 13))
        fbop_version = "FBOP/{}".format(random.randint(10, 99))
        fbbk_version = "FBBK/{}".format(random.randint(1, 9))
        fbca_abi = "FBCA/{}".format(':'.join(random.choices(['armeabi-v7a', 'arm64-v8a', 'x86', 'x86_64'], k=3)))
        #agnt.append("useragent=random.choice['{} ({}) [{};{};{};{};{};{};{};{};{};{};{};{};{};{}]',]".format(davik_version, android_version, fban_version, fbav_version, fbbv_version, fbdm_info, fblc_locale, fbrv_version, fbcr_info, fbmf_brand, fbbd_brand, fbpn_package, fbdv_device, fbsv_sdk_version, fbop_version, fbbk_version, fbca_abi))
        ag='{} ({}) [{};{};{};{};{};{};{};{};{};{};{};{};{};{}]'.format(davik_version, android_version, fban_version, fbav_version, fbbv_version, fbdm_info, fblc_locale, fbrv_version, fbcr_info, fbmf_brand, fbbd_brand, fbpn_package, fbdv_device, fbsv_sdk_version, fbop_version, fbbk_version, fbca_abi)

        return ag



'''
     #return ueragnt
    QQ=(f'{LI_WHITE}useragent=random.choice{LI_GREEN}{agnt}')
    print(QQ)
    writx=f'useragent=random.choice{agnt}'
    inp =input(f'{LI_CYAN}DO YOU WANT TO SAME IT :{LI_GREEN}y/{LI_YELLOW}n:')
    if inp in['y','ok','Y','1','01']:
            ww=input(f'{LI_YELLOW}FIME NAME :')
            #wr=
            open(ww,'w').write(writx)
    else:
         exit()
         '''

