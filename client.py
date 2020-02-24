import socket as mysoc
import sys
#import threading

# Top-level server helper client task
def ts_client(ts_hostname, ts_listen_port, queried_hostname):
	# Create socket to communicate with the root server
	try:
		ts_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print "[C]: Client socket to communicate with root server created"
	except mysoc.error as err:
		print "[C]: Could not create socket to establish client-top server connection due to error: %s" % err

	# Create tuple that represents the IP address and port number that the root server is listening at, then connect socket to that tuple
	ts_server_binding = (ts_hostname, ts_listen_port)
	ts_socket.connect(ts_server_binding)

	# Send the query to the top-level server
    ts_socket.send(queried_hostname.encode('utf-8'))

    # Wait for and store response received from the top-level server
    ts_response = ts_socket.recv(4096).decode('utf-8')

    # Close socket with top-level server and return the response to the main client task
    ts_socket.close()
    return ts_response

# Root server client task
def rs_client():
	if len(sys.argv) != 4:
		raise TypeError('Expected 4 but received only %d arguments.' % len(sys.argv))
	rs_hostname = sys.argv[1]
	rs_listen_port = sys.argv[2]
	ts_listen_port = sys.argv[3]
	
	# Create socket to communicate with the root server
	try:
		rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print "[C]: Client socket to communicate with root server created"
	except mysoc.error as err:
		print "[C]: Could not create socket to establish client-root server connection due to error: %s" % err

	# Create tuple that represents the IP address and port number that the root server is listening at, then connect socket to that tuple
	rs_server_binding = (rs_hostname, rs_listen_port)
	rs_socket.connect(rs_server_binding)

	# Open the text file containing all the hostnames whose IP addresses we want from the DNS servers. Also create/open an output file to
	# write the hostnames with their corresponding IP addresses (or an error if the IP address did not exist for that hostname in both the
	# root and top-level servers' look-up tables)
	try:
        input_file = open("PROJI-HNS.txt", "r")
        output_file = open("RESOLVED.txt", "w+")
    except IOError as err:
        print "[C]: Could not open input/output file due to error: %s" % err

     # Read hostname queries line by line
    hostname = input_file.readline()
    while hostname:
    	# Print hostname query to terminal console
    	print "[C]: The client is about to query the DNS system for the following hostname: %s" % hostname

    	# Send the query to the root server
    	rs_socket.send(hostname.encode('utf-8'))

    	# Receive response from root server
    	rs_response = rs_socket.recv(4096).decode('utf-8')

    	# Parse it into an array and determine whether the response is an address or a NS hostname
    	rs_response_parsed = rs_response.split()
    	if len(rs_response_parsed) != 3:
    		raise TypeError('Expected response from root server to have 3 words but received %d words' % len(rs_response_parsed))
    	flag = rs_response_parsed[2]

    	# Check if flag is A or NS or invalid.
    	if flag == 'A':
    		 # We've found the IP address for the query. Simply output to terminal and write to output file.
    		 print "[C]: Found the following entry for the requested hostname in the Root Server's table: %s" % rs_response
    		 output_file.write(rs_response + str("\n"))
    	elif flag == 'NS':
    		# The hostname did not exist in the root server's lookup table, and so we received the hostname for the top-level server.
    		ts_hostname = rs_response_parsed[0]
    		# ts_client_thread = threading.Thread(name='ts_client_thread', target=ts_client, args=(ts_hostname, ts_listen_port))

    		# We call a separate function to handle creating a separate socket to connect to the top-level server
    		ts_response = ts_client(ts_hostname, ts_listen_port, hostname)

    		# Parse it into an array and determine whether the response is an address or an error
    		ts_response_parsed = ts_response.split()
    		
    		flag = ts_response_parsed[2]
    		# Check if flag is A or error or invalid.
    		if flag == 'A':
    			# We've found the IP address for the query. Simply output to terminal and write to output file.
    		 	print "[C]: Found the following entry for the requested hostname in the Top-Level Server's table: %s" % ts_response
    		 	output_file.write(ts_response + str("\n"))
    		elif flag == 'Error:HOST':
    			print "[C]: Could not find an IP address for the requested hostname: %s" % ts_response
    			output_file.write(ts_response + str("\n"))
    		else:
    			raise ValueError('The server returned an unrecognized flag')	

    	else:
    		raise ValueError('The server returned an unrecognized flag')

    return

rs_client()