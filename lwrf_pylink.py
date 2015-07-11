#!/usr/bin/python

import sys, string
import httplib
import requests
import socket

# Define IP address and port to listen on.
# UDP 9761 is the default for this on the WiFiLink.
UDP_IP = "0.0.0.0"
UDP_PORT = 9761

# Host you want to post to: localhost would be an
# emoncms installation on this computer, this could
# be changed to emoncms.org to post to emoncms.org.
host = "<host>"

# Location of emoncms install on your server, the 
# standard setup is to place it in a folder called emoncms
# To post to emoncms.org change this to blank: ""
emoncmspath = "emoncms"

# Write the apikey of emoncms account.
apikey = "<apikey>"

# Node id youd like the feed to appear from.
nodeid = 1

# Define HTTP connection to emoncms host.
conn = httplib.HTTPConnection(host)

# Start loop to listen for UDP packets from the
# LightwaveRF WiFiLink and once recieved, clean
# the data up and send to emoncms.
while True:
  try:
    # Read in line of readings from UPD port.
    sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  except Exception, msg:
    print "Error capturing UDP packets."
    print msg
  else:
    # We've got a UDP packet successfully, do some checking
    # and processing and then send to emoncms.

    # Ensure the data has pwrMtr in the string captured.
    # We need to do this otherwise we would catch the 
    # other command packets here too, i.e. turn on light X.
    if "pwrMtr" in data:
      # Some logging to console.  I run this via screen
      # and this suits best instead of sending to a log.
      print "Received data from UDP"
      print data

      # Split the line at the comma
      array = data.split(',')

      # split element in list again by ":"
      cUse = array[7].split(':')

      # Print only power usage to console.
      Watts = cUse[1]
      print "Current Watts: "+str(Watts)

      try:
        # Send to emoncms.
        print "Send data to EmonCMS"
        conn.request("GET", "/"+emoncmspath+"/input/post.json?apikey="+apikey+"&node="+str(nodeid)+"&json={Watts:"+str(Watts)+"}")

        # Get response.
        response = conn.getresponse()
        print "Response"
        print response.status, response.reason
        # Important ro remember to close the connection!
        conn.close()
      except Exception, msg:
        print "Error sending to emoncms."
        print msg
