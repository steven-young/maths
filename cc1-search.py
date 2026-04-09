#!/usr/bin/env python3
import argparse
import math

def main():
	parser = argparse.ArgumentParser(description="Search for Cunningham chains (type 1) of length m.")
	parser.add_argument("length", type=int, help="Length of chain m")
	args = parser.parse_args()
	m = args.length
	if m == 1:
		print("All primes are candidates for chains of length 1")
	# Check size of m against primes which have 2 as a primitive
	# root and establish the multiplier for k
	ps=[3,5,11,13,19,29,37]
	mul=2
	if m < max(ps):
		for p in ps:
			if (m >= p-1):
				mul *= p
			else:
				break
	print(f"multipler = {mul}")

if __name__ == "__main__":
	main()
