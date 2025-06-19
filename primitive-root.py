#!/usr/bin/env python3
import argparse
import math

def is_prime(n):
	if n <= 1:
		return False
	if n <= 3:
		return True
	if n % 2 == 0 or n % 3 == 0:
		return False
	i = 5
	while i * i <= n:
		if n % i == 0 or n % (i + 2) == 0:
			return False
		i += 6
	return True

def gcd(p, q):
	# Use Euclid's algorithm to find the GCD
	while q != 0:
		p, q = q, p % q
	return p

def is_coprime(x, y):
	# Check if the GCD of x and y is equal to 1
	return gcd(x, y) == 1

def main():
	parser = argparse.ArgumentParser(description="Determine primitive roots.")
	parser.add_argument("number", type=int, help="The integer to analyze")
	args = parser.parse_args()
	num = args.number

	# Loop through numbers that are prime to the integer
	#print(f"{num} is {'a prime number' if is_prime(num) else 'not prime number'}.")
	print(f"{num} ", end='')
	i = 2;
	while i < num:
		if is_coprime(num, i):
			o = 1
			p = i
			line = "("
			while p != 1:
				line += f"{p},"
				p = (p * i) % num
			line += f"{p})"
			print(line, end='')
		i += 1
	print()

if __name__ == "__main__":
	main()
