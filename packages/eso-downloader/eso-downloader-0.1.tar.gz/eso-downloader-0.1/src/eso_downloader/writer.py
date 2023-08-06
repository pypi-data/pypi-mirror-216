"""
Common helper classes and functions for download files based on TAP queries.
"""
from .datalink import (
    DatalinkResult, DatalinkSemanticMap, dp_id_from_datalink_id,
)
from .utils import url_to_votable, DownloadError


class FileWriterBase:

    def __init__(self, *, session):
        self.session = session

    def save(self, *, dp_id, download_url, ob_id, science_dp_id=None):
        raise NotImplementedError("save must be defined to download files")

    def handle_tap_result(self, *, result, use_processed_calibrations=False):
        datalink_result = DatalinkResult.from_datalink_url(
            session=self.session,
            datalink_url=result.datalink_url,
        )
        try:
            night_log = datalink_result.get_night_log(session=self.session)
        except DownloadError as exc:
            print(f"Nightlog check failed: {exc}")
            return False

        if not night_log.is_acceptable:
            print(f"Night is bad, skipping: {night_log.grade}")
            return False
        else:
            print(f"Night is good ({night_log.grade}), downloading")

        self.save(
            dp_id=result.dp_id, ob_id=result.ob_id,
            download_url=datalink_result.science_file_url,
        )

        cal_url = (
            datalink_result.processed_cal_selector_url
            if use_processed_calibrations
            else datalink_result.raw_cal_selector_url
        )
        try:
            cal_table = url_to_votable(session=self.session, url=cal_url)
        except DownloadError as exc:
            print(f"Finding calibrations failed: {exc}")
            return False

        return self.handle_calibrations(
            cal_table=cal_table, science_dp_id=result.dp_id,
            science_ob_id=result.ob_id,
        )

    def filter_calibrations(self, initial_calibrations):
        return initial_calibrations

    def handle_calibrations(self, *, cal_table, science_dp_id, science_ob_id):
        inital_datalink_map = DatalinkSemanticMap.from_table(cal_table)
        cal_map = self.filter_calibrations(inital_datalink_map.calibrations)
        for url in cal_map.get_datalink_urls():
            row = DatalinkSemanticMap.from_datalink_url(
                session=self.session, url=url
            ).this_row
            self.save(
                ob_id=science_ob_id, science_dp_id=science_dp_id,
                dp_id=dp_id_from_datalink_id(row["ID"]),
                download_url=row["access_url"],
            )

        return True

    def finalise(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalise()
