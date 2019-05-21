import os
def get_graph_from_data(input_file):
	"""
	Args:
		input_file:
	Return:
		a dict: {userA:{itema:1,itemb:1},{item1:{userA:1}}}
	"""
	filepath = os.path.dirname(os.path.abspath(__file__))
	input_file = filepath+'/'+input_file
	if not os.path.exists(input_file):
		print('path is not exist')
		return {}
	graph ={}
	lineNum = 0
	score_thr = 3.0
	fp = open(input_file,'r')
	for line in fp:
		if lineNum == 0:
			lineNum += 1
			continue
		item = line.strip().split(',')
		if len(item) < 3:
			continue
		userid, itemid, score = item[0], 'item_'+ item[1], float(item[2])
		if float(score) < score_thr:
			continue
		if userid not in graph:
			graph[userid] = {}
		graph[userid][itemid] = 1
		if itemid not in graph:
			graph[itemid] = {}
		graph[itemid][userid] = 1
	return graph

if __name__ == '__main__':
	print(get_graph_from_data(input_file = '../data/ratings.csv'))
