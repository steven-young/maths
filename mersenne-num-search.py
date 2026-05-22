#!/usr/bin/env python3
import argparse
import math
import sys
from primefac import isprime,primefac 
from collections import OrderedDict

def main():
	# Script will search through Mersenne numbers to determine
	# the order of 2 for the primes encountered

	# Algorithm description:
	# Consider a Mersenne number M_n.
	# If M_n is prime then this implies that the order of 2 mod M_n is n
	# If n isn't prime, then for k|n, then M_k|M_n.  Also if
	# M_k**j|n, then M_k**(j+1)|M_n
	# Divide M_n by all of these divisors to obtain m_n and
	# For any factor f of m_n, the order of 2 mod f is n
	parser = argparse.ArgumentParser(description="Search Mersenne numbers to determine order of 2 mod p.")
	parser.add_argument("-n","--start_n", type=int,default=2,help="Start n value")
	args = parser.parse_args()

	prlist = []
	order = {}
	n = args.start_n
	while True:
		M = 2**n - 1
		M_factors = [1]
		if not isprime(n):
			# Determine divisors
			n_factors=list(primefac(n))
			uniq_n_factors = list(OrderedDict.fromkeys(n_factors))
			M_factors = []
			for k in uniq_n_factors:
				j = 1
				Mk = 2**k - 1
				F = Mk
				while n%F == 0:
					j += 1
					F = F*Mk
				for i in range(j):
					M_factors.append(Mk)
		m = M
		for f in M_factors:
			# Might want to check that f can divide into m
			if m%f != 0:
				print("Problem: {f} doesn't divide into {m}")
			m //= f
		if m > 1:
			m_factors = list(primefac(m))
			for mf in m_factors:
				if mf==n+1:
					# Primitive root
					print(f"{mf} has 2 as a primitive root")
					prlist.append(mf)
				else:
					order.setdefault(n,[]).append(mf)
			if m==M and len(m_factors)==1:
				# Mersenne prime
				print(f"M{n}={M} is a Mersenne prime")
		else:
			print(f"No new info from m={n}")
		breakpoint()
		n += 1
	
if __name__ == "__main__":
	main()
