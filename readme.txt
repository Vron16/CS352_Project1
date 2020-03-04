1. Please write down the full names and netids of both your team members. 
Asmaa Hasan (aah150)
Varun Ravichandran (vr250)

2. Briefly discuss how you implemented your recursive client functionality. 
The client has two sockets. The first socket is to communicate with the Root DNS server (RS), and getting a response for the user's query. If the query is not found in the RS. The RS provides the client with the hostname of the Top-level Server (TS). So, the client redirects itself to the TS and tries to find a response to the query in the TS. The action of querying the RS and redirecting to the TS is a form of recursion. Let’s imagine if multiple DNS servers beside TS and RS existed. Assuming each server would refer the client to another server's hostname when it doesn’t have an answer to the client's query, it is on the client to keep calling the other servers. This recursive functionality is implemented by checking the flag of the response from the queried server, if flag == ‘A’, the IP address of the query is found, elif flag == ‘NS’, we parse the response in the search for the TS hostname and port number and connect to it. 

3. Are there known issues or functions that aren't working currently in your attached code? If so, explain. 
We have not found any issues so far. The program compiled successfully and was able to run on different machines.

4. What problems did you face developing code for this project?
Some parts required making decisions such as deciding on how to parse the input and get the right indexing. That involved assuming that testing would follow the same structure of querying given in the project description. In addition, deciding how to thread the program properly and developing the best way to store the IP addresses (ended up in a Python dictionary) were important aspects when developing the code.

5.  What did you learn by working on this project?
 We learned how to make multiple sockets, how DNS works and the process behind requesting an IP address from the internet. Moreover, we got to experiment with how to send and receive data to and from multiple sockets in addition to exploring the nature of recursive functionality implemented in the client. The project helped provide a practical understating of DNS and more exposure to socket programming.

