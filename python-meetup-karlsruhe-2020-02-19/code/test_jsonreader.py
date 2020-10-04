import pytest

import json
from jsonreader import jsonreader

def test_jsonreader():
    doc_a = {"id": 0, "name": "whatev"}
    doc_b = {"id": 1, "name": "what else"}
    input_ = [json.dumps(doc_a), json.dumps(doc_b)]
    reader = jsonreader(input_)
    assert next(reader) == doc_a
    assert next(reader) == doc_b
    with pytest.raises(StopIteration):
        next(reader)
