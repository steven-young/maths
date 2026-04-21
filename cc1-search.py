#!/usr/bin/env python3
import argparse
import math
import subprocess
import os
import sys
import signal
from primefac import isprime,primefac 

LINE_CLEAR = '\x1b[2K'

k=1

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def signal_handler(sig, fram):
	global k
	print()
	print(f"k={k}")
	sys.exit(0)

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
	while isprime(num):
		result.chain += [num]
		num = 2*num+1
	result.end=num
	result.factors=list(primefac(num))
	return result

def k_mod(p,i,mul):
	mk_list = [1]
	for j in range(2,i+1):
		if mk_list[j-2]%2 == 0:
			mk_list.append(mk_list[j-2]//2)
		else:
			mk_list.append((mk_list[j-2]+p)//2)
	#print("p =", p, "mk_list =", mk_list)
	#index_list = list(range(1,p+1))
	#mulk_modp_list = [ mul * i % p for i in index_list]
	#print("mulk_modp_list = ", mulk_modp_list)
	k_list = []
	k1 = pow(mul, p-2, mod=p)
	for v in mk_list:
		k_list.append(k1*v%p)
	return k_list

def main():
	global k
	signal.signal(signal.SIGINT, signal_handler)	
	signal.signal(signal.SIGQUIT, signal_handler)	
	signal.signal(signal.SIGTERM, signal_handler)	
	parser = argparse.ArgumentParser(description="Search for Cunningham chains (type 1) of length m.")
	parser.add_argument("length", type=int, help="Length of chain m")
	parser.add_argument("-k","--start_k", type=int,default=1,help="Start k value")
	parser.add_argument("-l","--limit_sieve_size",action="store_true",help="Limit sieve size")
	parser.add_argument("-s","--sieve_size_limit", type=int,default=5000,help="Sieve size limit")
	parser.add_argument("-p","--progress",action="store_true",help="Print progress")
	parser.add_argument("-n","--shorter_chain_length", type=int,default=0,help="Shorter chain length to print")
	args = parser.parse_args()
	m = args.length
	if (args.shorter_chain_length == 0):
		n = m
	else:
		n = args.shorter_chain_length
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
		print(f"multipler = {mul}", flush=True)
	else:
		print(f"Chain length currently limited to {max(primitive_root_primes)}")
		exit(1)

	# Establish initial sieve considering primes with order of 2 mod p less than or equal to m
	init_sieve_mod = {}
	init_sieve_to = {}
	sieve_mod = {}
	sieve_to = {}
	sieve_cur = {}
	order_2_mod_p=((),(),(),(7,),(),(31,),(),(127,),(17,),(73,),(),(23,89),(),(8191,),(43,),(151,),(257,),(131071,),(),(524287,),(41,),(337,),(683,),(47,178481),(241,),(601,1801),(2731,),(262657,),(113,),(233,1103,2089),(331,),(2147483647,),(65537,),(599479,),(43691,),(71,122921),(109,))
	for i in range(3,m):
		for p in order_2_mod_p[i]:
			# Construct a set of values mod p where k*mul*2^j-1 for j in range(i)
			if args.progress:
				eprint(end=LINE_CLEAR)
				eprint(f"k=0 ss={len(sieve_to)} Adding p={p} to sieve",end='\r')
			init_sieve_mod[p] = k_mod(p,i,mul)
			init_sieve_to[p] = 0
			#print("sieve_dict = ", sieve_dict)

	# Start searching
	k=args.start_k
	sieve_vals=set()
	sieve_mod = dict(init_sieve_mod)
	sieve_to = dict(init_sieve_to)
	while True:
		# Skip k values depending on sieve_list
		prev_k=k
		while any(s<=k for s in iter(sieve_to.values())):
			for p in sieve_to:
				if k >= sieve_to[p]:
					if args.progress:
						eprint(end=LINE_CLEAR)
						eprint(f"k={k} ss={len(sieve_to)} sv={len(sieve_vals)} Updating sieve values for p={p}",end='\r')
					sieve_cur[p] = [(k//p)*p+i for i in sieve_mod[p]]
					sieve_to[p] = (k//p + 1)*p
					#print("p = ", p, "sieve_dict[p] = ", sieve_dict[p])
					for v in sieve_cur[p]:
						sieve_vals.add(v)
			while k in sieve_vals:
				k += 1
		sieve_vals.difference_update(range(prev_k,k+1))
		num=mul*k-1
		if args.progress:
			eprint(end=LINE_CLEAR)
			eprint(f"k={k} ss={len(sieve_to)} sv={len(sieve_vals)} Checking CC1({num})",end='\r')
		result=cc1(num)
		if len(result.chain)>=n:
			print(f"k = {k}: ", end='')
			print(" ".join(map(str,result.chain))+f" length: {len(result.chain)} ({result.end}="+"*".join(map(str,result.factors))+")", flush=True)
		for p in set(result.chain+result.factors):
			if args.progress:
				eprint(end=LINE_CLEAR)
				eprint(f"k={k} ss={len(sieve_to)} sv={len(sieve_vals)} Adding p={p} to sieve",end='\r')
			# Process each prime
			sieve_to[p] = k
			sieve_mod[p] = k_mod(p,n,mul)
			if ( args.limit_sieve_size and (len(sieve_to)>args.sieve_size_limit) ):
				sieve_mod = dict(init_sieve_mod)
				sieve_to = dict(init_sieve_to)
				eprint();
				eprint("Sieve size limit reached. Resetting sieve to initial values")
		#print("sieve_dict = ", sieve_dict)
		k += 1

if __name__ == "__main__":
	main()
