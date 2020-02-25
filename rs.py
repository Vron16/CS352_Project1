import socket as mysoc
import sys

def rs_server():
	if len(sys.argv) != 2:
		raise TypeError('Expected 2 but received %d arguments.' % len(sys.argv))

	port = sys.argv[1]





rs_server()