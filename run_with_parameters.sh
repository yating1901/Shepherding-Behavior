
count=0
TICK=10000
for N_sheep in $(seq 100 50 300)
do
  for N_shepherd in $(seq 1 1 4)
  do
    for Repetition in $(seq 1 1 5)
    do
      for Iterations in 200000
      do
        nohup python "main.py" $N_sheep $N_shepherd $Repetition $Iterations $TICK  >/dev/null 2>&1 &
        echo "N_sheep: $N_sheep";
        echo "N_shepherd: $N_shepherd";
        echo "Repetition: $Repetition";
        echo "Iterations: $Iterations";
        echo "TICK: $TICK";
        count=$((count + 1));
      done
    done
  done
done

echo "Number of total runs: $count"