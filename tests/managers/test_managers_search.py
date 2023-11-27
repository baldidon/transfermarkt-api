from datetime import datetime

import pytest
from schema import And, Schema

from app.services.managers.search import TransfermarktManagerSearch


def test_players_search_empty(len_greater_than_0, len_equal_to_0):
    tfmkt = TransfermarktManagerSearch(query="0")
    result = tfmkt.search_players()

    expected_schema = Schema(
        {
            "query": And(str, len_greater_than_0),
            "pageNumber": 1,
            "lastPageNumber": 1,
            "results": And(list, len_equal_to_0),
            "updatedAt": datetime,
        },
    )

    assert expected_schema.validate(result)


@pytest.mark.parametrize("query,page_number", [("Messi", 1), ("Ronaldo", 2)])
def test_players_search(query, page_number, len_greater_than_0, regex_integer, regex_market_value):
    tfmkt = TransfermarktManagerSearch(query=query, page_number=page_number)
    result = tfmkt.search_managers()

    expected_schema = Schema(
        {
            "query": query,
            "pageNumber": page_number,
            "lastPageNumber": And(int, lambda x: x > 1),
            "results": [
                {
                    "id": And(str, len_greater_than_0, regex_integer),
                    "name": And(str, len_greater_than_0),
                    "age": And(str, len_greater_than_0, regex_integer),
                    "nationality": And(str, len_greater_than_0),
                    "club": {
                        "id": And(str, len_greater_than_0, regex_integer),
                        "name": And(str, len_greater_than_0),
                    },
                    "contract": And(str, len_greater_than_0),
                    "function": And(str, len_greater_than_0),
                },
            ],
            "updatedAt": datetime,
        },
    )

    assert expected_schema.validate(result)
