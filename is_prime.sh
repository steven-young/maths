#!/bin/bash

n="$1"

# Ensure input is a valid integer
if ! [[ "$n" =~ ^[0-9]+$ ]]; then
  echo "Error: Please provide a positive integer."
  exit 2
fi

# Handle edge cases
if (( n < 2 )); then
  echo "$n is not a prime number."
  exit 1
fi

# Check for primality
for ((i = 2; i * i <= n; i++)); do
  if (( n % i == 0 )); then
    echo "$n is not a prime number."
    exit 1
  fi
done

echo "$n is a prime number."
exit 0
