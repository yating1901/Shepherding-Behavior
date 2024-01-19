count=0
TICK=10000
for N_sheep in $(seq 400 100 400)
do
  for N_shepherd in $(seq 3 1 5)
  do
    for Repetition in 5
    do
      for Iterations in 150000
      do
        for L3 in $(seq 5 5 10)
        do
          nohup python "main_interface.py" $N_sheep $N_shepherd $Repetition $Iterations $TICK $L3 #>/dev/null 2>&1 &
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
