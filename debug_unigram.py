from math import log
from os import listdir
def readData(location):
	contents = []
	filenames = []
	docs = listdir(location)
	docs.remove(".DS_Store")
	for doc in docs:
		filenames.append(doc)
		doc = location+"/"+doc
		content = []
		with open(doc) as f:
			for i,line in enumerate(f):
				#print(line)
				tmp = line.split()
				if "-1" in tmp:
					tmp.remove("-1")
				if location != "SPLIT_DOC_WDID_NEW":
					for word in tmp:
						content.append(word)
				else:
					if(i>2):
						for word in tmp:
							content.append(word)
		contents.append(content)
	return filenames,contents

def getVocabSize(corpus):
	count = 0;
	for one in corpus:
		count+=len(one)
	return count

def buildGlobalDict(corpus,querys):
	dict = {}
	for one in corpus:
		for word in one:
			if word not in dict:
				dict[word] = 1
			else:
				dict[word] += 1

	for one in querys:
		for word in one:
			if word not in dict:
				dict[word] = 1
			else:
				dict[word] += 1

	size = getVocabSize(corpus)
	size += getVocabSize(querys)
	for i in dict:
		dict[i] = float(dict[i]) / float(size);
		#print(i)
	return dict

def ReadExternalGlobalDict(filename):
	dict = {}
	with open(filename) as f:
		for i,line in enumerate(f):
			tmp = line.split()
			dict[tmp[0]] = tmp[1] 	
	return dict


lambd = 0.1
docnames,documents = readData("SPLIT_DOC_WDID_NEW")
qrynames,querys = readData("QUERY_WDID_NEW")
"""
print(docnames[:5])
print(documents[:1])
print(qrynames[:5])
print(querys[:1])
"""

#dict = ReadExternalGlobalDict("Word_Unigram_Xinhua98Upper")
dict = buildGlobalDict(documents,querys)
distinct_querys = []
for qry in querys:
	distinct_querys.append(qry)





with open('ResultsTrainSet.txt', 'w') as f:
	for i,qry in enumerate(distinct_querys):
		output = ""
		print('.')
		output += ("Query " + str(i+1) + " " + qrynames[i] + " "+ str(len(docnames)) + "\n")
		results = {}
		for ind,doc in enumerate(documents):
			prob = 0.0
			total = len(doc)
			for word in qry:
				try:
					prob +=  log(   lambd * (doc.count(word)/float(total))  +   (1-lambd) * dict[word]   )
				except:
					prob +=  0
			results[ind] = prob

		for key, value in sorted(results.items(), key=lambda item: (item[1], item[0]),reverse=True):
			output += (docnames[key] + " " + str(value) + "\n")
		output += "\n"
		f.write(output)



# =========================================================



import sys
import os
import math
import copy
from scipy import spatial
import math
import numpy as np
import pickle

if __name__ == "__main__":
	if sys.argv:
		ans_list = []
		predict_list =[]
		#open ans
		with open('AssessmentTrainSet.txt') as ans_set:
			current_query_ans=[]
			for line in ans_set:	
							
				if line in ['\n', '\r\n']:
					ans_list.append(current_query_ans)
					current_query_ans=[]

				else:
					if line.split()[0] != 'Query':
						current_query_ans.append(line.split()[0])
		#open predict
		with open('ResultsTrainSet.txt') as predict_set:
			current_query_ans=[]
			for line in predict_set:
							
				if line in ['\n', '\r\n']:
					predict_list.append(current_query_ans)
					current_query_ans=[]

				else:
					if line.split()[0] != 'Query':
						current_query_ans.append(line.split()[0])

		result_precision = []
		result_recall =[]
		result_averge =[]

		#cuont precision 
		for query_now in range(len(ans_list)):
			
			current_recall = []
			current_precision = []
			ans_num = len(ans_list[query_now])
			predict_num = len(predict_list[query_now])

			current_match_num = 0
			
			for entity_in_predict in range(len(predict_list[query_now])):
				if predict_list[query_now][entity_in_predict] in ans_list[query_now]:
					current_match_num = current_match_num +1
					current_precision.append((current_match_num)/(entity_in_predict+1.0))
					
					#print 'Precision:'+ str(round((current_match_num*100)/(entity_in_predict+1.0),3)) + '%' +'\t Recall:' +str(round((current_match_num*100)/(ans_num+0.0),3))+ '%'
			sum_now = sum(current_precision)
			average_mean_now = sum_now/ans_num
			print('Curreny query precision:' +str(average_mean_now))
			print('============Query'+str(query_now+1)+'============')
			#result_precision.append(current_precision)
			#result_recall.append(current_recall)
			result_averge.append(average_mean_now)
		print('MAP:'+ str(sum(result_averge)/len(ans_list)))