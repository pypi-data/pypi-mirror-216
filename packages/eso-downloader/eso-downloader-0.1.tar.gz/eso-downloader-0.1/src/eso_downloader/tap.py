"""
Helper classes and functions for querying the ESO archive TAP service.
"""
from attrs import define, field
from pyvo.dal import TAPService

ESO_TAP_OBS = "https://archive.eso.org/tap_obs"
TAP_OBS_QUERY = """
    SELECT dp_id, datalink_url, ob_id FROM dbo.raw
    WHERE prog_id = '{prog_id}' AND dp_cat = 'SCIENCE'
"""


@define
class ScienceQueryResult:  # pylint: disable=too-few-public-methods
    dp_id = field()
    datalink_url = field()
    ob_id = field()

    @classmethod
    def from_row(cls, row):
        return cls(
            dp_id=row.get("dp_id"),
            datalink_url=row.get("datalink_url"),
            ob_id=row.get("ob_id"),
        )


def get_science_datalink_urls(*, session, program_id):
    """
    Get an iterator which yields `ScienceQueryResult` for each result.
    """
    query = TAP_OBS_QUERY.format(prog_id=program_id)
    tap_service = TAPService(ESO_TAP_OBS, session)
    print("Starting TAP query")
    results = tap_service.run_sync(query)
    print("Got TAP query,", len(results), "science observations found")
    for result in results:
        yield ScienceQueryResult.from_row(result)
