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
#print(content)
#print(getVocabSize(content))
dict = buildDict(content)
print(dict)
lambd = 0.95
n = 1000000
"""
print("P(nara) = ",lambd * dict["nara"] + (1-lambd) * (1/n))
print("P(i) = ",lambd * dict["i"] + (1-lambd) * (1/n))
try:
	print("P(kyoto) = ",lambd * dict["kyoto"] + (1-lambd) * (1/n))
except:
	print("P(kyoto) = ",0.05*(1/n))
"""
test_set = readCorpus("test.txt")
#print(test_set[0].split())
"""
prob = 1.0
for i in test_set[0].split():
	prob *= (lambd * dict[i] + (1-lambd) * (1/n))
print(prob)
"""

# likelihood
prob = 1.0
for one in test_set:
	for i in one:
		try:
			prob *= (lambd * dict[i] + (1-lambd)/n)
		except:
			prob *= (1-lambd)/n
print(prob)
# log likelihood

