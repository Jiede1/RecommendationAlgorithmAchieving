#coding:utf-8
"""
author: Jiede1
date: 2019
"""

import os
def get_item_info(input_file):
	filepath = os.path.dirname(os.path.abspath(__file__))
	input_file = filepath+'/'+input_file
	if not os.path.exists(input_file):
		print('path is not exist')
		return {}
	lineNum = 0
	item_info = {}
	fp = open(input_file,encoding='utf-8')
	for line in fp:
		if lineNum == 0:
			lineNum+=1
			continue
		item = line.strip().split(',')
		if len(item) < 3:
			continue
		elif len(item)>3:
			itemid = item[0]
			genre = item[-1]
			title = ','.join(item[1:-1])
		else:
			itemid,title,genre = item[0],item[1],item[2]
		item_info[itemid] = [title,genre]
	
	fp.close()
	return item_info
	
def get_ave_score(input_file):
	"""
	get item ave rating score
	Args:
		input_file: user rating file
	Return:
		a dict,key:itemid,value:ave_score
	"""
	if not os.path.exists(input_file):
		print('file not exist')
		return {}
	lineNum = 0
	record_dict = {}
	score_dict = {}
	fp = open(input_file)
	for line in fp:
		if lineNum == 0:
			lineNum+=1
			continue
		item = line.strip().split(',')
		if len(item) < 4:
			continue
		userid,itemid,rating = item[0],item[1],float(item[2])
		if itemid not in record_dict:
			record_dict[itemid] = [0,0]
		record_dict[itemid][0]+=1
		record_dict[itemid][1]+=rating
	fp.close()
	for itemid in record_dict:
		score_dict[itemid]=round(record_dict[itemid][1]/record_dict[itemid][0],3)
	return score_dict

def get_train_data(input_file,score_thr = 4):
	"""
	Args:
		input_file
	Return:
		a list[(userid,itemid,label)]
	"""
	filepath = os.path.dirname(os.path.abspath(__file__))
	input_file = filepath+'/'+input_file
	if not os.path.exists(input_file):
		return []
	score_dict = get_ave_score(input_file)
	lineNum = 0
	train_data = []
	neg_dict = {}
	pos_dict ={}
	fp = open(input_file)
	for line in fp:
		if lineNum == 0:
			lineNum += 1
			continue
		item = line.strip().split(',')
		if len(item) > 4:
			continue
		elif len(item) == 4:
			userid,itemid,rating = item[0],item[1],float(item[2])
			if userid not in pos_dict:
				pos_dict[userid] = []
			if userid not in neg_dict:
				neg_dict[userid] = []
			if rating >= score_thr:
				pos_dict[userid].append((itemid,1))
			else:
				score = score_dict.get(itemid,0)
				neg_dict[userid].append((itemid,score))
	fp.close()
	for userid in pos_dict.keys():
		data_num = min(len(pos_dict[userid]),len(neg_dict.get(userid,[])))
		if data_num > 0:
			train_data += [(userid,value[0],value[1]) for value in pos_dict[userid]][:data_num]
		else:
			continue
		sorted_neg_dict = sorted(neg_dict[userid],key=lambda element:element[1],reverse=True)[:data_num]
		train_data += [(userid,value[1],0)for value in sorted_neg_dict]
		
		if userid == '24':
			print(len(pos_dict[userid]))
			print(len(neg_dict[userid]))
			print(len(sorted_neg_dict))
	return train_data
		
if __name__ == '__main__':
	'''
	item_dict = get_item_info(r'../data/ml-latest-small/movies.csv')
	print(len(item_dict))
	print(item_dict['11'])
	'''
	train_data = get_train_data(r'../data/ml-latest-small/ratings.csv')
	print(len(train_data))
	print(train_data[:100])
	
	