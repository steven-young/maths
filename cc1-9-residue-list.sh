echo -n "11 -> "
./times-two-mod.py -c 2 11

echo "10 or less:"
for i in 17 31 73 127
do
  echo -n  "$i -> "
  ./times-two-mod.py -c 2 $i
done

echo "2 isn't primitive root"
for i in 23 43 71 89
do
  echo -n "$i -> "
  ./times-two-mod.py -c 2 $i | rev | cut -d ' ' -f 1-10 | rev
done

echo "2 is primitive root"
for i in 13 19 29 37 41 53 59 61 67 71
do
  echo -n "$i -> "
  ./times-two-mod.py 2 $i | rev | cut -d ' ' -f 1-10 | rev
done
