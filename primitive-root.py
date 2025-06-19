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

def is_coprime(x, y):
	# Check if the GCD of x and y is equal to 1
	return math.gcd(x, y) == 1

def phi(n):
	val = 0
	for k in range(1, n):
		if math.gcd(n, k) == 1:
			val += 1
	return val

def main():
	parser = argparse.ArgumentParser(description="Determine primitive roots.")
	parser.add_argument("number", type=int, help="The integer to analyze")
	args = parser.parse_args()
	num = args.number

	# Loop through numbers that are coprime with num
	print(f"{num} ", end='')
	t = phi(num)
	i = 2
	output = ""
	while i < num:
		if is_coprime(num, i):
			o = 1
			p = i
			line = "("
			while p != 1:
				line += f"{p},"
				p = (p * i) % num
				o += 1
			line += f"{p})"
			if o == t:
				output = line
				break
			else:
				output += line
		i += 1
	print(output)

if __name__ == "__main__":
	main()
