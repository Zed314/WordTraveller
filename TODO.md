# TODO
## Tokenization
- [X] Tokenization (use space as delimiter, remove punctuation, use nltk)
- [X] remove tags `<BYLINE>`, ..., `<P>`, `<TYPE>`
- [X] replace <number>,<money> to numbers or currencies
- [ ] add tests for tokenizer (recommanded) (pff…)
- [ ] upgrade tokenizer for "Phillip J. Fry."=>[Phillip, J., Fry]

## Stemming
- [X] Stem words, use Porter's algorithm

## Stop words removal
- [X] remove stop words

## Create Inverted file (IF)
- [X] Formula : ` <ti, ni> --> ..., <dj,score(ti, dj)>,...`
- [X] Build IF in RAM
- [ ] When full, flush the PL and the VOC of this partial IF to the disk
- [ ] Find an efficient datastructure to store the partial IF
- [ ] When all the documents have been seen, merge and flushed PL to obtain the IF


### Score
- [ ] Term frequency tf(t,d) = 1 + log(n) or 0 if n = 0
- [ ] Inverse-document-frequency (view formula)

## Aggregation of the scores of each term
- [ ] sum as an aggregation function
- [ ] consider only conjunctive and/of disjunctive queries

## Ranked queries
- [ ] Queries

## Performance
- [ ] Add a benchmark
- [ ] Add tests to run the benchmark with
- [ ] Add graphical way of visualizing the performances

## Building
- [ ] Find a way to specify all the dependencies required by nltk (tokenization needs a special dataset for instance, that can be grabbed using the method nltk.dowload)

## Interface
- [ ] Use parameters of the program to choose among several ways of running the program (with partial IFs, etc)
- [ ] Write an help section when no argument or badly written argument are used or when the option -h is used

## Code itself
- [ ] Add more structure and comments to the code

## Tests
- [ ] Add regression tests (one or several files) 
