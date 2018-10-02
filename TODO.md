# TODO
## Tokenization
- [ ] Tokenization (use space as delimiter, remove punctuation, use nltk)
- [ ] remove tags `<BYLINE>`, ..., `<P>`, `<TYPE>`
- [ ] replace <number>,<money> to numbers or currencies

## Stemming
- [ ] Stem words, use Porter's algorithm

## Stop words removal
- [ ] remove stop words

## Create Inverted file (IF)
- Formula : ` <ti, ni> --> ..., <dj,score(ti, dj)>,...`
- [ ] Build IF in RAM
- [ ] When full, flush the PL and the VOC of this partial IF to the disk
- [ ] when all the documents have been seen, merge and flushed PL to obtain the IF


### Score
- [ ] Term frequency tf(t,d) = 1 + log(n) or 0 if n = 0
- [ ] Inverse-document-frequency (view formula)

## Aggregation of the scores of each term
- [ ] sum as an aggregation function
- [ ] consider only conjunctive and/of disjunctive queries

## Ranked queries
- [ ] Queries
