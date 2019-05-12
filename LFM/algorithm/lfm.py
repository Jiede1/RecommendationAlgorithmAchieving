#coding:utf-8

import numpy as np
import os
print(os.getcwd())
import sys
import operator
sys.path.append('..')
print(sys.path)
from util.read import get_train_data, get_item_info

def lfm(train_data,F,alpha,beta,step):
	"""
	Args:
		train_data: train_data for lfm
		F: user vector len, item vector len
		alpha: regularization factor
		beta: learning rate
		step: iteration num
	Return:
		dict key itemid, value np.ndarray
		dict key userid, value np.ndarray
	"""
	user_vec = {}
	item_vec = {}
	for step_index in range(step):
		for data_instance in train_data:
			userid,itemid,label = data_instance[0],data_instance[1],data_instance[2]
			if userid not in user_vec:
				user_vec[userid] = init_model(F)
			if itemid not in item_vec:
				item_vec[itemid] = init_model(F)
		delta = label - model_predict(user_vec[userid],item_vec[itemid])
		#print(delta, label, model_predict(user_vec[userid],item_vec[itemid]))
		for index in range(F):
			user_vec[userid][index] += beta*(delta*item_vec[itemid][index]) - alpha*user_vec[userid][index]
			item_vec[itemid][index] += beta*(delta*user_vec[userid][index]) - alpha*item_vec[itemid][index]
		beta *= 0.9
	return user_vec,item_vec
	
def init_model(vector_len):
	return np.random.randn(vector_len)

def model_predict(user_vector, item_vector):
	# /
	res = np.dot(user_vector, item_vector) /(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
	return res

def model_train_process():
	# 训练数据
	train_data = get_train_data("../data/ml-latest-small/ratings.csv")
	user_vec,item_vec = lfm(train_data, F = 50 , alpha = 0.01, beta = 0.1, step = 50)
	print('user_vec:',len(user_vec),user_vec['1'])
	print('item_vec:',len(item_vec),item_vec['1'])
	
	recom_list = get_recom_result(user_vec, item_vec, userid = '24')
	
	# 算法预测效果和用户真实评分记录对比
	ana_recom_result(train_data, '24', recom_list)

def get_recom_result(user_vec, item_vec, userid):
	if userid not in user_vec:
		return []
	fix_num = 10
	record = {}
	recom_list = []
	user_vector = 	user_vec[userid]
	for itemid in item_vec.keys():
		item_vector = item_vec[itemid]
		res = model_predict(user_vector, item_vector) 
		record[itemid] = res
	for value in sorted(record.items(), key= operator.itemgetter(1),reverse = True)[:fix_num]:
		itemid = value[0]
		score = round(value[1],3)
		recom_list.append((itemid,score))
	return recom_list
	
def ana_recom_result(train_data, userid, recom_list):
	"""
	debug recom result for userid
	Args:
		train_data
		userid
		recom_list
	Return:
		
	"""
	item_info = get_item_info('../data/ml-latest-small/movies.csv')
	for data_instance in train_data:
		temp_userid,itemid,label = data_instance
		if temp_userid == userid and label == 1:
			print(item_info[itemid])
	print('recom result:')
	for value in recom_list:
		print(item_info[value[0]])
		
	
if __name__ == '__main__':
	model_train_process()
	
	
	

