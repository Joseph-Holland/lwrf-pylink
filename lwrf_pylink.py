#!/usr/bin/python

import sys, string
import httplib
import requests
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 9761

# Domain you want to post to: localhost would be an emoncms installation on your own laptop
# this could be changed to emoncms.org to post to emoncms.org
host = "localhost"

# Location of emoncms in your server, the standard setup is to place it in a folder called emoncms
# To post to emoncms.org change this to blank: ""
emoncmspath = "emoncms"

# Write apikey of emoncms account
apikey = ""

# Node id youd like the emontx to appear as
nodeid = 1

conn = httplib.HTTPConnection(host)

while True:
  # Read in line of readings from emontx serial
  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))

  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  if "pwrMtr" in data:
    print "Received data from UDP"
    print data

    # Split the line at the comma
    array = data.split(',')
    #  array2 = data.split(':')
    #print array[7]

    # split element in list again by :
    cUse = array[7].split(':')

    # print only power usage
    Watts = cUse[1]
    print "Current Watts: "+str(Watts)

    # Send to emoncms
    print "Send data to EmonCMS"
    conn.request("GET", "/"+emoncmspath+"/input/post.json?apikey="+apikey+"&node="+str(nodeid)+"&json={Watts:"+str(Watts)+"}")

    # Get response
    response = conn.getresponse()
    print "Response"
    print response.status, response.reason
    conn.close()