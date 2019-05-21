def personal_rank(graph, root, alpha, item_num, recom_num = 10):
	"""
	Args:
		graph: user item graph
		root: the fixed user for which to recom
		alpha: the prob to go to random walk down
		item_num: iteration num
		recom_num:
	Return:
		a dict, key itemid,value pro
	"""
	rank = {}
	rank = {point:0 for point in graph}
	rank[root] = 1
	for iter_index in iter_num:
		tmp_rank = {}
		tmp_rank = {point:0 for point in graph}
		for out_point,out_dict in graph.items():
			for inner_point,value in graph[out_point]:
				