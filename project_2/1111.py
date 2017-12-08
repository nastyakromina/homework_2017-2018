#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import json

from flask import Flask
from flask import url_for, render_template, request, redirect


app = Flask(__name__)


@app.route('/')
def index():
#    if request.args:
    if not os.path.exists('data.json'):
        json_f = open('data.json', 'w', encoding = "utf-8")
        json_f.close()
    return render_template('index.html')


@app.route('/hi')
def hi():
    if request.args:
        json_f = open('data.json', 'a', encoding = "utf-8")
        sl = {"kl":request.args['kl'], "ob":request.args['ob'], "obl":request.args['obl'], "sex":request.args['sex'], "education": request.args['education'], "age":request.args['age'], "language":request.args['language'], "town_n":request.args['town_n'], "town_l":request.args['town_l']}
        json.dump(sl, json_f)
        json_f.close()
    return '<html><body><p>Спасибо за участие в опросе!</p></body></html>'

@app.route('/stats')
def stats():
    json_f = open('data.json', 'r', encoding = "utf-8")
    lst = json_f.readline()
    json_f.close()
    arr = []
    arr = str(lst).split('}{')
    htm = ''
    klAla, klalA, obnAlis, obnalIs, oblEgchit, oblegchIt, kl_total, ob_total, obl_total = 0, 0, 0, 0, 0, 0, 0, 0, 0
    klAla_m, klalA_m, kl_m_total, obnAlis_m, obnalIs_m, ob_m_total, oblEgchit_m, oblegchIt_m, obl_m_total = 0, 0, 0, 0, 0, 0, 0, 0, 0
    klAla_f, klalA_f, kl_f_total, obnAlis_f, obnalIs_f, ob_f_total, oblEgchit_f, oblegchIt_f, obl_f_total = 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(len(arr)):
        arr[i] = arr[i].strip('}{')
        sl = '{' + arr[i] + '}'
        dic = json.loads(sl)
        for k, v in dic.items():
            if v == 'klAla':
                klAla += 1
            elif v == 'klalA':
                klalA += 1
            elif v == 'obnAlis':
                obnAlis += 1
            elif v == 'obnalIs':
                obnalIs += 1
            elif v == 'oblEgchit':
                oblEgchit += 1
            elif v == 'oblegchIt':
                oblegchIt += 1
        if dic.get('kl', None) == 'klAla' and dic.get('sex', None) == 'male':
            klAla_m += 1
        elif dic.get('kl', None) == 'klalA' and dic.get('sex', None) == 'male':
            klalA_m += 1
        if dic.get('ob', None) == 'obnAlis' and dic.get('sex', None) == 'male':
            obnAlis_m += 1
        elif dic.get('ob', None) == 'obnalIs' and dic.get('sex', None) == 'male':
            obnalIs_m += 1
        if dic.get('obl', None) == 'oblEgchit' and dic.get('sex', None) == 'male':
            oblEgchit_m += 1
        elif dic.get('obl', None) == 'oblegchIt' and dic.get('sex', None) == 'male':
            oblegchIt_m += 1
        if dic.get('kl', None) == 'klAla' and dic.get('sex', None) == 'female':
            klAla_f += 1
        elif dic.get('kl', None) == 'klalA' and dic.get('sex', None) == 'female':
            klalA_f += 1
        if dic.get('ob', None) == 'obnAlis' and dic.get('sex', None) == 'female':
            obnAlis_f += 1
        elif dic.get('ob', None) == 'obnalIs' and dic.get('sex', None) == 'female':
            obnalIs_f += 1
        if dic.get('obl', None) == 'oblEgchit' and dic.get('sex', None) == 'female':
            oblEgchit_f += 1
        elif dic.get('obl', None) == 'oblegchIt' and dic.get('sex', None) == 'female':
            oblegchIt_f += 1
    
    obl_m_total = oblEgchit_m+oblegchIt_m #как ставят ударения мужчины
    oblEgchit_m = oblEgchit_m*100//obl_m_total
    oblegchIt_m = oblegchIt_m*100//obl_m_total
    
    kl_m_total = klAla_m+klalA_m
    klAla_m = klAla_m*100//kl_m_total
    klalA_m = klalA_m*100//kl_m_total
    
    ob_m_total = obnAlis_m+obnalIs_m
    obnAlis_m = obnAlis_m*100//ob_m_total
    obnalIs_m =obnalIs_m*100//ob_m_total

    obl_f_total = oblEgchit_f+oblegchIt_f #как ставят ударения женщины
    oblEgchit_f = oblEgchit_f*100//obl_f_total
    oblegchIt_f = oblegchIt_f*100//obl_f_total
    
    kl_f_total = klAla_f+klalA_f
    klAla_f = klAla_f*100//kl_f_total
    klalA_f = klalA_f*100//kl_f_total
    
    ob_f_total = obnAlis_f+obnalIs_f
    obnAlis_f = obnAlis_f*100//ob_f_total
    obnalIs_f =obnalIs_f*100//ob_f_total
    
    kl_total = klAla + klalA
    klAla = klAla*100//kl_total
    klalA = 100 - klAla
    ob_total = obnAlis+obnalIs
    obnAlis = obnAlis*100//ob_total
    obnalIs = 100 - obnAlis
    obl_total = oblEgchit+oblegchIt
    oblEgchit = oblEgchit*100//obl_total
    oblegchIt = 100 - oblEgchit
                
        
#            htm +='<td>' + v + ' ' + '</td>'
    return render_template('stats.html', klAla=klAla, klalA=klalA, obnAlis=obnAlis,
                           obnalIs=obnalIs, oblegchIt=oblegchIt, oblEgchit=oblEgchit,
                           klAla_m=klAla_m, klalA_m=klalA_m, obnAlis_m=obnAlis_m, obnalIs_m=obnalIs_m,
                           oblEgchit_m=oblEgchit_m, oblegchIt_m=oblegchIt_m, klAla_f=klAla_f, klalA_f=klalA_f,
                           obnAlis_f=obnAlis_f, obnalIs_f=obnalIs_f, oblEgchit_f=oblEgchit_f, oblegchIt_f=oblegchIt_f)

@app.route('/json')
def jsonf():
    json_f = open('data.json', 'r', encoding = "utf-8")
    lst = json_f.readline()
    json_f.close()
    arr = []
    arr = str(lst).split('}{')
    dic = [0]*len(arr)
    for i in range(len(arr)):
        arr[i] = arr[i].strip('}{')
        sl = '{' + arr[i] + '}'
        dic[i] = json.loads(sl)
    return render_template('JS.html', mlst=dic)

@app.route('/search')
def search():
    json_f = open('data.json', 'r', encoding = "utf-8")
    lst = json_f.readline()
    json_f.close()
    arr = []
    arr = str(lst).split('}{')
    for i in range(len(arr)):
        arr[i] = arr[i].strip('}{')
        sl = '{' + arr[i] + '}'
        dic = json.loads(sl)
    return render_template('search.html', mlst=dic)

@app.route('/results')
def results():
    if request.args:
        search_by_sex = request.args['sex']
        json_f = open('data.json', 'r', encoding = "utf-8")
        lst = json_f.readline()
        json_f.close()
        arr = []
        arr = str(lst).split('}{')
        dic = []
        for i in range(len(arr)):
            arr[i] = arr[i].strip('}{')
            sl = '{' + arr[i] + '}'
            item = json.loads(sl)
            if item['sex'] == search_by_sex:
                dic.append(item)
                app.logger.error(item)
    else:
        return redirect(url_for('search'))
    return render_template('JS.html', mlst=dic)

@app.route('/time')
def time_redirect():
#    h = datetime.datetime.today().hour
#    if 10 < h < 18:
#        return redirect(url_for('index'))
    return redirect(url_for('hi'))


if __name__ == '__main__':
    app.run(debug=True)
