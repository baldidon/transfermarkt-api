from dataclasses import dataclass
from datetime import datetime

from app.services.base import TransfermarktBase
from app.utils.utils import (
    clean_response,
    extract_from_url,
)
from app.utils.xpath import Managers

@dataclass
class TransfermarktManagerProfile(TransfermarktBase):
    """
    Represents a service for retrieving and parsing the profile information of a football manager on Transfermarkt.

    Args:
        manager_id (str): The unique identifier of the manager.

    Attributes:
        URL (str): The URL to fetch the player's profile data.
    """
    manager_id: str = None
    URL: str = "https://www.transfermarkt.com/-/profil/trainer/{manager_id}"

    def __post_init__(self) -> None:
        """Initialize the TransfermarktPlayerProfile class."""
        self.URL = self.URL.format(manager_id=self.manager_id)
        self.page = self.request_url_page()
        self.raise_exception_if_not_found(xpath=Managers.Profile.URL)

    def get_manager_profile(self) -> dict:
        """
        Retrieve and parse the player's profile information, including their personal details,
        club affiliations, market value, agent information, social media links, and more.

        Returns:
            dict: A dictionary containing the player's unique identifier, profile information, and the timestamp of when
                the data was last updated.
        """
        self.response["id"] = self.get_text_by_xpath(Managers.Profile.ID)
        self.response["url"] = self.get_text_by_xpath(Managers.Profile.URL)
        self.response["name"] = self.get_text_by_xpath(Managers.Profile.NAME)
        self.response["description"] = self.get_text_by_xpath(Managers.Profile.DESCRIPTION)
        self.response["fullName"] = self.get_text_by_xpath(Managers.Profile.FULL_NAME)
        self.response["nameInHomeCountry"] = self.get_text_by_xpath(Managers.Profile.NAME_IN_HOME_COUNTRY)
        self.response["imageURL"] = self.get_text_by_xpath(Managers.Profile.IMAGE_URL)
        self.response["dateOfBirth"] = self.get_text_by_xpath(Managers.Profile.DATE_OF_BIRTH)
        self.response["placeOfBirth"] = {
            "city": self.get_text_by_xpath(Managers.Profile.PLACE_OF_BIRTH_CITY),
            "country": self.get_text_by_xpath(Managers.Profile.PLACE_OF_BIRTH_COUNTRY),
        }
        self.response["age"] = self.get_text_by_xpath(Managers.Profile.AGE)
        self.response["citizenship"] = self.get_list_by_xpath(Managers.Profile.CITIZENSHIP)
        self.response['currentClub'] = {
            "currentClubName":self.get_text_by_xpath(Managers.Profile.CURRENT_CLUB_NAME),   
            "currentClubId":extract_from_url(self.get_text_by_xpath(Managers.Profile.CURRENT_CLUB_URL)),
            "currentClubAppointed": self.get_text_by_xpath(Managers.Profile.CURRENT_CLUB_APPOINTED),
            "currentClubContractExpires": self.get_text_by_xpath(Managers.Profile.CURRENT_CLUB_CONTRACT_EXPIRES),
        }
        self.response['avgTermAsManager'] = self.get_text_by_xpath(Managers.Profile.AVG_TERM_AS_MANAGER)
        self.response['licence'] = self.get_text_by_xpath(Managers.Profile.LICENCE)
        self.response['preferredFormation'] = self.get_text_by_xpath(Managers.Profile.PREFERRED_FORMATION)
        self.response["updatedAt"] = datetime.now()

        return clean_response(self.response)
