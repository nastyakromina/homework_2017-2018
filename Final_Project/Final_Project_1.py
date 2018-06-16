import re
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()
from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/names')
def names():
    if request.args:
        file = open("text.txt", "w", encoding = "utf-8")
        text = request.args['phrase']
        file.write(str(text))
        file.close()
        upper_words = []
        names = []
        reg = re.compile('[^а-яА-ЯёЁ ]')
        text_1 = reg.sub('', text)
        text_new = text_1.split()
        for i in text_new:
            if i[0].isupper():
                upper_words.append(i)
        for i in upper_words:
            ana = morph.parse(i)
            if 'Name' in ana[0].tag or 'Surn' in ana[0].tag or 'Patr' in ana[0].tag:
                names.append(i)
        f_1 = open("names.txt", "w", encoding = "utf-8")
        f_1.write(str(names))
        f_1.close()
        change_name = []
        for i in names:
            ana_1 = morph.parse(i)
            words = ana_1[0].normalized
            will_check = words.word
            will_check_upper = will_check.title()
            if any(will_check_upper in s for s in change_name):
                continue
            else:
                change_name.append(will_check_upper)
        f = open("change_name.txt", "w", encoding = "utf-8")
        f.write(str(change_name))
        f.close()
    return render_template('names.html', rezult = change_name)
    
@app.route('/final_text')
def final_text():
    file_1 = open("change_name.txt", "r", encoding = "utf-8")
    change_name_1 = file_1.read()
    file_1.close()
    file_2 = open("text.txt", "r", encoding = "utf-8")
    text = file_2.read()
    file_2.close()
    file_3 = open("names.txt", "r", encoding = "utf-8")
    names_1 = file_3.read()
    file_3.close()
    regg = re.compile('[^а-яА-ЯёЁ ]')
    text_1 = regg.sub('', change_name_1)
    change_name = text_1.split()
    text_2 = regg.sub('', names_1)
    names = text_2.split()
    dict_chan_name = {}
    for i in change_name:
        dict_chan_name[i.lower()] = request.args[i]
    final_slovar = {}
    for i in names:
        ana_2 = morph.parse(i)
        for key in dict_chan_name:
            ana_3 = morph.parse(dict_chan_name[key])[0]
            ana_4 = ana_3.lexeme
            for i in ana_4:
                if key == ana_2[0].normal_form and ana_2[0].tag.number == i.tag.number and ana_2[0].tag.case == i.tag.case and ana_2[0].tag.POS == i.tag.POS:
                    final_slovar[ana_2[0].word] = i.word.title()
                    break
    reg_2 = re.sub(r"(\W*)(" + "|".join(final_slovar.keys()) + r")(\W*)", lambda m: "".join([m.group(1), final_slovar[m.group(2).lower()], m.group(3)]), text, flags=re.I)
    return render_template('final_text.html', rezult = reg_2)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 80)

