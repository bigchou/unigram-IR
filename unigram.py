def readCorpus(fname):
	content = []
	with open(fname) as f:
		for line in f:
			content.append(line.rstrip())
	return content

def getVocabSize(corpus):
	count = 0;
	for one in corpus:
		for word in one.split():
			count+=1
	return count

def buildDict(corpus):
	dict = {}
	for one in corpus:
		for word in one.split():
			if word not in dict:
				dict[word] = 1;
			else:
				dict[word] += 1;
	size = getVocabSize(corpus)
	for i in dict:
		dict[i]/=size;
	return dict





content = readCorpus("corpus.txt")
dict = {}
print(content)
print(getVocabSize(content))
dict = buildDict(content)
print(dict)