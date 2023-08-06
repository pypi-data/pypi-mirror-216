"""Utilities for preparing data for visualization."""
from typing import Tuple

import numpy as np
import pandas as pd
import scipy.sparse as spr
import umap


def group_positions(
    group_topic_importances: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates group positions from group-topic matrices.

    Parameters
    ----------
    group_topic_importances: array of shape (n_groups, n_topics)
        Group-topic matrix.

    Returns
    -------
    x: array of shape (n_groups)
    y: array of shape (n_groups)
    """
    # Calculating distances
    n_topics = group_topic_importances.shape[0]
    # Setting perplexity to 30, or the number of topics minus one
    perplexity = np.min((30, n_topics - 1))
    if n_topics <= 3:
        init = "random"
    else:
        init = "spectral"
    manifold = umap.UMAP(
        n_components=2, n_neighbors=perplexity, metric="cosine", init=init
    )
    x, y = manifold.fit_transform(group_topic_importances).T
    return x, y


def group_importances(
    document_topic_matrix: np.ndarray,
    document_term_matrix: np.ndarray,
    group_labels: np.ndarray,
    n_groups: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates empirical group importances, term importances, group-term importances
    and group-topic importances.

    Parameters
    ----------

    Returns
    -------
    group_importances: array of shape (n_groups, )
    term_importances: array of shape (n_terms, )
    group_term_importance: array of shape (n_groups, n_terms)
    group_topic_importances: array of shape (n_groups, n_topics)
    """
    n_terms = document_term_matrix.shape[1]
    group_importances = np.zeros(n_groups)
    for i_group in range(n_groups):
        group_importances[i_group] = np.sum(group_labels == i_group)
    group_term_importances = spr.lil_array((n_groups, n_terms))
    for i_group in range(n_groups):
        group_term_importances[i_group, :] = document_term_matrix[
            group_labels == i_group
        ].sum(axis=0)
    # TODO
    pass


# TODO rest of the  file


def word_relevance(
    topic_id: int,
    term_frequency: np.ndarray,
    topic_term_frequency: np.ndarray,
    alpha: float,
) -> np.ndarray:
    """Returns relevance scores for each topic for each word.

    Parameters
    ----------
    components: ndarray of shape (n_topics, n_vocab)
        Topic word probability matrix.
    alpha: float
        Weight parameter.

    Returns
    -------
    ndarray of shape (n_topics, n_vocab)
        Topic word relevance matrix.
    """
    probability = np.log(topic_term_frequency[topic_id])
    probability[probability == -np.inf] = np.nan
    lift = np.log(topic_term_frequency[topic_id] / term_frequency)
    lift[lift == -np.inf] = np.nan
    relevance = alpha * probability + (1 - alpha) * lift
    return relevance


def calculate_top_words(
    topic_id: int,
    top_n: int,
    alpha: float,
    term_frequency: np.ndarray,
    topic_term_frequency: np.ndarray,
    vocab: np.ndarray,
) -> pd.DataFrame:
    """Arranges top N words by relevance for the given topic into a DataFrame."""
    vocab = np.array(vocab)
    term_frequency = np.array(term_frequency)
    topic_term_frequency = np.array(topic_term_frequency)
    relevance = word_relevance(
        topic_id, term_frequency, topic_term_frequency, alpha=alpha
    )
    highest = np.argpartition(-relevance, top_n)[:top_n]
    res = pd.DataFrame(
        {
            "word": vocab[highest],
            "importance": topic_term_frequency[topic_id, highest],
            "overall_importance": term_frequency[highest],
            "relevance": relevance[highest],
        }
    )
    return res
