#!/usr/bin/env python3
import argparse
import math
import subprocess
import os

def is_prime(n):
	result = subprocess.run(["openssl","prime", str(n)], stdout=subprocess.PIPE)
	output= str(result.stdout)
	return not (output.find("is prime")== -1)

def prime_factors(n: int) -> list[int]:
	factors = []
	# Handle factor 2 separately (only even prime)
	while n % 2 == 0:
		factors.append(2)
		n //= 2
	# Check odd factors up to sqrt(n)
	i = 3
	while i * i <= n:
		while n % i == 0:
			factors.append(i)
			n //= i
		if is_prime(n):
			break
		i += 2
	# If remainder is a prime number > 2
	if n > 1:
		factors.append(n)
	return factors

class CCResult:
	end: int
	def __init__(self):
		self.chain = []
		self.factors = []

def cc1(num):
	start = num
	result = CCResult()
	while is_prime(num):
		result.chain += [num]
		num = 2*num+1
	result.end=num
	result.factors=prime_factors(num)
	return result

def main():
	parser = argparse.ArgumentParser(description="Search for Cunningham chains (type 1) of length m.")
	parser.add_argument("length", type=int, help="Length of chain m")
	args = parser.parse_args()
	m = args.length
	if m == 1:
		print("All primes are candidates for chains of length 1")
	# Check size of m against primes which have 2 as a primitive
	# root and establish the multiplier for k
	primitive_root_primes=(3,5,11,13,19,29,37)
	mul=2
	if m < max(primitive_root_primes):
		for p in primitive_root_primes:
			if (m >= p-1):
				mul *= p
			else:
				break
		print(f"multipler = {mul}")
	else:
		print(f"Chain length currently limited to {max(primitive_root_primes)}")
		exit(1)
	# Establish initial sieve considering primes with order of 2 mod p less than or equal to m
	order_2_mod_p=((),(),(3,),(7,),(5,),(31,),(),(127,),(17,),(73,),(11,),(23,89),(13,),(8191,),(43,))
	for o in order_2_mod_p:
		print(",".join(map(str,o)))

	# Start searching

	k=1
	while True:
		num=mul*k-1
		result=cc1(num)
		print(f"{num}: "+" ".join(map(str,result.chain))+f" length: {len(result.chain)} ({result.end}="+"*".join(map(str,result.factors))+")")
		for p in set(result.chain+result.factors):
			# Process each prime
			print(f"{p}")

if __name__ == "__main__":
	main()
