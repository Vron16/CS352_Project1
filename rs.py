import socket as mysoc
import sys
import threading

# Each client connection handler thread runs this function.
def handle_connection(connection_socket, rs_dns_table, ts_information):
	while 1:
		# Using the client connection socket passed in from the main thread, wait to receive data from the
		# client using recv. Save the query in client_query after decoding it with UTF-8.
		client_query = connection_socket.recv(4096).decode('utf-8').strip().lower()
		print "[RS]: Received request to find IP address for the hostname:", client_query
		# Now, check if the rs_dns_table dictionary contains a key corresponding to the hostname queried by the
		# client. If so, create the string as it appeared in the file and send it back to the client. Otherwise,
		# send ts_information so that client can connect with the top-level server.
		if client_query in rs_dns_table:
			address_response = rs_dns_table[client_query]
			print "[RS]: Found query in root server DNS table. Sending following string back to client:", address_response
			connection_socket.send(address_response.encode('utf-8'))
		elif client_query == 'done':
			break
		else:
			print "[RS]: Could not locate", client_query, "in root server DNS table. Sending following top-level server hostname back to client:", ts_information
			connection_socket.send(ts_information.encode('utf-8'))
	# Close the connection with the client and return
	connection_socket.close()
	return

# This function is what runs at startup, populates the root server's DNS table, sets up and binds to the socket based on the specified
# port, and then listens for incoming connections. When they are received, a new child thread is spawned to handle it.
def rs_server():

	if len(sys.argv) != 2:
		raise TypeError('[RS]: Expected 2 but received %d arguments.' % len(sys.argv))

	# The port that the root server will listen on is provided as the sole argument to the program call.
	port = int(sys.argv[1])

	# Opens PROJI-DNSRS.txt and reads in contents line by line. All lines that end with the flag A are stored
	# into a dictionary. There should be only one line with the NS flag, which will be saved in a local str
	# variable as the response in case the client needs to reconnect to the top-level server.
	input_file = open("PROJI-DNSRS.txt", "r")
	line = input_file.readline()
	rs_dns_table = {}
	ts_information = ''
	while line:
		line_parsed = line.split()
		hostname = line_parsed[0].strip()
		hostname_lowercase = hostname.lower()
		ip_address = line_parsed[1]
		flag = line_parsed[2]
		if flag == 'A':
			rs_dns_table[hostname_lowercase] = line.strip()
		elif flag == 'NS':
			ts_information = line.strip()
		else:
			raise ValueError("[RS]: Error - PROJI-DNSRS.txt file contains unrecognized flags.")
		line = input_file.readline()

	input_file.close()
	# Attempts to create a socket for the root server to listen from. Communicates with IPV4 via TCP.
	try:
		rs_server_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print "[RS]: Root Server socket created."
	except mysoc.error as err:
		print "[RS]: Could not create socket for root server to listen to connections from due to error:", err

	# Bind the server socket to the IP address of the machine it is running on and the port provided as input. 
	host = mysoc.gethostname()
	print "[RS]: Root server host name is:", host
	host_ip = mysoc.gethostbyname(host)
	print "[RS]: Root server host IP address is:", host_ip 
	rs_server_binding = ('', port)
	rs_server_socket.bind(rs_server_binding)

	# Listen to up to 10 connections at a time from clients
	rs_server_socket.listen(10)

	while 1:
		# Call accept to block and wait for any new incoming connection requests to the socket and accept them.
		connection_socket, addr = rs_server_socket.accept()
		print "[RS]: Received a connection request from a client at:", addr

		# Create a new thread to serve the client while the current thread continues listening for connections.
		connection_handler_thread = threading.Thread(name='connection_handler', target=handle_connection, args=(connection_socket, rs_dns_table, ts_information))
		connection_handler_thread.start()

	rs_server_socket.close()
	return

rs_server()