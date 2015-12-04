import libxml2
import sys
import quiz_library

'''
purpose
	Accept 1 or more log file names on the command line.
	For each log file
		write to standard output the course mark for the log file,
		in CSV format
preconditions
	Each command-line argument is the name of a legal, readable quiz log file.

	All of the log files have the same number of questions.
'''

# handle command line arguments
if len(sys.argv) < 2:
	print 'Syntax:', sys.argv[0], 'quiz_log_file ...'
	sys.exit()

# iterate through all command line arguments counting the number of correct answers
for i in range(1,len(sys.argv)):
	quiz_mark = 0
	log_list = quiz_library.load_quiz_log(sys.argv[i])
	mark_list = quiz_library.compute_mark_list(log_list)

	# count the correct results
	for mark in mark_list:
		if mark == 1:
			quiz_mark += 1

	print sys.argv[i] + "," + str(quiz_mark)