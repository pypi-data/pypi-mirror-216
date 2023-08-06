import pytest

from eso_downloader.night_log import NightLog, Grade


@pytest.mark.parametrize("filename,expected_grade", [
    ("SPHER.2016-09-26T03 04 09.308.NL.txt", Grade.A),
])
def test_galah(shared_datadir, filename, expected_grade):
    nl = NightLog.from_path(shared_datadir / "nightlogs" / filename)

    assert nl.grade == expected_grade
