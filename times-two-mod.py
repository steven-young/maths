#!/usr/bin/env python3
import argparse
import math

def main():
	parser = argparse.ArgumentParser(description="Print num times two sequence mod n")
	parser.add_argument("number", type=int, help="Number")
	parser.add_argument("modulus", type=int, help="Modulus")
	parser.add_argument("-c","--show_count",action="store_true",help="Show count of modulo sequence")
	parser.add_argument("-s","--stop", type=int,default=0,help="Stop after stop steps")
	args = parser.parse_args()
	num = args.number
	mod = args.modulus
	stop = args.stop
	stopped = False
	count = 1
	if mod==0:
		cur = num*2
	else:
		if num > mod:
			num = num%mod
		cur = (num*2)%mod
	print(f"{num} ", end='')
	while (cur != num):
		print(f"{cur} ",end='')
		if mod==0:
			cur = cur*2
		else:
			cur = (cur*2)%mod
		count += 1
		if (count > stop and stop != 0):
			stopped = True
			break
	if (args.show_count and not stopped):
		print(f"count={count}",end='')
	print('')

if __name__ == "__main__":
	main()
