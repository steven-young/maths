#!/usr/bin/env python3
import argparse
import math
import subprocess

def is_prime(n):
	result = subprocess.run(["openssl","prime", str(n)], stdout=subprocess.PIPE)
	output= str(result.stdout)
	return not (output.find("is prime")== -1)

def main():
	parser = argparse.ArgumentParser(description="Check start of Cunningham chain of type 1.")
	parser.add_argument("number", type=int, help="The start of the chain")
	parser.add_argument("start",type=int, help="Start value")
	parser.add_argument("end",type=int, help="End value")
	args = parser.parse_args()
	num = args.number
	for i in range(args.start,args.end+1):
		if is_prime(i):
			result = subprocess.run(["./times-two-mod.py","-c",str(num%i),str(i)], text=True,stdout=subprocess.PIPE)
			output= str(result.stdout)
			l = output.split()
			vals = list(map(int,l[:-1]))
			if 1 in vals:
				ind = vals.index(1)+1
				per = int(l[-1].split("=")[1])
				print(f"{i}: {ind} + {per}k")

if __name__ == "__main__":
	main()
