import libxml2
import sys
import quiz_library

'''
purpose
	Accept 1 or more log file names on the command line.

	Accumulate across all the log files the pass ratio for each question.

	A question result is considered a pass if it is not 0 or None
	and fail otherwise.

	The pass ratio for a question is the number of passes
	divided by the number of passes + fails.
preconditions
	Each command-line argument is the name of a
	readable and legal quiz log file.

	All the log_files have the same number of questions.
'''

# check number of command line arguments
if len(sys.argv) < 2:
	print 'Syntax:', sys.argv[0], 'quiz_log_file ...'
	sys.exit()

number_of_questions = quiz_library.compute_question_count(quiz_library.load_quiz_log(sys.argv[1]))
results = [0] * number_of_questions

# iterate through all command line arguments computing the pass ratio
for i in range(1,len(sys.argv)):
	log_list = quiz_library.load_quiz_log(sys.argv[i])
	mark_list = quiz_library.compute_mark_list(log_list)

	# sum the results
	for j in range(len(mark_list)):
		results[j] += float(mark_list[j])

# format the output as CSV
output = ""
for num in results:
	input_size = len(sys.argv) - 1
	num /= input_size
	output += str(num) + ","

# don't print final comma
print output[0:-1]