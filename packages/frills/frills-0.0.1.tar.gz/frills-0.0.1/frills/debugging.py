import sys


def printx(*messages):
	acc_string = ""
	for m in messages: acc_string += str(m)+" "
	print(acc_string)
	sys.exit()


