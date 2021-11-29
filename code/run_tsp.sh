seed=0
time=$time
city=$city
method=$method
echo $time
# shellcheck disable=SC2004
while(($seed < 50))
do
  python3 tsp_main.py -inst $city -alg $method -time $time -seed $seed
  # shellcheck disable=SC2219
  let "seed++"
done


