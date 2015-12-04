import libxml2
import sys
import quiz_library

'''
purpose
	Accept 1 or more log file names on the command line.

	For each log file, compute the total time taken for each question. 

	Write to standard output, the average time spent for each question.
preconditions
	Each command-line argument is the name of a readable and
	legal quiz log file.

	All the log_files have the same number of questions.
'''

# handle command line arguments
if len(sys.argv) < 2:
	print 'Syntax:', sys.argv[0], 'quiz_log_file ...'
	sys.exit()

number_of_questions = quiz_library.compute_question_count(quiz_library.load_quiz_log(sys.argv[1]))
time_taken_list = [0.0] * number_of_questions

# iterate through all command line arguments
for i in range(1,len(sys.argv)):
	log_list = quiz_library.load_quiz_log(sys.argv[i])

	initial_time = None
	current_index = None

	# sum the time spent on each question (computed as time where question 2 is displayed minus time where question 1 is displayed)
	for item in log_list:
		if isinstance(item, quiz_library.Display):
			if initial_time is not None:
				elapsed_time = item.time - initial_time
				time_taken_list[current_index] += float(elapsed_time)
			current_index = item.index
			initial_time = item.time

		# account for last item in list
		if item is log_list[-1]:
			elapsed_time = item.time - initial_time
			time_taken_list[current_index] += elapsed_time

# format the output as CSV
output = ""
for time in time_taken_list:
	input_size = len(sys.argv) - 1
	time /= input_size
	output += str(time) + ","

# don't print final comma
print output[0:-1]