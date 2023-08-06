from typing import Callable
 
import numpy as np
import pandas as pd
from toolz import compose, curry, juxt

def token2doc_frequencies(
    tokens_dataframe: pd.DataFrame, target: str, tokens: str, doc_id: str
) -> pd.DataFrame:
    """Count token frequency in each docunemt.
 
    Args:
        tokens_dataframe (DataFrame[TokenFrame]): dataframe with list tokens for doc.
        target (str): name of target column.
        tokens (str): name of tokens column.
        doc_id (str): name of item id column.
 
    Returns:
        DataFrame[TokenCountFrame]: dataframe with count token per doc.
    """
    explode_tokens_df = (
        tokens_dataframe[[target, tokens, doc_id]]
        .explode(tokens)
        .reset_index()
        .rename(columns={"index": "item_id", target: "target", tokens: "tokens"})
    )
    return (
        explode_tokens_df.groupby(["target", "item_id", "tokens"])
        .agg(count=(doc_id, "count"))
        .reset_index()
    )

def doc2token_frequencies(
    tokens_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Count doc frequency for each token.
 
    N1 - means number of documents which have word W.
    This docs can be in different themes.
 
    Args:
        tokens_dataframe (DataFrame[TokenCountFrame]): dataframe with docs tokens count.
 
    Returns:
        DataFrame[DocsTokenCountFrame]: dataframe with count docs per tokens.
    """
    return tokens_dataframe.groupby(["tokens"], as_index=False).agg(
        N1=("item_id", "count")
    )

def token2target_frequencies(
    tokens_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Count token frequency in each target.
 
    N11 - means number of documents which have word W and theme T.
 
    Args:
        tokens_dataframe (DataFrame[TokenCountFrame]): dataframe with docs tokens count.
 
    Returns:
        DataFrame[TokenTargetCountFrame]: dataframe with count token per target.
    """
    return tokens_dataframe.groupby(["target", "tokens"], as_index=False).agg(
        N11=("item_id", "count")
    )

def token2target_frequencies(
    tokens_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Count token frequency in each target.
 
    N11 - means number of documents which have word W and theme T.
 
    Args:
        tokens_dataframe (DataFrame[TokenCountFrame]): dataframe with docs tokens count.
 
    Returns:
        DataFrame[TokenTargetCountFrame]: dataframe with count token per target.
    """
    return tokens_dataframe.groupby(["target", "tokens"], as_index=False).agg(
        N11=("item_id", "count")
    )

def doc2target_frequencies(
    tokens_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Count docs frequency in each target.
 
    NT - means number of documents which have theme T.
 
    Args:
        tokens_dataframe (DataFrame[TokenCountFrame]): dataframe with docs tokens count.
 
    Returns:
        DataFrame[DocsTokenCountFrame]: dataframe with count docs per target.
    """
    return (
        tokens_dataframe.drop_duplicates(["target", "item_id"])
        .groupby(["target"], as_index=False)
        .agg(NT=("item_id", "count"))
    )



def count_frequency_statisitcs(
    tokens_dataframe: pd.DataFrame, docs_number: int
) -> pd.DataFrame:
    """Count frequency stats for tokens, themes and docs.
 
    N11 - number of documents which have word W and theme T.
    N10 - number of documents which have word W and haven't theme T.
    N1 - number of documents which have word W and from different themes.
    N1 = N11 + N10
    N01 - number of documents which haven't word W and have theme T.
    N00 - number of documents which haven't word W and theme T.
    N0 - number of documents which haven't word W and from different themes.
    N0 = N01 + N00
    NT - number of documents which have theme T.
    NT = N11 + N10
    N - number of all docs in dataset.
    N = N0 + N1
 
    Args:
        tokens_dataframe (DataFrame[TokenCountFrame]):
                dataframe with count token per doc.
        docs_number (int): number of all documents in dataset.
 
    Returns:
        DataFrame[TokenStatsFrame]: simple tokens stats.
    """
    token_arget, target, token = juxt(
        token2target_frequencies,
        doc2target_frequencies,
        doc2token_frequencies,
    )(tokens_dataframe)
    token_frequencies = (
        token_arget.merge(target, on="target")
        .merge(token, on="tokens")
        .assign(N=docs_number)
    )
    return token_frequencies.assign(
        N10=token_frequencies.eval("N1-N11"),
        N01=token_frequencies.eval("NT-N11"),
        N00=token_frequencies.eval("N-N1-NT+N11"),
        N0=token_frequencies.eval("N-N1"),
    )
 

def compute_mutual_information(
    stats_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Compute mutual information base on simple statistics.
 
    Used formula:
 
    .. math::
        I(U,C) = N11 / N * log2(N11 * N / ((N10 + N11) * (N11 + N01))) +
                N01 / N * log2(N01 * N / ((N00 + N01) * (N11 + N01))) +
                N10 / N * log2(N10 * N / ((N10 + N11) * (N10 + N00))) +
                N00 / N * log2(N00 * N / ((N00 + N01) * (N10 + N00)))
 
    From Manning K.D., Raghavan P., Sch tze H. Introduction to information search.
 
    Mutual information measures the amount of information about belonging to a class T
    that carries the presence or absence of a word W.
 
    Args:
        stats_dataframe (DataFrame): simple stats frame.
 
    Returns:
        DataFrame: simple tokens stats.
    """
    return stats_dataframe.assign(
        mutual_information=stats_dataframe.assign(
            log_11=np.log2(stats_dataframe.eval("N11*N/((N10+N11)*(N11+N01))")),
            log_01=np.log2(stats_dataframe.eval("N01*N/((N00+N01)*(N11+N01))")),
            log_10=np.log2(stats_dataframe.eval("N10*N/((N10+N11)*(N10+N00))")),
            log_00=np.log2(stats_dataframe.eval("N00*N/((N00+N01)*(N10+N00))")),
        )
        .eval("N11/N*log_11+N01/N*log_01+N10/N*log_10+N00/N*log_00")
        .fillna(0)
    )
 

def mutual_info_pipeline(
    target: str, tokens: str, doc_id: str, docs_number: int
) -> Callable[[pd.DataFrame], pd.DataFrame]:
    """Pipeline for MI computation.
 
    Args:
        target (str): target columne name.
        tokens (str): tokens column name.
        doc_id (str): item id column name.
        docs_number (int): number of docs.
 
    Returns:
        Callable[[DataFrame[TokenFrame]], DataFrame[TokensMIFrame]]: compute pipeline.
    """
    return compose(
        compute_mutual_information,
        curry(count_frequency_statisitcs, docs_number=docs_number),
        curry(token2doc_frequencies, target=target, tokens=tokens, doc_id=doc_id),
    )
 

