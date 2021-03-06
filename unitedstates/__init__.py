from pupa.scrape import Jurisdiction, Organization
from .legislative import UnitedStatesLegislativeScraper
from .disclosures import (UnitedStatesLobbyingRegistrationDisclosureScraper,
                          UnitedStatesHousePostEmploymentScraper,
                          UnitedStatesSenatePostEmploymentScraper)

# scrapers
from .bill import UnitedStatesBillScraper
from .committee import UnitedStatesCommitteeScraper


class UnitedStates(Jurisdiction):
    classification = 'government'
    division_id = 'ocd-division/country:us'

    name = 'United States Federal Government'
    url = 'http://usa.gov/'

    parties = [
        {"name": "Republican", },
        {"name": "Democratic", },
        {"name": "Independent", },
    ]

    scrapers = {
        "congress": UnitedStatesLegislativeScraper,
        "lobbying_registrations":
            UnitedStatesLobbyingRegistrationDisclosureScraper,
        "house_post_employment":
            UnitedStatesHousePostEmploymentScraper,
        "senate_post_employment":
            UnitedStatesSenatePostEmploymentScraper,
        # Executive Scraper here
        "bills": UnitedStatesBillScraper,
        "committees": UnitedStatesCommitteeScraper
    }

    def get_organizations(self):
        legislature = Organization("United States Congress",
                                   classification='legislature')

        self._legislature = legislature

        yield legislature

        senate = Organization(
            name="United States Senate",
            classification='upper',
            parent_id=legislature._id,
        )

        self._senate = senate

        yield senate

        house = Organization(
            name="United States House",
            classification='lower',
            parent_id=legislature._id,
        )

        self._house = house

        yield house

        sopr = Organization(
            name="Office of Public Record, US Senate",
            classification="office",
            parent_id=senate._id,
        )

        sopr.add_contact_detail(type="voice",
                                value="202-224-0322")

        sopr.add_source(url="http://www.senate.gov/pagelayout/legislative/"
                            "one_item_and_teasers/opr.htm",
                        note="Profile page")

        sopr.add_source(url="http://www.senate.gov/pagelayout/legislative/"
                            "g_three_sections_with_teasers/lobbyingdisc.htm"
                            "#lobbyingdisc=lda",
                        note="Disclosure Home")

        sopr.add_link(url="http://soprweb.senate.gov/index.cfm"
                          "?event=selectfields",
                      note="Disclosure Search Portal")

        sopr.add_link(url="http://soprweb.senate.gov/",
                      note="Disclosure Electronic Filing System")

        self._sopr = sopr

        yield sopr

        house_clerk = Organization(
            name="Office of the Clerk, US House",
            classification="office",
            parent_id=house._id,
        )

        house_clerk.add_contact_detail(type="voice",
                                       value="202-225-7000")

        house_clerk.add_source(url="http://clerk.house.gov/",
                               note="Home page")

        self._house_clerk = house_clerk

        yield house_clerk
        yield legislature
