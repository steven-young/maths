#!/usr/bin/env python3
import argparse
import math

def main():
	parser = argparse.ArgumentParser(description="Print num times two sequence mod n")
	parser.add_argument("number", type=int, help="Number")
	parser.add_argument("modulus", type=int, help="Modulus")
	parser.add_argument("-c","--show_count",action="store_true",help="Show count of modulo sequence")
	args = parser.parse_args()
	num = args.number
	mod = args.modulus
	print(f"{num} ", end='')
	count = 1
	cur = (num*2)%mod
	while (cur != num):
		print(f"{cur} ",end='')
		cur = (cur*2)%mod
		count += 1
	if (args.show_count):
		print(f"count={count}",end='')
	print('')

if __name__ == "__main__":
	main()
