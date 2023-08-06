# FastAPI Pagination Utilities

This Python package contains utilities to aid in paginating responses from
FastAPI applications.

## Use

Install `fastapi-pagination-utilities` using pip:

```
pip install fastapi-pagination-utilities
```

The module can then be used as `fastapi_pagination`:

```python3
from fastapi import FastAPI
from fastapi_pagination import (
    CURSOR_QUERY, PAGE_SIZE_QUERY, PaginationDetails, PaginatedResults
)
from pydantic import BaseModel

app = FastAPI()

class Widget(BaseModel):
    name: str

@app.get(
    '/widgets',
    summary="List widgets",
    description="List all the widgers which are available."
    response_model=PaginatedResults[Widget]
)
def list_widgets(
        request: Request,
        cursor: Optional[str] = CURSOR_QUERY,
        page_size: Optional[int] = PAGE_SIZE_QUERY):

    # Get pagination.
    pagination = PaginationDetails(cursor, page_size)

    # list_widgets() should take a page size and offset and return a list of
    # results.
    results, has_more = list_widgets(pagination.offset, pagination.page_size)

    return PaginatedResults(
        next=(
            str(request.url.include_query_params(cursor=pagination.next_cursor()))
            if has_more else None
        ),
        previous=(
            str(request.url.include_query_params(cursor=pagination.previous_cursor()))
            if pagination.previous_cursor() else None
        ),
        results=results
    )
```

## Developer quickstart

This project contains a dockerized testing environment which wraps [tox](https://tox.readthedocs.io/en/latest/).

Tests can be run using the `./test.sh` command:

```bash
# Run all PyTest tests and Flake8 checks
$ ./test.sh

# Run just PyTest
$ ./test.sh -e py3

# Run a single test file within PyTest
$ ./test.sh -e py3 -- tests/test_identifiers.py

# Run a single test file within PyTest with verbose logging
$ ./test.sh -e py3 -- tests/test_identifiers.py -vvv
```
