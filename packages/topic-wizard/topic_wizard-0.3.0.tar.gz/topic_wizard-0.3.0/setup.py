# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topicwizard',
 'topicwizard.blueprints',
 'topicwizard.compatibility',
 'topicwizard.components',
 'topicwizard.components.documents',
 'topicwizard.components.topics',
 'topicwizard.components.words',
 'topicwizard.figures',
 'topicwizard.plots',
 'topicwizard.prepare']

package_data = \
{'': ['*'], 'topicwizard': ['assets/*']}

install_requires = \
['dash-extensions>=0.1.10,<0.2.0',
 'dash-iconify>=0.1.2,<0.2.0',
 'dash-mantine-components>=0.11.1,<0.12.0',
 'dash>=2.7.1,<2.8.0',
 'joblib>=1.2.0,<1.3.0',
 'numpy>=1.22.0',
 'pandas>=1.5.2,<1.6.0',
 'scikit-learn>=1.2.0,<1.3.0',
 'scipy>=1.8.0',
 'umap-learn>=0.5.3',
 'wordcloud>=1.8.2.2,<1.9.0.0']

setup_kwargs = {
    'name': 'topic-wizard',
    'version': '0.3.0',
    'description': 'Pretty and opinionated topic model visualization in Python.',
    'long_description': '<img align="left" width="82" height="82" src="assets/logo.svg">\n\n# topicwizard\n\n<br>\n\nPretty and opinionated topic model visualization in Python.\n\n[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/x-tabdeveloping/topic-wizard/blob/main/examples/basic_usage.ipynb)\n[![PyPI version](https://badge.fury.io/py/topic-wizard.svg)](https://pypi.org/project/topic-wizard/)\n[![pip downloads](https://img.shields.io/pypi/dm/topic-wizard.svg)](https://pypi.org/project/topic-wizard/)\n[![python version](https://img.shields.io/badge/Python-%3E=3.8-blue)](https://github.com/centre-for-humanities-computing/tweetopic)\n[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)\n<br>\n\n\n\nhttps://user-images.githubusercontent.com/13087737/234209888-0d20ede9-2ea1-4d6e-b69b-71b863287cc9.mp4\n\n## New in version 0.3.0 🌟 🌟\n\n - Exclude pages, that are not needed :bird:\n - Self-contained interactive figures :gift:\n - Topic name inference is now default behavior and is done implicitly.\n\n\n## Features\n\n-   Investigate complex relations between topics, words and documents\n-   Highly interactive\n-   Automatically infer topic names\n-   Name topics manually\n-   Pretty :art:\n-   Intuitive :cow:\n-   Clean API :candy:\n-   Sklearn, Gensim and BERTopic compatible :nut_and_bolt:\n-   Easy deployment :earth_africa:\n\n## Installation\n\nInstall from PyPI:\n\n```bash\npip install topic-wizard\n```\n\n## Usage ([documentation](https://x-tabdeveloping.github.io/topic-wizard/))\n\n### Step 1:\n\nTrain a scikit-learn compatible topic model.\n(If you want to use non-scikit-learn topic models, check [compatibility](https://x-tabdeveloping.github.io/topic-wizard/usage.compatibility.html))\n\n```python\nfrom sklearn.decomposition import NMF\nfrom sklearn.feature_extraction.text import CountVectorizer\nfrom sklearn.pipeline import make_pipeline\n\n# Create topic pipeline\ntopic_pipeline = make_pipeline(\n    CountVectorizer(),\n    NMF(n_components=10),\n)\n\n# Then fit it on the given texts\ntopic_pipeline.fit(texts)\n```\n\n### Step 2a:\n\nVisualize with the topicwizard webapp :bulb:\n\n```python\nimport topicwizard\n\ntopicwizard.visualize(pipeline=topic_pipeline, corpus=texts)\n```\n\nFrom version 0.3.0 you can also disable pages you do not wish to display thereby sparing a lot of time for yourself:\n\n```python\nimport topicwizard\n\n# A large corpus takes a looong time to compute 2D projections for so\n# so you can speed up preprocessing by disabling it alltogether.\ntopicwizard.visualize(pipeline=topic_pipeline, corpus=texts, exclude_pages=["documents"])\n```\n\n![topics screenshot](assets/screenshot_topics.png)\n![words screenshot](assets/screenshot_words.png)\n![words screenshot](assets/screenshot_words_zoomed.png)\n![documents screenshot](assets/screenshot_documents.png)\n\nOoooor...\n\n### Step 2b:\n\nProduce high quality self-contained HTML plots and create your own dashboards/reports :strawberry:\n\n### Map of words\n\n```python\nfrom topicwizard.figures import word_map\n\nword_map(corpus=texts, pipeline=pipeline)\n```\n\n![word map screenshot](assets/word_map.png)\n\n### Timelines of topic distributions\n\n```python\nfrom topicwizard.figures import document_topic_timeline\n\ndocument_topic_timeline(\n    "Joe Biden takes over presidential office from Donald Trump.",\n    pipeline=pipeline,\n)\n```\n![document timeline](assets/document_topic_timeline.png)\n\n### Wordclouds of your topics :cloud:\n\n```python\nfrom topicwizard.figures import topic_wordclouds\n\ntopic_wordclouds(corpus=texts, pipeline=pipeline)\n```\n\n![wordclouds](assets/topic_wordclouds.png)\n\n### And much more ([documentation](https://x-tabdeveloping.github.io/topic-wizard/))\n',
    'author': 'Márton Kardos',
    'author_email': 'power.up1163@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
