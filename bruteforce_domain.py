# script to bruteforce domains

import string
import socket
import itertools


from itertools import combinations, product

symbols = "abcdefghijklmnopqrstuvwxyz0123456789-"
max_length = len(symbols)


###########################################################
# https://stackoverflow.com/questions/4719850/python-combinations-of-numbers-and-letters
# iterator way of permutating - saves memory
# generator of all combinations allowing repetitions
def permutate_combinations(chars=symbols, min_len = 1, max_len = max_length):
    for length in range(min_len, max_len):
        for word in map(''.join, product(*[symbols]*length)):
            yield word
			
def generate(chars, length, prefix = None):
    if length < 1:
        return
    if not prefix:
        prefix = ''
    for char in chars:
        permutation = prefix + char
        if length == 1:
            yield permutation
        else:
            for sub_permutation in generate(chars, length - 1, prefix = permutation):
                yield sub_permutation			
			
def promptYesNo(message):
	reply = input(message)
	if reply and (reply[0] == 'y' or reply[0] == 'Y'):
		return True
	return False
	
def resolve_host(domain):
	try:
		socket.gethostbyname(domain)
		return True
	except socket.error:
		return False
		
def nslookup(domain):
	ip_list = []
	
	return socket.gethostbyname(domain)

# If domain has wildcard, then our algorithm needs to be slightly changed
# though it may bring about false results. We can however, improve it by using a 
# rdns tool (though not necessarily accurate too)
def wildcard_exists(domain):
	return resolve_host("*." + domain)
def get_wildcard_ip(domain):
	return socket.gethostbyname("*." + domain)

	
def is_qualified_domain(domain):
	return (domain.count(".") >= 1) # a rough check - more detailed is to ensure its at least x.x


def empty_log(domain):
	open(domain + ".txt", "w").close()
	
def log_resolved_domain(domain, ip):
	with open(domain + ".txt", "a") as ipFile:
		ipFile.write(domain + ", " + ip + "\n")

def bruteforce_log(msg):
	with open("bruteforce_domains.txt", "a") as ipFile:
		ipFile.write(msg + "\n")
		
	
def bruteforce_domain(domain, level, minChar, maxChar, prefix, enableLog):
	resolved_domains = []
	
	wildcard_ip  = ""
	has_wildcard = wildcard_exists(domain)
	print("Wildcard detected : %r" % has_wildcard)
	if has_wildcard:
		print("Resolving by nslookup(gethostbyname) while a wildcard exists may have false results")
		result = promptYesNo("Continue?")
		if not result:
			quit()
		wildcard_ip = get_wildcard_ip(domain)
		print("wildcard_ip : " + wildcard_ip)
	else:
		print("No wildcard A record detected")
		
	#has_wildcard = True
	#wildcard_ip = "xxx.xxx.xxx.xx"
		
	if maxChar <= 0 or minChar <= 0 :
		print("maxChar or minChar minimum is 1")
		return []
		
	lower_a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	special = ['-']
	
	all = []
	all = lower_a + num + special

	for i in range(minChar, maxChar):
		for permutation in generate(symbols, i, ''):
			#do something with word
			#print(word)	
			domain_name = permutation + '.' + domain

			#print(' '.join(s))
			if len(prefix) > 0:
				if not domain_name.startswith(prefix):
					continue

			print("Resolving domain : " + domain_name)		
			
			if resolve_host(domain_name):
				ip = nslookup(domain_name)
				if ip == wildcard_ip:
					print("	Wildcard detected, skipping result")
				else:
					resolved_domains.append(domain_name + " : " + ip)
					if enableLog:
						log_resolved_domain(domain_name, ip)
						
					print("	Resolved domain")
			else:
				print("	Failed to resolve domain")
				# if we want multi level domain, we should do it here
				
		#bruteforce_log("Finished " + str(r) + " characters")
	return resolved_domains
	##
	
	for word in permutate_combinations(symbols, minChar, maxChar):
		#do something with word
		#print(word)	
		domain_name = word + '.' + domain

		#print(' '.join(s))
		if len(prefix) > 0:
			if not domain_name.startswith(prefix):
				continue

		print("Resolving domain : " + domain_name)		
		
		if resolve_host(domain_name):
			ip = nslookup(domain_name)
			if ip == wildcard_ip:
				print("	Wildcard detected, skipping result")
			else:
				resolved_domains.append(domain_name + " : " + ip)
				if enableLog:
					log_resolved_domain(domain_name, ip)
					
				print("	Resolved domain")
		else:
			print("	Failed to resolve domain")
			# if we want multi level domain, we should do it here
		#bruteforce_log("Finished " + str(r) + " characters")
		
		
	return resolved_domains	 
	#########################################################################
	
	for r in range(minChar, maxChar):
		for s in itertools.product(all, repeat=r):
			domain_name = ''.join(s) + '.' + domain

			#print(' '.join(s))
			if len(prefix) > 0:
				if not domain_name.startswith(prefix):
					continue

			print("Resolving domain : " + domain_name)		
			
			if resolve_host(domain_name):
				ip = nslookup(domain_name)
				if ip == wildcard_ip:
					print("	Wildcard detected, skipping result")
				else:
					resolved_domains.append(domain_name + " : " + ip)
					if enableLog:
						log_resolved_domain(domain_name, ip)
						
					print("	Resolved domain")
			else:
				print("	Failed to resolve domain")
				# if we want multi level domain, we should do it here
		bruteforce_log("Finished " + str(r) + " characters")
		
	return resolved_domains	 
	




	
	

	
domain = input("Enter the domain you wish to bruteforce : ")
#if not reply
#	print("Enter a domain and try again")
#	quit()
prefix  = input("Enter the prefix of your subdomain or leave blank to not specify any : ")
minChar = int(input("Enter min char : "))
maxChar = int(input("Enter max char : "))	
#level = int(input("Enter level : "))
log = promptYesNo("Enable logging ? : ")
if log:
	empty_log(domain)
	
resolved_domains = bruteforce_domain(domain, 1, minChar, maxChar, prefix, log)
if resolved_domains and len(resolved_domains) > 0:
	print("\nSuccessfully resolved domain(s) : ")
	print('\n'.join(resolved_domains))
else:
	print("no domains resolved")
	
