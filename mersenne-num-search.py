#!/usr/bin/env python3
import argparse
import math
import sys
import json
from primefac import isprime,primefac 
from bisect import bisect_left
from collections import OrderedDict,namedtuple
from operator import attrgetter

def bits_idx(n):
	while n:
		b = n & (~n+1)
		yield b.bit_length() - 1
		n ^= b

def main():
	# Script will search through Mersenne numbers to determine
	# the order of 2 for the primes encountered

	# Algorithm description:
	# Consider a Mersenne number M_n.
	# If M_n is prime then this implies that the order of 2 mod M_n is n
	# If M_n isn't prime, then for the prime factors f of M_n which aren't
	# represented in the lists of factors for M_k, k<n, the order
	# of 2 mod f is n
	# If n isn't prime, then for k|n, then M_k|M_n.  More
	# specifically though for the prime factors f for which the order of 2
	# mod f is k, then f|M_n.  Further, if f**j|n, for some j,
	# then f**(j+1)|M_n
	# Divide M_n by all of these divisors to obtain m_n and
	# for any factor f of m_n, the order of 2 mod f is n
	parser = argparse.ArgumentParser(description="Search Mersenne numbers to determine order of 2 mod p.")
	parser.add_argument("-n","--start_n", type=int,default=2,help="Start n value")
	parser.add_argument("-e","--end_n", type=int,default=0,help="End n value")
	args = parser.parse_args()

	# Here are some number facts to make things work better.
	# Specifically, the number facts tuple contains tuples where
	# the second item is a factor of the first item
	fact = namedtuple('fact', ('number', 'factor'))
	number_facts = [
		# M101
		fact(2535301200456458802993406410751, 7432339208719),
		fact(2535301200456458802993406410751, 341117531003194129),
		# M137
		fact(174224571863520493293247799005065324265471, 32032215596496435569),
		fact(174224571863520493293247799005065324265471, 5439042183600204290159),
		# M149
		fact(713623846352979940529142984724747568191373311, 86656268566282183151),
		fact(713623846352979940529142984724747568191373311, 8235109336690846723986161)
	]
	by_number = attrgetter('number')
	number_facts.sort(key=by_number)

	prlist = []
	order = {}
	n = args.start_n
	while not (args.end_n != 0 and n > args.end_n):
		M = 2**n - 1
		M_factors = [1]
		if not isprime(n):
			# Determine divisors
			n_divisors=list(primefac(n))
			l = len(n_divisors)
			for i in range(2**l-1):
				if i.bit_count() > 1:
					val = 1
					for j in bits_idx(i):	
						val *= n_divisors[j]
					n_divisors.append(val)
			uniq_n_divisors = list(OrderedDict.fromkeys(n_divisors))
			M_factors = []
			for k in uniq_n_divisors:
				j = 1
				for f in order[k]:
					F = f
					while n%F == 0:
						j += 1
						F = F*f
					for i in range(j):
						M_factors.append(f)
		m = M
		for f in M_factors:
			# Might want to check that f can divide into m
			if m%f != 0:
				print("Problem: {f} doesn't divide into {m}")
			m //= f
		m_factors = []
		idx = bisect_left(number_facts, m, key=by_number)
		if idx < len(number_facts):
			if number_facts[idx][0]!=m:
				idx += 1
			while (number_facts[idx][0]==m):
				m_factors.append(number_facts[idx][1])
				idx += 1
				if idx == len(number_facts):
					break
		if m > 1:
			if len(m_factors) == 0:
				m_factors = list(primefac(m))
			for mf in m_factors:
				if mf==n+1:
					# Primitive root
					print(f"{mf} has 2 as a primitive root")
					prlist.append(mf)
				print(f"The order of 2 mod {mf} is {n}")
				order.setdefault(n,[]).append(mf)
			if m==M and len(m_factors)==1:
				# Mersenne prime
				print(f"M{n}={M} is a Mersenne prime")
		else:
			print(f"No new info from m={n}")
			order[n]=[]
		#breakpoint()
		n += 1
	print("prlist =", json.dumps(prlist))
	print("order = ", json.dumps(order))
	
if __name__ == "__main__":
	main()
