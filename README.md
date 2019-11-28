
DeriNet is a lexical network which models word-formation relations in the lexicon of Czech. Nodes of the network correspond to Czech lexemes, while edges represent derivational links (relations between derivatives and their base lexemes) or links connecting compounds with their base words.

This is a Python toolbox that implements the training and testing of the approach described in our paper:
#### Building a Morphological Network for Persian on Top of a Morpheme-Segmented Lexicon [View PDF](https://www.aclweb.org/anthology/W19-8511.pdf)
Hamid Haghdoost, Ebrahim Ansari, Zdeněk Žabokrtský, Mahshid Nikravesh

![A sample tree](https://github.com/tuytoosh/derinet_fa/blob/master/images/tree.jpeg)

#### What is it?
This code implements:
* creating derivational networks
* evaluate trees (network)
* segments words based on Morfessor

#### Prerequisites
In order to run this toolbox you will need:
* python 3.x (tested with Python 3.7.0 on Ubuntu 18.04.3)
* the provided dataset

### Input data format
In `providers/data.py` we have two property for input data. ‍‍`ourDataRoute` is a data that created by unsupervised Morfessor and `ourDataRoute` created by us. if you want to use your own data, modify the coressponding dataset route and formatted as follows.

```
play
play er
play er s
```

#### Usage

Run the following command to execution. you can find more information about parameters in detail of paper.

```python main.py $morfData $auto $count $supervised```

Example: `python main.py y y 100 y`

notice:
  `y` represents `yes` for that parameter and `n` stands for `no`


if you want to run all of these configuration together use `run.sh` bash file as follows on Linux OS:

```
  sudo chmod +x run.sh
  sudo ./run.sh
```

In other operating systems you need to write your own alternatives, for example `.bat` file in windows.

finally if you have any problem with running the code, feel free to open an issue.
