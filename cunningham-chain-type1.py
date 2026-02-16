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
        i += 2

    # If remainder is a prime number > 2
    if n > 1:
        factors.append(n)

    return factors

#def is_coprime(x, y):
#	# Check if the GCD of x and y is equal to 1
#	return math.gcd(x, y) == 1

#def phi(n):
#	val = 0
#	for k in range(1, n):
#		if math.gcd(n, k) == 1:
#			val += 1
#	return val

def main():
	parser = argparse.ArgumentParser(description="Print Cunningham chain of type 1.")
	parser.add_argument("number", type=int, help="The start of the chain")
	parser.add_argument("-c","--show_composite",action="store_true",help="Print composite value at end of chain")
	parser.add_argument("-l","--show_length",action="store_true",help="Print length of chain")
	args = parser.parse_args()
	num = args.number
	if (is_prime(num)):
		prev = (num-1)/2.0
		while (prev >= 2 and int(prev) == prev):
			if (is_prime(prev)):
				num=int(prev)
				prev = (num-1)/2.0
			else:
				break
		length = 0
		while (is_prime(num)):
			print(f"{num} ", end='')
			num = 2*num+1
			length += 1
		else:
			if (args.show_composite):
				factors=prime_factors(num)
				print(f"({num}="+"*".join(str(i) for i in factors)+") ", end='')
			if (args.show_length):
				print(f"Chain length {length}", end='')
		print('')
	else:
		factors=prime_factors(num)
		print(f"{num} is composite "+"*".join(str(i) for i in factors))

if __name__ == "__main__":
	main()
