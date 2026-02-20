echo -n "($1+$2*$3)*30-1="
echo "($1+$2*$3)*30-1" | bc
for i in 7 11
do
  echo -n "($1+$2*$3)*30%$i="
  echo "($1+$2*$3)*30%$i" | bc
done

for i in 17 31 73 127
do
  echo -n "($1+$2*$3)*30%$i="
  val=`echo "($1+$2*$3)*30%$i" | bc`
  echo -n "$val "
  ./times-two-mod.py -c 2 $i | grep " $val "
  echo
done

for i in 23 43 47 71 89
do
  echo -n "($1+$2*$3)*30%$i="
  val=`echo "($1+$2*$3)*30%$i" | bc`
  echo -n "$val "
  ./times-two-mod.py -c 2 $i | rev | cut -d ' ' -f 1-$4 | rev | grep " $val "
  echo
done

for i in `cat primes-987.list`
do
  echo -n "($1+$2*$3)*30%$i="
  val=`echo "($1+$2*$3)*30%$i" | bc`
  echo -n "$val "
  ./times-two-mod.py 2 $i | rev | cut -d ' ' -f 1-$4 | rev | grep " $val "
  echo
done

