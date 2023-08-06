from typing import Any, List

import dash_mantine_components as dmc
import numpy as np
from dash_extensions.enrich import DashBlueprint, dcc, html
from plotly import colors


def create_blueprint(
    vocab: np.ndarray,
    document_term_matrix: np.ndarray,
    document_topic_matrix: np.ndarray,
    topic_term_matrix: np.ndarray,
    corpus: List[str],
    vectorizer: Any,
    topic_model: Any,
    groups: List[str],
    **kwargs,
) -> DashBlueprint:
    # --------[ Preparing data ]--------

    # --------[ Collecting blueprints ]--------
    blueprints = [
        document_map,
        document_selector,
        document_wordcloud,
        document_pie,
        timeline,
        window_slider,
    ]

    # --------[ Creating app blueprint ]--------
    app_blueprint = DashBlueprint()
    app_blueprint.layout = html.Div(
        [],
        className="""
        hidden
        """,
        id="groups_container",
    )

    # --------[ Registering callbacks ]--------
    for blueprint in blueprints:
        blueprint.register_callbacks(app_blueprint)
    return app_blueprint
