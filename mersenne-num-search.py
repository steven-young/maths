#!/usr/bin/env python3
import argparse
import math
import sys
import json
import os
from primefac import isprime,primefac 
from bisect import bisect_left
from collections import OrderedDict,namedtuple
from operator import attrgetter,itemgetter

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
	number_facts_path = "number_facts.json"
	if os.path.exists(number_facts_path):
		with open(number_facts_path, "r", encoding="utf-8") as f:
			number_facts = json.load(f)
		by_number = itemgetter(0)
	else:
		number_facts = [
			# M101
			fact(2535301200456458802993406410751, 7432339208719),
			fact(2535301200456458802993406410751, 341117531003194129),
			# M125
			# M137
			fact(174224571863520493293247799005065324265471, 32032215596496435569),
			fact(174224571863520493293247799005065324265471, 5439042183600204290159),
			# M139
			fact(696898287454081973172991196020261297061887, 5625767248687),
			fact(696898287454081973172991196020261297061887, 123876132205208335762278423601),
			# M143
			# M149
			fact(713623846352979940529142984724747568191373311, 86656268566282183151),
			fact(713623846352979940529142984724747568191373311, 8235109336690846723986161),
			# M157
			fact(182687704666362864775460604089535377456991567871, 852133201),
			fact(182687704666362864775460604089535377456991567871, 60726444167),
			fact(182687704666362864775460604089535377456991567871, 1654058017289),
			fact(182687704666362864775460604089535377456991567871, 2134387368610417),
			# M167
			fact(187072209578355573530071658587684226515959365500927, 2349023),
			fact(187072209578355573530071658587684226515959365500927, 79638304766856507377778616296087448490695649),
			# M169
			fact(748288838313422294120286634350736906063837462003711, 4057),
			fact(748288838313422294120286634350736906063837462003711, 6740339310641),
			fact(748288838313422294120286634350736906063837462003711, 3340762283952395329506327023033),
			# M173
			fact(11972621413014756705924586149611790497021399392059391, 730753), 
			fact(11972621413014756705924586149611790497021399392059391, 1505447), 
			fact(11972621413014756705924586149611790497021399392059391, 70084436712553223),
			fact(11972621413014756705924586149611790497021399392059391, 155285743288572277679887),
			# M185
			fact(49039857307708443467467104868809893875799651909875269631, 1587855697992791),
			fact(49039857307708443467467104868809893875799651909875269631, 7248808599285760001152755641),
			# M191
			fact(3138550867693340381917894711603833208051177722232017256447, 383),
			fact(3138550867693340381917894711603833208051177722232017256447, 7068569257),
			fact(3138550867693340381917894711603833208051177722232017256447, 39940132241),
			fact(3138550867693340381917894711603833208051177722232017256447, 332584516519201),
			fact(3138550867693340381917894711603833208051177722232017256447, 87274497124602996457),
			# M193
			fact(12554203470773361527671578846415332832204710888928069025791, 13821503),
			fact(12554203470773361527671578846415332832204710888928069025791, 61654440233248340616559),
			fact(12554203470773361527671578846415332832204710888928069025791, 14732265321145317331353282383),
			# M207
			# M209
			fact(822752278660603021077484591278675252491367932816789931674304511, 94803416684681),
			fact(822752278660603021077484591278675252491367932816789931674304511, 1512348937147247),
			fact(822752278660603021077484591278675252491367932816789931674304511, 5346950541323960232319657),
			# M211
			fact(3291009114642412084309938365114701009965471731267159726697218047, 15193),
			fact(3291009114642412084309938365114701009965471731267159726697218047, 60272956433838849161),
			fact(3291009114642412084309938365114701009965471731267159726697218047, 3593875704495823757388199894268773153439)
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
		idx = bisect_left(number_facts, M, key=by_number)
		if idx < len(number_facts):
			if number_facts[idx][0]!=M:
				idx += 1
			while (number_facts[idx][0]==M):
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
					print(f"{mf} has 2 as a primitive root",flush=True)
					prlist.append(mf)
				print(f"The order of 2 mod {mf} is {n}",flush=True)
				order.setdefault(n,[]).append(mf)
			if m==M and len(m_factors)==1:
				# Mersenne prime
				print(f"M{n}={M} is a Mersenne prime",flush=True)
		else:
			print(f"No new info from m={n}",flush=True)
			order[n]=[]
		#breakpoint()
		n += 1
	print("prlist =", json.dumps(prlist),flush=True)
	print("order = ", json.dumps(order),flush=True)
	
if __name__ == "__main__":
	main()
