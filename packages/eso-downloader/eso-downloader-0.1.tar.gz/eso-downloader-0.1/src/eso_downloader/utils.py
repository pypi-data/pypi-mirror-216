"""
Various helper functions and classes.
"""
from io import BytesIO

from astropy.io.votable import parse_single_table
from requests.exceptions import RequestException


def url_to_votable(*, session, url, invalid="mask", **kwargs):
    """
    Download a URL and read in as a VOTable.
    """

    # We would like to stream this, but astropy does seeks when reading, so we
    # can't :(
    try:
        res = session.get(url)
    except RequestException as exc:
        raise DownloadError("Failed to get response from ESO") from exc
    try:
        res.raise_for_status()
    except RequestException as exc:
        raise DownloadError("Bad response from ESO") from exc
    return parse_single_table(BytesIO(res.content), invalid=invalid, **kwargs)


class DownloadError(Exception):
    """
    Exception subclass for 'user friendly' errors that occur as part of the
    download process.
    """
    pass
