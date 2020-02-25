import threading
import time
import random
import socket as mysoc

# server task
def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    server_binding=('',50007)
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)

# create DNS table
    dns={"qtsdatacenter.aws.edu":["128.60.3.2", 'A'],"www.rutgers.com":["192.64.4.4","A"],
         "mx.rutgers.com":['192.64.4.5', 'A'], "grep.cs.princeton.edu":['182.49.3.2','A'],"www.ibm.com":
             ["64.42.3.4","A"],"www.google.edu": ["8.7.45.2", "A"]}
# receive message from the client.

    data_from_client= csockid.recv(100)
    print("[S]: Data received from client::  ",data_from_client.decode('utf-8'))
    hostname_requested = data_from_client.decode('utf-8')

    if hostname_requested in dns:
        dns_result= dns.get(hostname_requested);
    else:
        dns_result= 'Error:HOST NOT FOUND';

    print("[S]: Data sent to client:: ", dns_result.encode('utf-8'))

   # Close the server socket
    ss.close()
    exit()
