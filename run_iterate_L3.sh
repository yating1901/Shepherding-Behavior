count=0
Repetition=3
for N_sheep in $(seq 100 100 300)
do
  for N_shepherd in $(seq 1 1 2)
  do
    for Iterations in 10000
    do
      for L3 in 0
      do
        nohup python "main_interface_metric.py" $N_sheep $N_shepherd $Iterations $L3 $Repetition >/dev/null 2>&1 &
        echo "N_sheep: $N_sheep";
        echo "N_shepherd: $N_shepherd";
        echo "Repetition: $Repetition";
        echo "Iterations: $Iterations";
        echo "TICK: $TICK";
        echo "L3: $L3";
        count=$((count + 1));
      done
    done
  done
done

echo "Number of total runs: $count"
