from io import open
from conllu import parse_incr, parse


#data_file = open("gold.txt", "r", encoding="utf-8")
#data = data_file.read()
#sentences = parse(data)
#for tokenlist in parse_incr(data_file):
 #   print(tokenlist)
#sentence = sentences[0]
#print(len(sentences))
#print(sentence[0])

"""Data has the following form:
[[[dic1,dic2,dict3]/lines ]/sentnece]/sentences
sentences -> sentence -> lines -> ordered dict

"""
def loadFile(path):
	file = open(path, "r", encoding="utf-8")
	data = file.read()
	return parse(data)

def computeMultiple(gold,pred):
	"""Compute Labeled exactMatch, Labeled Attachment Score and Unlabeled Attachment Score"""
	if (len(gold)!=len(pred)):
		print("number of sentence are different")
		return
	error_dict = {}
	sentence_num = len(gold)
	sentence_cor = 0 # used to compute exactMatch
	word_num = 0
	word_cor_label = 0
	word_cor_unlabel = 0
	deprel_set = set()
	for sent_ind in range(len(gold)):
		# First compute labeled version of ExactMathc and Attachment Score
		pred_sent = pred[sent_ind]
		gold_sent = gold[sent_ind]
		sent_flag = len(gold_sent)
		for gr_ind in range(len(gold_sent)):
			word_num += 1
			if gold_sent[gr_ind]['id'] != pred_sent[gr_ind]['id'] or gold_sent[gr_ind]['form'] != pred_sent[gr_ind]['form'] :
				print(gold_sent[gr_ind])
				print(pred_sent[gr_ind])
				print("ID/Form mismatch")
				exit()
			deprel_set.add(gold_sent[gr_ind]['deprel'])
			if  gold_sent[gr_ind]['head'] == pred_sent[gr_ind]['head']:
				word_cor_unlabel += 1
				if gold_sent[gr_ind]['deprel'] == pred_sent[gr_ind]['deprel']:
					word_cor_label += 1
					sent_flag -= 1
			else:
				if sent_ind not in error_dict:
					error_dict[sent_ind] = 0
				error_dict[sent_ind] += 1
				print(gold_sent)
				print(gold_sent[gr_ind])
				print(pred_sent[gr_ind])
				print("=========================")
		if sent_flag == 0:
			sentence_cor += 1
	exactMatch = sentence_cor/ sentence_num
	LAS = word_cor_label/word_num
	UAS = word_cor_unlabel/word_num
	print(word_num,word_cor_label,word_cor_unlabel)
	return exactMatch, LAS, UAS, error_dict, deprel_set
def computeInd(gold,pred,dep_type):
	"""Compute Precision, Recall and F1 for a specific dependency type"""
	if (len(gold)!=len(pred)):
		print("number of sentence are different")
		return

	# for precision
	num_in_output = 0
	correct_in_output = 0
	# for recall
	num_in_gold = 0
	for sent_ind in range(len(gold)):
		pred_sent = pred[sent_ind]
		gold_sent = gold[sent_ind]
		sent_flag = len(gold_sent)
		for gr_ind in range(len(gold_sent)):
			if pred_sent[gr_ind]['deprel']==dep_type:
				num_in_output += 1
			if gold_sent[gr_ind]['deprel']==dep_type:
				num_in_gold += 1
				if gold_sent[gr_ind]['id'] != pred_sent[gr_ind]['id'] or gold_sent[gr_ind]['form'] != pred_sent[gr_ind]['form'] :
					print(gold_sent[gr_ind])
					print(pred_sent[gr_ind])
					print("ID/Form mismatch")
					exit()
				if  gold_sent[gr_ind]['head'] == pred_sent[gr_ind]['head']:
					if gold_sent[gr_ind]['deprel'] == pred_sent[gr_ind]['deprel']:
						correct_in_output += 1
					#print(gold_sent)
					#print(gold_sent[gr_ind])
					#print(pred_sent[gr_ind])
					#print("=========================")
	if num_in_output==0 or correct_in_output==0:
		return 0,0,0
	p = correct_in_output/num_in_output
	r = correct_in_output/num_in_gold
	return p,r,2*p*r/(p+r)
# num of corr/outpu
gold = loadFile("gold.txt")
pred1 = loadFile("Shift-reduce.txt")
pred2 = loadFile("testFile.txt.stp")

a,b,c,d,dep_type = computeMultiple(gold,pred1)

print("==============P, R, F1=============")
print(len(dep_type))
for ele in dep_type:
	print(ele+" :")
	print("SR: ",computeInd(gold,pred1,ele),"PCFG: ",computeInd(gold,pred2,ele))
	print("===================")
#distribution of error graph to show how similar two parsers are
#similarity -> difference

