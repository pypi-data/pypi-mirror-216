# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_sentence_tokenize',
 'fast_sentence_tokenize.bp',
 'fast_sentence_tokenize.dmo',
 'fast_sentence_tokenize.dto',
 'fast_sentence_tokenize.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'nltk', 'spacy>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'fast-sentence-tokenize',
    'version': '0.1.15',
    'description': 'Fast and Efficient Sentence Tokenization',
    'long_description': '# Fast Sentence Tokenizer (fast-sentence-tokenize)\nBest in class tokenizer\n\n## Usage\n\n### Import\n```python\nfrom fast_sentence_tokenize import fast_sentence_tokenize\n```\n\n### Call Tokenizer\n```python\nresults = fast_sentence_tokenize("isn\'t a test great!!?")\n```\n\n### Results\n```json\n[\n   "isn\'t",\n   "a",\n   "test",\n   "great",\n   "!",\n   "!",\n   "?"\n]\n```\nNote that whitespace is not preserved in the output by default.\n\nThis generally results in a more accurate parse from downstream components, but may make the reassembly of the original sentence more challenging.\n\n### Preserve Whitespace\n```python\nresults = fast_sentence_tokenize("isn\'t a test great!!?", eliminate_whitespace=False)\n```\n### Results\n```json\n[\n   "isn\'t ",\n   "a ",\n   "test ",\n   "great",\n   "!",\n   "!",\n   "?"\n]\n```\n\nThis option preserves whitespace.\n\nThis is useful if you want to re-assemble the tokens using the pre-existing spacing\n```python\nassert \'\'.join(tokens) == input_text\n```\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/fast-sentence-tokenize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
