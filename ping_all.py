#!/usr/bin/python3
import os
import subprocess


def get_hosts():
	hosts ="/etc/hosts"
	hostnames = []
	f =open(hosts, "r")
	lines = f.readlines()
	f.close()

	for line in lines:
		if line[0] != '#':
			if line != '\n':
				line_l = line.split('\t')
				if len(line_l) > 1:
					name = line_l[1]
					if name not in hostnames:
						hostnames.append(name.strip())
	return hostnames


def ping_hosts(host_list):
	nice_count = 0
	naughty_count = 0
	nice_list = []
	naughty_list = []

	for host in host_list:
		if host != "broadcasthost":
			output = subprocess.run(["ping", "-c", "1","-q", host], capture_output=True, text=True)
			print(output.stdout)
			if output.returncode != 0:
				naughty_list.append(host)
				naughty_count += 1
			else:
				nice_list.append(host)
				nice_count += 1
	return {"total_responding": nice_count,
			"total_unresponsive": naughty_count,
			"responding":nice_list,
			"unresponsive": naughty_list}




def main():
	print('-'*70)
	print("Getting host names:")
	hosts = get_hosts()
	host_count = len(hosts)
	print('-'*70)
	print("Executing Pings on hosts:")
	results = ping_hosts(hosts)
	print("************RESULTS************")
	






if __name__ == '__main__':
	main()