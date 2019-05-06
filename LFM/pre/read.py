#coding:utf-8
"""
author: Jiede1
date: 2019
"""

import os
def get_item_info(input_file):
	if not os.path.exists(input_file)
		return {}
	lineNum = 0
	item_info = {}
	fp = open(input_file)
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

if __name__ == '__main':
	item_dict = get_item_info('../data/movies.txt')
	print(len(item_dict))
	print(item_dict[1])
	print(item_dict['11'])
	