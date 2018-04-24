# ping sweep
# firstly, we ping to see if the server at ip is alive
# secondly, we test to see if it responds to http request(80)
# information is logged.

import subprocess
import os
import urllib.request
import socket



def log_ping(file_name, msg):
	with open(file_name, "a") as ipFile:
		ipFile.write(msg + "\n")

def http_ping(ip):
	try:
		response = urllib.request.urlopen("http://" + ip).getcode()
		return response
	except:
		return 0
def rdns_lookup(ip):
	try:
		return socket.gethostbyaddr(ip)
	except socket.error:
		return "<couldnt get domain name>"
	
def get_html_title(ip):
	webpage = urllib.request.urlopen("http://" + ip).read()
	html = str(webpage)
	if "<title>" in html: #sometimes the document doesnt have a title tag
		title = html.split('<title>')[1].split('</title>')[0]
		return title
	return "<cant parse title>"
	
	
ip = input("Enter a /24 in the format e.g 110.24.32. : ")	
if ip.count('.') != 3:
	input("IP Format is wrong. Please restart and try again ")
	quit()
		
file_name = ip + "0.txt"
log_ping(file_name, "The format is as follow - <ip address>, <active>, <http response code>, <html title>")
	
with open(os.devnull, "wb") as limbo:
	for n in range(0, 256):
		scan_ip = ip + str(n) #"110.24.32.{0}".format(n)
		result=subprocess.Popen(["ping", "-n", "1", "-w", "200", scan_ip],
		stdout=limbo, stderr=limbo).wait()
		if result:
			msg = scan_ip + " inactive"
			print(msg)
			log_ping(file_name, msg)
		else:
			response = http_ping(scan_ip)
			title = ""
			if response == 200:
				title = get_html_title(scan_ip)
					
			domain = rdns_lookup(scan_ip)
			
			msg = scan_ip + "({0})".format(domain) + " active, " + str(response) + " , " + title
			print(msg)
			log_ping(file_name, msg)
