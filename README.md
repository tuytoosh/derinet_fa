
DeriNet is a lexical network which models word-formation relations in the lexicon of Czech. Nodes of the network correspond to Czech lexemes, while edges represent derivational links (relations between derivatives and their base lexemes) or links connecting compounds with their base words.

This is a Python toolbox that implements the training and testing of the approach described in our paper:
#### Building a Morphological Network for Persian on Top of a Morpheme-Segmented Lexicon [View full pdf](https://www.aclweb.org/anthology/W19-8511.pdf)
Hamid Haghdoost, Ebrahim Ansari, Zdeněk Žabokrtský, Mahshid Nikravesh

![A sample tree](./image/tree.jpeg)

#### what is it?
This code implements:
* creating derivational networks
* evaluate trees (networks)
* segments words based on Morfessor

#### Prerequisites
In order to run this toolbox you will need:
- python 3.x (tested with Python 3.7.0 on Ubuntu 18.04.3)
- the provided dataset

#### Usage

run following command to run:

```python main.py $morfData $auto $count $supervised```

example: `python main.py y y 100 y`

help:
  `y` = yes
  `n` = no


if you want to run all of these configuration use `run.sh` bash file as follows:

```
  sudo chmod +x run.sh
  sudo ./run.sh
```
