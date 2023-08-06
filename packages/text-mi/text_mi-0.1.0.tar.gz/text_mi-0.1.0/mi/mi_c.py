from multiprocessing.pool import ThreadPool
from functools import partial
from tqdm import tqdm
import os 
from ctypes import *
from typing import Iterable
from pathlib import Path

# find the C library
if os.environ.get('MI_LIB_NAME') is None:
    import importlib.machinery as mch
    for name in mch.EXTENSION_SUFFIXES:
        candidate_file = Path(os.path.dirname(__file__)).parent.absolute() / ("libmi"+name)
        if candidate_file.is_file():
            os.environ["MI_LIB_NAME"] = str(candidate_file)
            break

# If we haven't fint the C library, raise an exception
if not os.environ.get('MI_LIB_NAME'):
    raise FileNotFoundError("DLL not found")

# Connecting to the C library
libname = os.environ.get('MI_LIB_NAME')
mi_lib = CDLL(libname)
mi_lib.mi.restype = c_longdouble


def mi(txts: Iterable[str], tgts: Iterable[str], word: str, tgt: str) -> float:
    """ Wrapper for C calculation function.

    This makes converting variables to C types, calling C function and returning result.

    MI is a non-negative value. It is equal to 0 when random variables are independent.
    Args:
        @txts (Iterable[str]): Iterable of texts.
        @tgts: (Iterable[str]): Iterable of targets corresponding to texts from @txts.
                                All targets corresponding to one text should be separated by "|".
        @word (str): Word for building Mutual Information for.
        @tgt (str): Target for building mutual information for.
    
    Result (float): Mutual Information between @word and @tgt.
    """
    txt_c = (c_char_p * len(txts))()
    tgt_c = (c_char_p * len(tgts))()
    txt_c[:] = [s.encode() for s in txts]
    tgt_c[:] = [s.encode() for s in tgts]

    res = mi_lib.mi(txt_c, len(txts),
                    create_string_buffer(str.encode(tgt)), 
                    tgt_c, create_string_buffer(str.encode(word)))
    return res


def multi_mi(txts: Iterable[str], 
             tgts: Iterable[str], 
             targets: Iterable[str], 
             vocabulary: Iterable[str], 
             workers: int=16) -> dict:
    """Wrapper for C calculation function for multiple words and multiple targets.

    This function converts variables, calculates MI for all word from @vocabulary and all targets 
    from @targets. Result of this function has following strucure: it is dictionary of dictionaries. 
    In the main dictionary keys are words. For every word value is a dictionary with targets, stored as keys. 
    Values of this dictionary is a MI for corresponding word and corresponding target.

    MI is a non-negative value. It is equal to 0 when random variables are independent.
    Args:
        @txts (Iterable[str]): Iterable of texts.
        @tgts (Iterable[str]): Iterable of targets corresponding to texts from @txts.
                                All targets corresponding to one text should be separated by "|".
        @targets (Iterable[str]): Iterable of targets.
        @vocabulary (Iterable[str]): list of words.
        @workers (int, optional): The number of parallel processes. Defaults to 16.
    
    Result: dictionary of dictionaries with MI as values.

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
    """
    vocabulary_dict = dict.fromkeys(set(vocabulary))

    for w in vocabulary_dict.keys():
        vocabulary_dict[w] = dict.fromkeys(targets)

    txt_c = (c_char_p * len(txts))()
    tgt_c = (c_char_p * len(tgts))()
    txt_c[:] = [s.encode() for s in txts]
    tgt_c[:] = [s.encode() for s in tgts]


    def fnc(word, target, txt_c, n, tgt_c, vocabulary_dict):
        res = mi_lib.mi(txt_c, n, create_string_buffer(str.encode(target)), tgt_c, create_string_buffer(str.encode(word)))
        vocabulary_dict[word][target] = res
        
    vocabulary_keys = list(vocabulary_dict.keys())

    for target in tqdm(targets):
        with ThreadPool(processes=workers) as pool:
            pool.map(partial(fnc, target=target, txt_c=txt_c, n=len(txts), 
                            tgt_c=tgt_c, vocabulary_dict=vocabulary_dict), vocabulary_keys)
    
    return vocabulary_dict
