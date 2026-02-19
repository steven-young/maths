#!/usr/bin/env python3
import argparse
import math

cont_count = 20

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

def cc1(num, args):
	global cont_count
	start = args.number
	if (is_prime(num)):
		prev = (num-1)/2.0
		reported_start = False
		while (prev >= 2 and int(prev) == prev):
			if (is_prime(prev)):
				if (args.report_not_start and not reported_start):
					print(f"{start} not start of chain: ", end='', flush=True)
					reported_start = True
				num=int(prev)
				prev = (num-1)/2.0
			else:
				break
		length = 0
		while (is_prime(num)):
			print(f"{num} ", end='', flush=True)
			num = 2*num+1
			length += 1
		else:
			if (args.show_length):
				print(f"Chain length {length} ", end='', flush=True)
			if (args.show_end):
				factors=prime_factors(num)
				print(f"({num}="+"*".join(str(i) for i in factors)+") ", end='', flush=True)
			if (args.continuous):
				if (cont_count > 0 or args.cont_count == 0):
					print("(", end='', flush=True)
					while (not is_prime(num)):
						factors=prime_factors(num)
						print(f"{num}="+"*".join(str(i) for i in factors)+" ", end='', flush=True)
						num = 2*num+1
						if (args.continuous):
							cont_count = cont_count - 1
					print(f"{num} is next prime) ", end='', flush=True)
		print('', flush=True)
	else:
		factors=prime_factors(num)
		print(f"{num} is composite "+"*".join(str(i) for i in factors)+" ",end='', flush=True)
		if (args.continuous):
			if (cont_count > 0 or args.cont_count == 0):
				num = 2*num+1
				while (not is_prime(num)):
					factors=prime_factors(num)
					print(f"{num}="+"*".join(str(i) for i in factors)+" ", end='', flush=True)
					num = 2*num+1
					if (args.continuous):
						cont_count = cont_count - 1
				print(f"{num} is next prime) ", end='', flush=True)
		print('', flush=True)
	return num

def main():
	global cont_count
	parser = argparse.ArgumentParser(description="Print Cunningham chain of type 1.")
	parser.add_argument("number", type=int, help="The start of the chain")
	parser.add_argument("-e","--show_end",action="store_true",help="Print composite value at end of chain")
	parser.add_argument("-l","--show_length",action="store_true",help="Print length of chain")
	parser.add_argument("-n","--report_not_start",action="store_true",help="Report if chain doesn't start with number")
	parser.add_argument("-c","--continuous",action="store_true",help="Continue along the chain for a few more steps")
	parser.add_argument("--cont_count",type=int,default=20,help="Count of how long to continue...")
	args = parser.parse_args()
	num = args.number
	if (args.continuous):
		if (args.cont_count != 0):
			cont_count = args.cont_count
		while (cont_count > 0 or args.cont_count == 0):
			num = cc1(num, args)
	else:
		num = cc1(num, args)

if __name__ == "__main__":
	main()
