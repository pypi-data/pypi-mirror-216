"""
Helper classes and functions related to ESO's datalink services.
"""
from collections import defaultdict
from collections.abc import Mapping
import enum

from attrs import define, field
from requests.exceptions import RequestException

from .night_log import NightLog
from .utils import url_to_votable, DownloadError


class DatalinkSemanticsLabel(enum.Enum):
    """
    An :class:`enum.Enum` representing the various possible values that the ESO
    datalink service provide for the semantics column.
    """
    CURRENT_FILE = "#this"
    NIGHT_LOG = "http://archive.eso.org/rdf/datalink/eso#night_log"
    RAW_CAL = "http://archive.eso.org/rdf/datalink/eso#calSelector_raw2raw"
    MASTER_CAL = (
        "http://archive.eso.org/rdf/datalink/eso#calSelector_raw2master"
    )
    CALIBRATION = "#calibration"
    DERIVATION = "#derivation"

    @classmethod
    def _missing_(cls, value):
        return value


@define
class DatalinkResult:
    """
    A helper class for loading and parsing a datalink result from the ESO
    archive.

    The semantics column is consulted to perform the discovery of relevant rows
    and their contents.

    Parameters
    ----------
    science_file_url: str
        The url to the original science file.
    night_log_url: str
        The url to the night log associated with the original science file.
    raw_cal_selector_url: str
        The url to the calibration selector service containing the raw
        calibrations for the original science file.
    processed_cal_selector_url: str
        The url to the calibration selector service containing the reduced
        calibrations (and raw if no reduced calibrations are available) for the
        original science file.
    """

    science_file_url = field()
    night_log_url = field()
    raw_cal_selector_url = field()
    processed_cal_selector_url = field()

    def get_night_log(self, *, session):
        """
        Get the parsed night log for this datalink result.

        Parameters
        ----------
        session: :class:`requests.Session`
            A session containing authentication details allowing access to the
            data.

        Returns
        -------
        :class:`eso_downloader.night_log.NightLog`
            The parsed night log for this datalink result.
        """
        try:
            res = session.get(self.night_log_url)
        except RequestException as exc:
            raise DownloadError(
                "Failed to get response from ESO for nightlog"
            ) from exc
        try:
            res.raise_for_status()
        except RequestException as exc:
            raise DownloadError("Bad response from ESO for nightlog") from exc
        return NightLog.from_str(res.text)

    @classmethod
    def from_datalink_url(cls, *, session, datalink_url):
        """
        Create a :class:`eso_downloader.datalink.DatalinkResult` from a URL to
        ESO's datalink service.

        Parameters
        ----------
        session: :class:`requests.Session`
            A session containing authentication details allowing access to the
            data.
        datalink_url: str
            A URL pointing to a ESO's datalink service for a specific science
            file.

        Returns
        -------
        :class:`eso_downloader.datalink.DatalinkResult`
            The parsed datalink result.
        """
        mapping = DatalinkSemanticMap.from_datalink_url(
            session=session, url=datalink_url
        )

        return cls(
            science_file_url=mapping.this_access_url,
            night_log_url=mapping.get_first_access_url(
                DatalinkSemanticsLabel.NIGHT_LOG
            ),
            raw_cal_selector_url=mapping.get_first_access_url(
                DatalinkSemanticsLabel.RAW_CAL
            ),
            processed_cal_selector_url=mapping.get_first_access_url(
                DatalinkSemanticsLabel.MASTER_CAL
            ),
        )

    def get_raw_cal_table(self, *, session):
        return url_to_votable(session=session, url=self.raw_cal_selector_url)

    def get_processed_cal_table(self, *, session):
        return url_to_votable(
            session=session, url=self.processed_cal_selector_url
        )


class DatalinkCalibrationMap(Mapping):
    """
    Datalink result handler which collects together rows of the same kind of
    calibration.

    Row classification is based on the ``"eso_category"`` column.
    """
    def __init__(self):
        self._mapping = defaultdict(list)

    def add_row(self, row):
        """
        Add a row from a ESO datalink service to the mapping, based on the
        category of the file.

        Parameters
        ----------
        row:
            A row from an ESO datalink service.
        """
        category = row["eso_category"]
        self._mapping[category].append(row)

    def __len__(self):
        return len(self._mapping)

    def __iter__(self):
        return iter(self._mapping)

    def __getitem__(self, item):
        return self._mapping[item]

    def __contains__(self, item):
        return item in self._mapping

    def get_datalink_urls(self):
        """
        Get an iterator over the datalink URLs for the rows held by this
        wrapper.

        Yields
        ------
        datalink_url: str
            The datalink URLs for the files
        """
        for cat_list in self.values():
            for row in cat_list:
                yield row["eso_datalink"]


class DatalinkSemanticMap(Mapping):
    def __init__(self, mapping):
        self._mapping = mapping

    @classmethod
    def from_table(cls, table):
        mapping = defaultdict(list)
        mapping[DatalinkSemanticsLabel.CALIBRATION] = DatalinkCalibrationMap()
        calib_map = mapping[DatalinkSemanticsLabel.CALIBRATION]
        for row in table.array:
            semantics = DatalinkSemanticsLabel(row["semantics"])
            if semantics == DatalinkSemanticsLabel.CALIBRATION:
                calib_map.add_row(row)
            else:
                mapping[semantics].append(row)

        return cls(mapping)

    @classmethod
    def from_datalink_url(cls, *, session, url):
        table = url_to_votable(session=session, url=url)
        return cls.from_table(table)

    def __len__(self):
        return len(self._mapping)

    def __iter__(self):
        return iter(self._mapping)

    def __getitem__(self, item):
        return self._mapping[item]

    def __contains__(self, item):
        return item in self._mapping

    def get_first(self, item):
        value = self.get(item, None)
        if isinstance(value, list):
            if not value:
                return None
            return value[0]
        return value

    def get_first_access_url(self, item):
        value = self.get_first(item)
        if value is not None:
            return value["access_url"]
        return None

    @property
    def calibrations(self):
        return self[DatalinkSemanticsLabel.CALIBRATION]

    @property
    def this_access_url(self):
        return self.get_first_access_url(DatalinkSemanticsLabel.CURRENT_FILE)

    @property
    def this_row(self):
        return self.get_first(DatalinkSemanticsLabel.CURRENT_FILE)


def dp_id_from_datalink_id(link_id):
    """
    Get the ``dp_id`` from the datalink ID.
    """
    # The ID isn't a valid URL, guess we split on '?'...
    return link_id.strip().split("?")[1]
