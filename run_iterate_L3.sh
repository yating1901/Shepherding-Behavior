count=0
TICK=10000
for N_sheep in $(seq 100 100 500)
do
  for N_shepherd in $(seq 1 1 5)
  do
    for Repetition in $(seq 1 1 10)
    do
      for Iterations in 160000
      do
        for L3 in $(seq 0 5 25)
        do
          nohup python "main_interface.py" $N_sheep $N_shepherd $Repetition $Iterations $TICK $L3 >/dev/null 2>&1 &
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
done

echo "Number of total runs: $count"
