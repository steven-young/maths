#!/usr/bin/env python3
import argparse
import math
import subprocess
import os
import sys
import signal
from primefac import isprime,primefac 
from bisect import bisect,insort
import bitstring

LINE_CLEAR = '\x1b[2K'

k=1

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def signal_handler(sig, fram):
	global k
	print()
	print(f"k={k}")
	sys.exit(0)

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
	parser.add_argument("-e","--end_k", type=int,default=0,help="End k value")
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
		exit(1)
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
		print(f"multiplier = {mul}", flush=True)
	else:
		print(f"Chain length currently limited to {max(primitive_root_primes)}")
		exit(1)

	# Establish initial sieve considering primes with order of 2 mod p less than or equal to m
	init_sieve_mod = {}
	init_sieve_to = []
	sieve_mod = {}
	sieve_to = []
	order_2_mod_p=((),(),(),(7,),(),(31,),(),(127,),(17,),(73,),(),(23,89),(),(8191,),(43,),(151,),(257,),(131071,),(),(524287,),(41,),(337,),(683,),(47,178481),(241,),(601,1801),(2731,),(262657,),(113,),(233,1103,2089),(331,),(2147483647,),(65537,),(599479,),(43691,),(71,122921),(109,))
	for i in range(3,m):
		for p in order_2_mod_p[i]:
			# Construct a set of values mod p where k*mul*2^j-1 for j in range(i)
			if args.progress:
				eprint(end=LINE_CLEAR,flush=True)
				eprint(f"k=0 ss={len(init_sieve_mod)} Adding p={p} to sieve",end='\r',flush=True)
			init_sieve_mod[p] = k_mod(p,i,mul)
			#init_sieve_to[p] = 0
			insort(init_sieve_to, (0,p))
			#print("sieve_dict = ", sieve_dict)

	# Start searching
	k=args.start_k
	end_k = args.end_k
	sieve_vals = []
	sieve_mod = dict(init_sieve_mod)
	sieve_to = list(init_sieve_to)
	cur_st_idx = 0
	cc1count = 0
	bs_size = 100000000
	bs_vals = bitstring.BitArray(bs_size)
	while not (end_k != 0 and k > end_k):
		# Skip k values depending on sieve_list
		prev_k=k
#		while any(s<=k for s in iter(sieve_to.values())):
#			for p in sieve_to:
		bs_start = k
		bs_end = k + bs_size
		bs_vals.set(0)
		while True:
			# Set bits from sieve_vals less than bs_end
			if len(sieve_vals) > 0:
				idx = bisect(sieve_vals, bs_end)
				bs_vals.set(1, [x - bs_start for x in sieve_vals[0:idx]])
				del sieve_vals[:idx]
			# Process the sieve_to values
			while sieve_to[cur_st_idx][0] <= k:
				p = sieve_to[cur_st_idx][1]
				if args.progress:
					eprint(end=LINE_CLEAR)
					eprint(f"k={k} ss={len(sieve_mod)} sv={len(sieve_vals)} cc1={cc1count} Updating sieve values for p={p}",end='\r')
				b=(k//p)*p
				for v in [b+i for i in sieve_mod[p]]:
					if v < k:
						v += p
					if v < bs_end:
						bs_vals.set(1, range(v-k, bs_size, p))
					else:
						if len(sieve_vals) == 0:
							sieve_vals.append(v)
						else:
							idx = bisect(sieve_vals, v)
							if sieve_vals[idx-1] != v:
								sieve_vals.insert(idx,v)
				#sieve_to[p] = (k//p + 1)*p
				insort(sieve_to, (bs_end,p), lo=cur_st_idx)
				cur_st_idx = cur_st_idx +1
				#print("p = ", p, "sieve_dict[p] = ", sieve_dict[p])
				idx = 0
				if len(sieve_vals) != 0:
					while sieve_vals[idx]==k:
						idx += 1
						k += 1
						if idx==len(sieve_vals):
							break
					del sieve_vals[:idx]
			del sieve_to[:cur_st_idx]
#			if args.progress:
#				eprint(end='\n')
			cur_st_idx=0
			if bs_vals.any(0):
				break
		# Step through bs_vals bitstring sieve vals
		# Find next value of k in bs_vals
		while k < bs_end:
			if bs_vals.all(1, range(k - bs_start, bs_size)):
				k = bs_end
				break;
			k = bs_vals.find('0b0', k - bs_start)[0] + bs_start
			num=mul*k-1
			result=cc1(num)
			cc1count += 1
			if args.progress:
				eprint(end=LINE_CLEAR)
				eprint(f"k={k} ss={len(sieve_mod)} sv={len(sieve_vals)} cc1={cc1count} Checking CC1({num})",end='\r')
			if len(result.chain)>=n:
				print(f"k = {k}: ", end='')
				print(" ".join(map(str,result.chain))+f" length: {len(result.chain)} ({result.end}="+"*".join(map(str,result.factors))+")", flush=True)
			for p in set(result.chain+result.factors):
				if p > 1000000:
					continue
				if args.progress:
					eprint(end=LINE_CLEAR)
					eprint(f"k={k} ss={len(sieve_mod)} sv={len(sieve_vals)} cc1={cc1count} Adding p={p} to sieve",end='\r')
				# Process each prime
				#sieve_to[p] = k
				sieve_mod[p] = k_mod(p,n,mul)
				# Update bs_vals with these mod values
				b = (k//p)*p
				for v in [ b+i for i in sieve_mod[p] ]:
					if v < k:
						v += p
					if v < bs_end:
						bs_vals.set(1, range(v - bs_start, bs_size, p))
					if v > bs_end and p > bs_size:
						if len(sieve_vals) == 0:
							sieve_vals.append(v)
						else:
							idx = bisect(sieve_vals, v)
							if sieve_vals[idx-1] != v:
								sieve_vals.insert(idx,v)
				if p < bs_size:
					insort(sieve_to, (bs_end, p), lo=cur_st_idx)
				else:
					insort(sieve_to, ((k//p +1)*p, p), lo=cur_st_idx)
			if ( args.limit_sieve_size and (len(sieve_to)>args.sieve_size_limit) ):
				sieve_mod = dict(init_sieve_mod)
				sieve_to = list(init_sieve_to)
				eprint();
				eprint("Sieve size limit reached. Resetting sieve to initial values")
			k += 1
	print(f"k={k} ss={len(sieve_mod)} sv={len(sieve_vals)}")

if __name__ == "__main__":
	main()
