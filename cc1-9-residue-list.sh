echo "10 or less:"
for i in 7 17 31 73 127
do
  echo -n  "$i -> "
  ./times-two-mod.py -c 2 $i
done

echo "2 isn't primitive root"
for i in 23 89 43 151 41 47 113 71 109 79 97 103 157 137 167 191 193 199
do
  echo -n "$i -> "
  ./times-two-mod.py -c 2 $i |rev | cut -d ' ' -f 1-10 | rev
done

echo "2 is primitive root"
for i in 11 13 19 29 37 53 59 61 67 83 101 107 131 139 163 173 179 181 197
do
  echo -n "$i -> "
  ./times-two-mod.py 2 $i | rev | cut -d ' ' -f 1-10 | rev
done
