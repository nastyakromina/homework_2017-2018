# -*- coding: utf-8 -*- 

import urllib.request
import re
import json
import math
import datetime
import matplotlib.pyplot as plt

def access_token(): #получаем доступ к токену
	token = '90cad1f790cad1f790cad1f7ae90a8571f990ca90cad1f7ca14c24ea704cc2fde59d81d'
	return '&access_token=' + token

def GetCity(response):
	try:
		return response[0]['city']['title'];
	except Exception as e:
		return '';

def GetAge(response):
	try:
		birthday = datetime.datetime.strptime(response[0]['bdate'], '%d.%m.%Y').year
		today = datetime.date.today().year
		return today - birthday
	except Exception as e:
		return -1

def RequestUser(from_id):
	req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids='+ str(abs(from_id)) + '&fields=bdate,city' + access_token() +'&v=5.74')
	response = urllib.request.urlopen(req)
	result = response.read().decode('utf-8')
	data = json.loads(result)
	#print(from_id, data)
	return { 
		'year' : GetAge(data['response']),
		'city' : GetCity(data['response'])
	}

def RequestComments(owner_id, post_id, count):
	shift = 100
	comments = {}
	for currentOffset in range(0, math.ceil(count / shift)):
		req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id='+ str(owner_id) + '&post_id=' + str(post_id) + access_token() +'&v=5.74&count=100&filter=owner&offset=' + str(shift*currentOffset))
		response = urllib.request.urlopen(req)
		result = response.read().decode('utf-8')
		data = json.loads(result)
		for item in data['response']['items']:
			comments[item['from_id']] = { 	
				'text' : item['text'],
				'words_count' : len(item['text'].split()),
				'user' : RequestUser(item['from_id'])
			}
	return comments
	
#https://vk.com/hsecouncil
def RequestPostWithComment(group, countPost):
	#myFile = open('json','w', encoding='utf-8')
        X = []
        Y = []
        Age = []
        Lpost = []
        Lcomm = []
        shift = 100
        postsWithComments = {}
        temp = {}
        for i in range(100):
                Age.append(0)
                Lpost.append(0)
                Lcomm.append(0)
        for currentOffset in range(0, math.ceil(countPost / shift)):
                req = urllib.request.Request('https://api.vk.com/method/wall.get?domain='+ group + access_token() +'&v=5.74&count=100&filter=owner&offset=' + str(shift*currentOffset))
                response = urllib.request.urlopen(req)
                result = response.read().decode('utf-8')
                data = json.loads(result) 
                counter = 0
                for item in data['response']['items']:
                        comments = RequestComments(item['owner_id'], item['id'], item['comments']['count'])
			
                        mean_comments = 0
                        for comment in comments.values():
                                mean_comments = mean_comments + comment['words_count']
                        if len(comments) > 0:
                                mean_comments = mean_comments / len(comments)
                        postsWithComments[item['id']] = { 
                                'from_id' : RequestUser(item['from_id']),
                                'text' : item['text'],
                                'words_count' : len(item['text'].split()),
                                'comments' : comments,
                                'mean_comments' : mean_comments
                        }
                        temp = RequestUser(item['from_id'])
                        age = temp.get('year')
                        if age > 0:
                                Age[age] += 1
                                Lpost[age] += len(item['text'].split())
                                Lcomm[age] += mean_comments
                        counter += 1
                        X.append(len(item['text'].split()))
                        Y.append(mean_comments)
                pass
        for i in range(100):
                if Age[i] != 0:
                        Lpost[age] = Lpost[age]/Age[i]
                        Lcomm[age] = Lcomm[age]/Age[i]
        plt.title("Соотношение длины поста со средней длиной комментария")
        plt.xlabel("Длина поста")
        plt.ylabel("Средняя длина комментария")
        plt.bar(X, Y)
        plt.show()
        plt.title("Длина поста от возраста")
        plt.xlabel("Возраст")
        plt.ylabel("Длина поста")
        plt.bar(Age, Lpost)
        plt.show()
        
        return postsWithComments

                

posts = RequestPostWithComment('evanescence', 100);
datFile = open('dataFil.txt','w', encoding='utf-8')
datFile.write(str(posts))
datFile.close()

