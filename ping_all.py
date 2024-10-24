#!/usr/bin/python3
import os
import subprocess


def get_hosts():
	hosts ="/etc/hosts"
	exclude = ["broadcasthost","localhost"]
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
					hostnames.append(name.strip())

	return [host for host in hostnames if host not in exclude]


def ping_hosts(host_list):
	nice_count = 0
	naughty_count = 0
	nice_list = []
	naughty_list = []

	for host in host_list:
		output = subprocess.run(["ping", "-c", "4","-q", host], capture_output=True, text=True)
		print(output.stdout)
		print('-'*70)
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
	print("{} % of hosts are responsive.".format(( results["total_responding"] / host_count )*100))
	if results["total_unresponsive"] > 0:
		print('-'*70)
		print("The following hosts are not responding:")
		for host in results["unresponsive"]:
			print(host)
	print('-'*70)


if __name__ == '__main__':
	main()