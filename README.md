# WordTraveller
Place the latimes' folder at the `data` folder of the project

It requires the punkt corpus.

The project is built and tested on Python 3.6

## Dataset
[Page web de Portier](http://p6e7p7.freeshell.org/teaching_2018_2019/)

## Installing dependencies:
- `pip3 install -r requirements.txt`

## Executing
- `python3 -m wordtraveller.analysis`
- `python3 -m wordtraveller.filemanager`
- `python3 -m wordtraveller.query`

## Executing tests
- `python3 -m tests.test[number] -v` (-v parameter for higher verbosity)
- `python3 -m unittest -v` (to execute all tests)

