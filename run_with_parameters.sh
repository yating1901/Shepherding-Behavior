

count=0
for N_sheep in $(seq 50 50 100)
do
  for N_shepherd in $(seq 1 1 2)
  do
    for Repetition in $(seq 1 1 2)
    do
      for Iterations in 100000
      do
        nohup python "main.py" $N_sheep $N_shepherd $Repetition $Iterations #>/dev/null 2>&1 &
        echo "N_sheep: $N_sheep";
        echo "N_shepherd: $N_shepherd";
        echo "Repetition: $Repetition";
        echo "Iterations: $Iterations";
        count=$[$count + 1];
      done
    done
  done
done

echo "Number of total runs: $count"