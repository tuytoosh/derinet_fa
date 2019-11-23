
DeriNet is a lexical network which models word-formation relations in the lexicon of Czech. Nodes of the network correspond to Czech lexemes, while edges represent derivational links (relations between derivatives and their base lexemes) or links connecting compounds with their base words.

In this repository the developing proceedure of derinet_fa (Persian version of Derinet) is programmed.

run following command to run:

```python main.py $morfData $auto $count $supervised```

ex: python main.py y y 100 y

help:
  y = yes
  n = no


if you want to run all of these configuration use `run.sh` bash file as follows:

```
  sudo chmod +x run.sh
  sudo ./run.sh
```
