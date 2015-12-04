import libxml2
import sys

'''
purpose
	store the information from an answer element
'''
class Answer:
	def __init__(self, index, path, result, answer, time):
		self.index = index
		self.path = path
		self.result = result
		self.answer = answer
		self.time = time

'''
purpose
	Store the information from a display element.
'''
class Display:
	def __init__(self, index, path, time):
		self.index = index
		self.path = path
		self.time = time

'''
purpose
	Extract the information from log_file and return it as a list
	of answer and display objects.
preconditions
	log_file is the name of a legal, readable quiz log XML file
'''
def load_quiz_log(log_file):
	# create parse tree using libxml2
	parse_tree = libxml2.parseFile(log_file)
	context = parse_tree.xpathNewContext()
	root = parse_tree.getRootElement()

	# parse the quiz log creating Answer and Display objects based on xml file
	log_list = []
	log = root.children
	while log is not None:
		if log.name == "answer":
			c = log.children
			while c is not None:
				if c.name == "index":
					index = int(c.content)
				if c.name == "path":
					if c.content == "":
						path = "None"
					else:
						path = c.content
				if c.name == "result":
					if c.content == "":
						result = "None"
					else:
						result = int(c.content)
				if c.name == "answer":
					if c.content == "":
						answer = "None"
					else:
						answer = c.content
				if c.name == "time":
					if c.content == "":
						time = "None"
					else:
						time = int(c.content)
				c = c.next
			log_list.append(Answer(index, path, result, answer, time))
		if log.name == "display":
			c = log.children
			while c is not None:
				if c.name == "index":
					index = int(c.content)
				if c.name == "path":
					if c.content == "":
						path = "None"
					else:
						path = c.content
				if c.name == "time":
					time = int(c.content)
				c = c.next
			log_list.append(Display(index, path, time))
		log = log.next

	return log_list


'''
purpose
	Return the number of distinct questions in log_list.
preconditions
	log_list was returned by load_quiz_log
'''
def compute_question_count(log_list):
	
	# count the number of Answer objects in log_list occuring before the first Display object
	count = 0
	for item in log_list:
		if isinstance(item, Display):
			break
		else:
			count += 1

	return count

'''
purpose
	Extract the list of marks.
	For each index value, use the result from the last non-empty answer,
	or 0 if there are no non-empty results.
preconditions
	log_list was returned by load_quiz_log
'''
def compute_mark_list(log_list):
	mark_list = [0] * compute_question_count(log_list)

	# iterate through each Answer in log_list storing and update mark_list at the appropriate index (initialized to 0s)
	for item in log_list:
		if isinstance(item, Answer):
			if type(item.result) == int:
				mark_list[int(item.index)] = int(item.result)

	return mark_list
