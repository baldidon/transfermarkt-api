from dataclasses import dataclass
from datetime import datetime
from app.services.base import TransfermarktBase
from app.utils.regex import REGEX_CHART_CLUB_ID
from app.utils.xpath import Managers
from app.utils.utils import extract_from_url, safe_regex

@dataclass
class TransfermarktManagerSearch(TransfermarktBase):
    """
    A class for searching football managers (only coaches) on Transfermarkt and retrieving search results.

    Args:
        query (str): The search query for finding football clubs.
        URL (str): The URL template for the search query.
        pippo (int): The page number of search results (default is 1).
    """
    query: str = None
    URL: str = (
        "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={query}&Spieler_page={page_number}"
    )

    page_number: int = 1

    def __post_init__(self) -> None:
        """Initialize the TransfermarktManagerSearch class."""
        self.URL = self.URL.format(query=self.query, page_number=self.page_number)
        self.page = self.request_url_page()
        self.raise_exception_if_not_found(xpath=Managers.Search.FOUND)
    
    def __parse_search_results(self) -> list:
        """
        Parse and return a list of managers search results. Each result includes manager information such as their unique
        identifier, name, club (including ID and name), age, nationality.

        Returns:
            list: A list of dictionaries, with each dictionary representing a manager search result.
        """
        idx = [extract_from_url(url) for url in self.get_list_by_xpath(Managers.Search.URL)]
        name = self.get_list_by_xpath(Managers.Search.NAME)
        club_name = self.get_list_by_xpath(Managers.Search.CLUB_NAME)
        club_id = [
            safe_regex(img, REGEX_CHART_CLUB_ID, "club_id") for img in self.get_list_by_xpath(Managers.Search.CLUB_IMAGE)
        ]
        contract = self.get_list_by_xpath(Managers.Search.CONTRACT)
        age = self.get_list_by_xpath(Managers.Search.AGE)
        nationality = self.get_list_by_xpath(Managers.Search.NATIONALITY)
        function = self.get_list_by_xpath(Managers.Search.FUNCTION)

        return [ 
            {
                "id": idx,
                "name": name,
                "age": age,
                "nationality": nationality,
                "club": {
                    "id": club_id,
                    "name": club_name,
                },
                "contract": contract,
                "function": function,
            } 
        for idx,
            name,
            age, 
            nationality,
            club_id,
            club_name,
            contract,
            function in zip(idx, name, age, nationality, club_id, club_name, contract, function)
        ]


    def search_managers(self) -> dict:
        """
        Retrieve and parse the search results for managers matching the specified query. The results
            include player information such as their name, club, age, nationality, and function.

        Returns:
            dict: A dictionary containing the search query, page number, last page number, search
                results, and the timestamp of when the data was last updated.
        """
        self.response["query"] = self.query
        self.response["pageNumber"] = self.page_number
        self.response["lastPageNumber"] = self.get_search_last_page_number(Managers.Search.BASE)
        self.response["results"] = self.__parse_search_results()
        self.response["updatedAt"] = datetime.now()

        return self.response
        
       

