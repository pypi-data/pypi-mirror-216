# Description
C library for python with custom mutual information calculations. Originally was part of https://github.com/volkoshkursk/NB.

There are two approach to calculate the MI: based on the Pandas framework and based on the custom C library. Pandas-based approach is faster, however you need to construct a DataFrame with columns ``` doc_id target token ``` where `token` is the column with only one token in the row. If you have a much data it can be memory-expensive operation. 

From the other hand, the custom library - based approach does not need in some special dataframe. It needs only two iterables with same lengthes: the targets and the textes. However, it is slower than the pandas-based approach.

# Requirements
If you want to build by `make` you need to have `make` and `python-dev` packages installed.
It is recommended to have a poetry library.
# Installation

There is several different ways to install this library:

## Installation with poetry.
This is a simpliest and recommended way to install the library.
Just run 
```
poetry install
``` 
åto install the library. Then you can run your code in poetry's virtual environment with 
```
poetry run script.py
```

where `script.py` is your script.

## Building from sources.
This way is useful if you don't have a poetry by some reason. However, it is strongly recommended to use the poetry installation.

You need create libmi.so to run this project.
For this purpose you need installed python3-dev on your system. For building on library *nix system run

```
make clean && make
```

Default Python version is 3.8. If you need build for another version run 

```
make clean && make VER=<ver>
```

where instead `<ver>` should be your version.

Also, you need to install Python dependencies with 
```
pip install -r requirements.txt
```

# Theory

MI is a non-negative value. It is equal to 0 when random variables are independent.

 The main formula, using for calculating MI was found in book Manning K.D., Raghavan P., Schütze H. Introduction to information search. 

$$
\begin{align}
I(U,C) = {N_{11} \over N}  \log_2\bigl({N_{11}N \over{(N_{10} + N_{11}) (N_{11} + N_{01})}}\bigr) + \\
{N_{01} \over N} \log_2({{N_{01} N} \over {(N_{00} + N_{01}) (N_{11} + N_{01})}}) + \\
{N_{10} \over N} \log_2({{N_{10} N} \over {(N_{10} + N_{11}) (N_{10} + N_{00})}}) + \\
{N_{00} \over N} \log_2({{N_{00} N} \over {(N_{00} + N_{01}) (N_{10} + N_{00})}}),
\end{align}
$$

where 
- $U$ is the random variable, shows presence of the word W.
- $C$ is the random variable, shows presence of the theme T.
- $N$ is the number of all docs in dataset,
- $N_{11}$ is the number of documents which have word W and theme T,
- $N_{10}$ is the number of documents which have word W and haven't theme T,
- $N_{01}$ is the number of documents which haven't word W and have theme T,
- $N_{00}$ is the number of documents which haven't word W and theme T.    

As we can see, the formula above can be calculated only if $N_{11}N_{00}N_{01}N_{11} > 0$. When we have lots of themes and less of documents this becomes a problem: for large number of word we can not calculate MI. 

This problem can be solved by going to the limit in each summand in formaula above. However, the result will be different with precise formula even if the formula can be calculated.

# Differences between approaches

As it was told upper, there is two approaches to mutual information calculation. [First of them](#c-based-approach) is based on custom C extension. It is slower than another one, but require less memory for running. [Second of them](#pandas-based-approach) based on Pandas framework. It is faster than the C-based approach, but requires a lot of memory. 

The another difference between the approaches is in handling division-by-zero exception.

In Pandas-based approach if $N_{11}N_{00}N_{01}N_{11} = 0$ the result is equal to $0$. In C-extension based approach if $N_{11}N_{00}N_{01} = 0$ the result is calulated as a sum of the summand, where logarithm can be calculated.

# Using
## C-based approach
There are two function you can use: `mi` and `multi_mi`. The first one calculate MI for one word and one theme. The second one uses `mi` for build a dictionary for all words and all themes.

### `mi`

__Args:__
- ___txts___ (_Iterable[str]_): Iterable of texts.
- ___tgts___ (_Iterable[str]_): Iterable of targets corresponding to texts from ___txts___. All targets corresponding to one text should be separated by "|".
- ___word___ (_str_): Word for building Mutual Information for.
- ___tgt___ (_str_): Target for building mutual information for.

__Result__ (_float_): Mutual Information between ___word___ and ___tgt___.

### `multi_mi`

__Args:__
- ___txts___ (_Iterable[str]_): Iterable of texts.
- ___tgts___ (_Iterable[str]_): Iterable of targets corresponding to texts from ___txts___. All targets corresponding to one text should be separated by "|".
- ___targets____ (_Iterable[str]_): Iterable of targets.
- ___vocabulary___ (_Iterable[str]_): list of words.
- ___workers___ (_int_, optional): The number of parallel processes. Defaults to 16.

__Result__ (_dict[dict[float]]_): dictionary of dictionaries with MI as values.

Example of result:

    {
        'quick': {
                    'target_1': 0.1,
                    'target_2': 0.2,
                    'target_3': 0.3
                 },
        'brown': {
                    'target_1': 0.1,
                    'target_2': 0.2,
                    'target_3': 0.3
                 },
        'fox': {
                    'target_1': 0.1,
                    'target_2': 0.2,
                    'target_3': 0.3
                 },
        'jumps': {
                    'target_1': 0.1,
                    'target_2': 0.2,
                    'target_3': 0.3
                 },
        'over': {
                    'target_1': 0.1,
                    'target_2': 0.2,
                    'target_3': 0.3
                 },
        'the': {
                    'target_1': 0.1,
                    'target_2': 0.2,
                    'target_3': 0.3
                 },
        'lazy': {
                    'target_1': 0.1,
                    'target_2': 0.2,
                    'target_3': 0.3
                 },
        'dog': {
                    'target_1': 0.1,
                    'target_2': 0.2,
                    'target_3': 0.3
                 },
    }

## Pandas-based approach

For using Pandas-based approach you should call the function `mutual_info_pipeline`, which generate a function in which you should send a Pandas.Dataframe, which has follow structure: it has some item identifyer (for example id of document), word and target. This DataFrame can content some other column, but this three is necessary.

The result will contain follow columns: 
- *target* - name of target,
- *tokens* - the word,
- *N11* - the number of documents which have both the word and the theme,
- *NT* - the number of documents which have the theme,
- *N1* - the number of documents which have the word,
- *N* - the number of all docs in dataset, which haven't the theme,
- *N10* - the number of documents which have the word and haven't the theme,
- *N01* - the number of documents which haven't the word and have the theme,
- *N00* - the number of documents which haven't both the word and the theme,
- *N0*  - the number of documents which haven't the word,
- *mutual_information* - MI for the word and the theme.

### `mutual_info_pipeline`
__Args:__
- ___target___ (_str_): target columne name.
- ___tokens___ (_str_): tokens column name.
- ___doc_id___ (_str_): item id column name.
- ___docs_number___ (_int_): number of docs.

__Result__ (_Callable[[DataFrame[TokenFrame]], DataFrame[TokensMIFrame]]_): compute pipeline.

Example of using:

```
from mi import mutual_info_pipeline

mutual_info_pipeline(
    'target',
    'word',
    'item_id',
    docs_number,
)(df)
```