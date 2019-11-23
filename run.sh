for morfData in y n; do
  for auto in y n; do
    for count in 100; do
      for supervised in y n; do
        python main.py $morfData $auto $count $supervised
      done;
    done;
  done;
done;
