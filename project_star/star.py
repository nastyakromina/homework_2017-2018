import urllib.request
import re
import datetime
import os
import json
import requests

from flask import Flask
from flask import url_for, render_template, request, redirect

Dict = {}


app = Flask(__name__)
def get_slovar():
    regwords = re.compile('<td class="uu">([А-Яа-я]*?)</td><td></td><td class="uu">(.*?)</td>', re.DOTALL)
    regfirst = re.compile('(([А-Яа-я]|\'|&#(\d{4});)*?)(,|\s|\b)', re.DOTALL)
    regTag = re.compile('<.*?>', re.DOTALL)
    dictionary = {}
    link = ['c0', 'c1', 'c2','c3','c4','c5','c6', 'c7','c8','c9', 'ca','cb','cc','cd','ce','cf','d0','d1','d2','d3','d4','d5','d6','d7','d8','d9','dd','de','df']
    dorev = 'http://www.dorev.ru/ru-index.html?l='
    for i in range(0, 29): 
        adr = dorev + link[i]
        req = requests.get(adr, headers={'User-Agent': 'Mozilla/5.0 (Chrome/39.0.2171.95'})
        req.encoding = 'windows-1251'
        letter = req.text
        for i in re.findall(regwords, letter):
            dictionary[i[0]] = regTag.sub("", i[1])
            if re.search(regfirst, dictionary[i[0]]):
                dictionary[i[0]] = re.search(regfirst, dictionary[i[0]]).group(1)
    return dictionary

# Программа перевода в старую литерацию
def transliter(word):
    global Dict
    trans = Dict.get(word)
    if trans == None:
        trans = word
    return trans

# Главная страница
@app.route('/')
def index():
    answ = ''
    global  Dict
    if len(Dict) == 0:
        Dict = get_slovar()
    if request.args:
        answ = 'Результат перевода: '
        answ = answ + transliter(request.args['wrd'])
    req = urllib.request.Request('https://www.gismeteo.ru/weather-skopje-3253/')
    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')
       r = re.compile('<span class="js_value tab-weather__value_l">(.*?)<span class="tab-weather__value_m">', flags= re.DOTALL)
       weather = re.search(r, html).group(1)    
    return render_template('index.html', weather=weather, rezult=answ)


@app.route('/lenta')
def lenta():
    wlist = []
    global Dict
    if len(Dict) == 0:
        Dict = get_slovar()
    req = urllib.request.Request('https://lenta.ru/')
    with urllib.request.urlopen(req) as response:
        lenta = response.read().decode('utf-8')
        trans = ''
        r = re.search(r'[а-яА-ЯёЁ]', lenta)
        for i in lenta:
            r = re.search(r'[а-яА-ЯёЁ]', i)
            if r != None:
                trans = trans + i
            else:
                if len(trans) > 0:
                    if trans != None:
                        wlist.append(transliter(trans))
                    trans = ''                    
    return render_template('lenta.html', lenta = wlist)
@app.route('/qst')
def qst():
    lst = ['w1','w2','w3','w4','w5','w6','w7','w8','w9','w10']    
    answ = ''
    tr = 0
    fl = 0
    na = 0
    if request.args:
        answ = 'Результат тестирования: '
        for i in range(0,10):
            try:
                if request.args[lst[i]] == 't':
                    tr += 1
                if request.args[lst[i]] == 'f':
                    fl += 1
            except:
                na += 1
        answ = answ + 'правильных ответов: ' + str(tr) + ',  ошибочных ответов: ' + str(fl) + ',  не отвечно: ' + str(na)

    return render_template('qst.html', rez = answ)
   
if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 80)

