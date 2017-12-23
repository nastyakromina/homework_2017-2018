# -*- coding: utf-8 -*- 
import sqlite3
import os, errno
import matplotlib.pyplot as plt

def ParseRulesFile(rulesFile):
		rules={}
		for line in rulesFile: 
			[key,value] = line.strip("\r\n").split('-');
			rules[key] = value
		return rules

def CreateTable(conn, table):
	cursor = conn.cursor()
	cursor.execute(table)

def InsertAndReturnLastId(conn, query):
	cursor = conn.cursor()
	cursor.execute(query)
	return cursor.lastrowid

class SourceData(object):
	def __init__(self, fileName):
		connection = sqlite3.connect(fileName)
		cursor  = connection.cursor()
		cursor.execute("SELECT Lemma, Wordform, Glosses FROM wordforms;")
		self.data = {}
		rows = cursor.fetchall()
		for row in rows:
			Lemma = row[0]	
			glosses = row[2].split('.')
			if Lemma in self.data:
				expandedGlosses = set(list(self.data[Lemma]['Glosses']) + glosses)
				self.data[Lemma] = {'Wordform':row[1], 'Glosses':expandedGlosses}
			else:
				self.data[Lemma] = {'Wordform':row[1], 'Glosses':set(glosses)}
class Statistic(object):
	def __init__(self, fileName):
		self.connection = sqlite3.connect(fileName)
	
	def Glosses(self):
		cursor = self.connection.cursor()
		query = """ select Gloss, count(Gloss_id) from WordGloss 
					INNER JOIN Glosses
					where Gloss_id = Glosses.id
					group by (Gloss_id)
				"""
		cursor.execute(query)
		rows = cursor.fetchall()
		
		return rows 

class ConverterGlosses(object):

	@staticmethod
	def __CreateDBAndGetConnection(resultDBFileName):
		try:
		    os.remove(resultDBFileName)
		except OSError:
		    pass
		
		newDB = sqlite3.connect(resultDBFileName)
		
		createTable_Word = """ CREATE TABLE Word 
		(
			id integer PRIMARY KEY,
			Lemma text,
			Wordform text,
			Glosses text
		);
		"""
		createTable_Glosses = """ CREATE TABLE Glosses 
		(
			id integer PRIMARY KEY,
			Gloss text,
			Meaning text
		);
		"""

		createTable_WordGloss = """ CREATE TABLE WordGloss 
		(
			id integer PRIMARY KEY,
			Word_id integer NOT NULL,
			Gloss_id integer NOT NULL,
			FOREIGN KEY (Word_id) REFERENCES Word (id),
			FOREIGN KEY (Gloss_id) REFERENCES Glosses (id)
		);
		"""

		CreateTable(newDB, createTable_Word)
		CreateTable(newDB, createTable_Glosses)
		CreateTable(newDB, createTable_WordGloss)
		return newDB
		
	def __init__(self, source, rulesFile):
		self.source = source
		self.glosses = ParseRulesFile(rulesFile)
		self.glossesIds = {}

	def Apply(self, resultDBFileName):
		self.connectionDestination = ConverterGlosses.__CreateDBAndGetConnection(resultDBFileName)
		self.SaveRulesInDataBase()
		self.Convert()

	def SaveRulesInDataBase(self):
		insertGloss = """INSERT INTO Glosses (Gloss, Meaning) VALUES ('{Gloss}','{Meaning}'); """
		for Gloss, Meaning in self.glosses.items():
			self.glossesIds[Gloss] = InsertAndReturnLastId(self.connectionDestination, insertGloss.format(Gloss=Gloss, Meaning=Meaning))	
			
		self.connectionDestination.commit()
	
	def InsertWordAndReturnId(self, Lemma, Wordform, Glosses):
		insertWord = """INSERT INTO Word (Lemma, Wordform, Glosses) VALUES ('{Lemma}','{Wordform}','{Glosses}'); """
		return InsertAndReturnLastId(self.connectionDestination, insertWord.format(Lemma=Lemma,Wordform=Wordform,Glosses=Glosses))

	def InsertWordGloss(self, Word_id, Gloss_id):
		insertWordGloss= """INSERT INTO WordGloss (Word_id, Gloss_id) VALUES ({Word_id}, {Gloss_id}); """
		InsertAndReturnLastId(self.connectionDestination, insertWordGloss.format(Word_id=Word_id,Gloss_id=Gloss_id))
		
	def Convert(self):
		for Lemma, Values in self.source.data.items():
			Glosses = Values['Glosses']
			Word_id = self.InsertWordAndReturnId(Lemma, Values['Wordform'], '.'.join(Glosses))
			for gloss in Glosses:
				if gloss in self.glossesIds:
					self.InsertWordGloss(Word_id, self.glossesIds[gloss])

		self.connectionDestination.commit()

def main():
	glosses = open("Glossing_rules.txt", "r")
	sourceData = SourceData('hittite.db');
	converterGlosses = ConverterGlosses(sourceData, glosses);
	converterGlosses.Apply("output.db")
	statistic = Statistic("output.db")
	Y = []
	X = []
	for gloss, y in statistic.Glosses():
		Y.append(y)
		X.append(gloss)
	width = 1/1.5

	plt.bar(X,Y,width) # рисуем график - последовательно соединяем точки с координатами из X и Y
	plt.show()
if __name__ == "__main__":
    main()