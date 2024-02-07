from datetime import date
from pathlib import Path
from dataclasses import dataclass
from enum import StrEnum
from os import getenv

from curl_cffi import requests
from curl_cffi.requests.session import BrowserType
from parsel import Selector
import json

from kyb.console import console

HEADERS = {"Cookie": getenv("CRUNCHBASE_COOKIE", "")}
IMPERSONATE = BrowserType.chrome101
TEMP_DIR = Path(".") / ".temp"


class EmployeeRange(StrEnum):
    c_00101_00250 = "101-250"


@dataclass
class Company:
    name: str
    website: str
    employee_range: str
    total_funding_amount: int
    founded_on: date
    crunchbase_url: str
    crunchbase_rank: int


def get_company_data(html_text: str):
    selector = Selector(text=html_text)
    name = selector.css("h1.profile-name::text").get()
    ng_state_text = selector.css("script#ng-state::text").get()
    assert ng_state_text, "no angular data script tag found"
    ng_state_js = json.loads(ng_state_text)
    keys = ng_state_js["HttpState"].keys()
    org_key = next((k for k in keys if "data/entities/organizations" in k))
    org_state = ng_state_js["HttpState"][org_key]
    data = org_state["data"]
    name = data["properties"]["title"]
    assert name, "name not found in script"
    cards = data["cards"]
    company_overview_highlights = cards["company_overview_highlights"]
    total_funding_amount = company_overview_highlights["funding_total"]["value"]
    assert total_funding_amount, "total_funding_amount not found in script"
    about = cards["company_about_fields2"]
    num_employees_enum = about["num_employees_enum"]
    assert num_employees_enum, "num_employees_enum not found"
    employee_range = EmployeeRange[num_employees_enum]
    website = about["website"]["value"]
    assert website, "website not found"
    perma_slug = data["properties"]["identifier"]["permalink"]
    crunchbase_url = f"https://www.crunchbase.com/organization/{perma_slug}"
    assert crunchbase_url, "crunchbase_url not found"
    crunchbase_rank = about["rank_org_company"]
    assert crunchbase_rank, "crunchbase_rank not found"
    founded_on = cards["overview_fields_extended"]["founded_on"]["value"]
    assert founded_on, "founded_on not found"
    # .HttpState["GET/v4/data/entities/organizations/getstream-iofield_ids=%5B%22identifier%22,%22layout_id%22,%22facet_ids%22,%22title%22,%22short_description%22,%22is_locked%22%5D&layout_mode=view_v2"].data.cards.overview_fields_extended.founded_on.value
    return Company(
        name=name.strip(),
        total_funding_amount=total_funding_amount,
        employee_range=str(employee_range),
        website=website,
        founded_on=founded_on,
        crunchbase_url=crunchbase_url,
        crunchbase_rank=crunchbase_rank,
    )


@dataclass
class CompanySearchResult:
    name: str
    url_slug: str
    description: str


def query_search_companies(term: str):
    # firstly check out cache
    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir(exist_ok=True)
    temp_file = TEMP_DIR / f"{term}.json"
    if temp_file.exists():
        console.log(f"temp file restored from {temp_file}")
        return json.load(temp_file.open())

    search_url = f"https://www.crunchbase.com/v4/data/autocompletes?query={term}&collection_ids=organizations&limit=25&source=topSearch"
    console.log(f"obtaining search result from url {search_url}")
    response = requests.get(search_url, impersonate=IMPERSONATE, headers=HEADERS)
    search_results = response.json()
    with open(temp_file, mode="w+") as file:
        json.dump(search_results, file)
        console.log(f"cached search results for term {term} in {file.name}")
    return search_results


def search_companies(term: str) -> list[CompanySearchResult]:
    results = query_search_companies(term)
    choices = []
    for result in results["entities"]:
        choices.append(
            CompanySearchResult(
                name=result["identifier"]["value"],
                url_slug=result["identifier"]["permalink"],
                description=result["short_description"],
            )
        )
    return choices
