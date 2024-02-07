from curl_cffi import requests

from kyb.scrapers.crunchbase import (
    CompanySearchResult,
    get_company_data,
    search_companies,
)
from uuid import uuid4


COMPANY_SITE_HTML = "crunchbase_company.html"


def test_get_company_data(data_file):
    # GIVEN
    file = data_file(COMPANY_SITE_HTML)

    # WHEN
    data = get_company_data(html_text=file.read())

    # THEN
    assert data.name == "Stream"
    assert data.total_funding_amount == 58058000
    assert data.employee_range == "101-250"
    assert data.website == "https://getstream.io/"
    assert data.founded_on == "2014-08-01"
    assert data.crunchbase_url == "https://www.crunchbase.com/organization/getstream-io"
    assert data.crunchbase_rank == 1446


def test_search_companies_response_handled(mocker, tmp_path):
    # GIVEN
    # cache is not used
    temp_dir = tmp_path / ".temp"
    temp_dir.mkdir()
    mocker.patch("kyb.scrapers.crunchbase.TEMP_DIR", temp_dir)
    requests_get = mocker.patch.object(requests, "get", autospec=True)
    data = {
        "count": 9001,
        "entities": [
            {
                "facet_ids": [
                    "contact",
                    "company",
                    "rank",
                ],
                "identifier": {
                    "uuid": str(uuid4()),
                    "value": "Stream",
                    "image_id": "v1502291302/owrqz1ikabuc8laaix4d.png",
                    "permalink": "getstream-io",
                    "entity_def_id": "organization",
                },
                "short_description": "Stream builds chat and feeds for applications at scale in a fraction of the time and cost of developing in-house.",
            },
            {
                "foo_spam": [],
                "identifier": {"value": "Steam", "permalink": "steam"},
                "short_description": "gaming platform",
            },
        ],
    }
    response = requests_get.return_value
    response.json.return_value = data

    # WHEN
    results = search_companies("foo")

    # THEN
    assert results == [
        CompanySearchResult(
            name="Stream",
            url_slug="getstream-io",
            description="Stream builds chat and feeds for applications at scale in a fraction of the time and cost of developing in-house.",
        ),
        CompanySearchResult(
            name="Steam", url_slug="steam", description="gaming platform"
        ),
    ]


def test_scrape_details():
    pass
