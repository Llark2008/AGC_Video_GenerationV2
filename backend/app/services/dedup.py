import itertools
from collections import Counter
from typing import List
from difflib import SequenceMatcher
from ..config import get_settings

settings = get_settings()


def _ngram(s: str, n: int = 4) -> set[str]:
    tokens = s.lower().split()
    return {" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def similarity(a: str, b: str) -> float:
    """综合 n‑gram + Levenshtein（SequenceMatcher）相似度"""
    grams_a, grams_b = _ngram(a), _ngram(b)
    if not grams_a or not grams_b:
        return 0.0
    jaccard = len(grams_a & grams_b) / len(grams_a | grams_b)
    seq = SequenceMatcher(None, a, b).ratio()
    return (jaccard + seq) / 2


def deduplicate(prompts: List[str]) -> List[str]:
    unique: list[str] = []
    for p in prompts:
        if all(similarity(p, q) < settings.dedup_threshold for q in unique):
            unique.append(p)
    return unique
