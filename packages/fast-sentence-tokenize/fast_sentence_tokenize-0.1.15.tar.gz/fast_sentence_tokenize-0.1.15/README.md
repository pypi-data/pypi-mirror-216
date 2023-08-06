# Fast Sentence Tokenizer (fast-sentence-tokenize)
Best in class tokenizer

## Usage

### Import
```python
from fast_sentence_tokenize import fast_sentence_tokenize
```

### Call Tokenizer
```python
results = fast_sentence_tokenize("isn't a test great!!?")
```

### Results
```json
[
   "isn't",
   "a",
   "test",
   "great",
   "!",
   "!",
   "?"
]
```
Note that whitespace is not preserved in the output by default.

This generally results in a more accurate parse from downstream components, but may make the reassembly of the original sentence more challenging.

### Preserve Whitespace
```python
results = fast_sentence_tokenize("isn't a test great!!?", eliminate_whitespace=False)
```
### Results
```json
[
   "isn't ",
   "a ",
   "test ",
   "great",
   "!",
   "!",
   "?"
]
```

This option preserves whitespace.

This is useful if you want to re-assemble the tokens using the pre-existing spacing
```python
assert ''.join(tokens) == input_text
```
