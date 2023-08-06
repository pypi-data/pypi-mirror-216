"""
A basic threadpool-based downloader and writer building upon
:class:`eso_downloader.writer.FileWriterBase` for the ESO science archive.
"""
import concurrent.futures
from pathlib import Path

from attrs import define, field
from requests_toolbelt import exceptions
from requests_toolbelt.downloadutils.stream import stream_response_to_file

from .writer import FileWriterBase


def get_save_dir(*, base_dir, ob_id, science_dp_id):
    return Path(base_dir) / str(ob_id) / science_dp_id


class PooledWriter(FileWriterBase):
    def __init__(self, *, session, base_dir, executor=None):
        super().__init__(session=session)

        if executor is None:
            executor = concurrent.futures.ThreadPoolExecutor()

        self._base_dir = base_dir
        self._executor = executor
        self._futures = set()

    def save(self, *, dp_id, download_url, ob_id, science_dp_id=None):
        if science_dp_id is None:
            science_dp_id = dp_id
        if not self._file_exists(
            dp_id=dp_id, ob_id=ob_id, science_dp_id=science_dp_id,
        ):
            self._start_download(
                dp_id=dp_id, download_url=download_url, ob_id=ob_id,
                science_dp_id=science_dp_id,
            )
        else:
            print(f"Skipping {ob_id}/{science_dp_id}/{dp_id}, exists already")

    def _file_exists(self, dp_id, ob_id, science_dp_id):
        save_dir = get_save_dir(
            base_dir=self._base_dir, ob_id=ob_id, science_dp_id=science_dp_id,
        )
        # extension could be fits or fits.fz, or possibly something else
        return bool(list(save_dir.glob(dp_id + ".*")))

    def _start_download(self, *, dp_id, download_url, ob_id, science_dp_id):
        def run_downloader(dlr):
            return dlr()

        save_dir = get_save_dir(
            base_dir=self._base_dir, ob_id=ob_id, science_dp_id=science_dp_id,
        )
        save_dir.mkdir(parents=True, exist_ok=True)

        print(f"Adding for download {ob_id}/{science_dp_id}/{dp_id}")
        downloader = Downloader(
            dp_id=dp_id,
            ob_id=ob_id,
            science_dp_id=science_dp_id,
            url=download_url,
            session=self.session,
            base_dir=self._base_dir
        )
        self._futures.add(self._executor.submit(run_downloader, downloader))

    def finalise(self, *, timeout=None):
        for future in concurrent.futures.as_completed(
            self._futures, timeout=timeout
        ):
            try:
                self._futures.discard(future)
                future.result().log_download_result()
            except Exception as exc:  # pylint: disable=broad-exception-caught
                print(f"Downloader raised uncaught {exc}")


@define
class DownloadResult:  # pylint: disable=too-few-public-methods
    dp_id = field()
    ob_id = field()
    science_dp_id = field()
    saved_filename = field(default=None)
    error = field(default=None)

    def log_download_result(self):
        if self.error is not None:
            # pylint: disable=consider-using-f-string
            print("{ob}/{sci_dp}/{dp} download failed with {e}".format(
                ob=self.ob_id,
                sci_dp=self.science_dp_id,
                dp=self.dp_id,
                e=self.error,
            ))
        else:
            print(f"Saved {self.saved_filename}")


@define
class Downloader:
    dp_id = field()
    ob_id = field()
    science_dp_id = field()
    url = field()
    session = field()
    base_dir = field()
    saved_filename = field(default=None)

    def __call__(self):
        try:
            self.do_download()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return self.fail_download(exc)
        return self.pass_download()

    def do_download(self):
        save_dir = get_save_dir(
            base_dir=self.base_dir, ob_id=self.ob_id,
            science_dp_id=self.science_dp_id
        )

        res = self.session.get(self.url, stream=True)
        try:
            self.saved_filename = stream_response_to_file(
                res, path=save_dir,
            )
        except exceptions.StreamingError as exc:
            raise RuntimeError("Download failed") from exc

    def pass_download(self):
        return DownloadResult(
            dp_id=self.dp_id,
            ob_id=self.ob_id,
            science_dp_id=self.science_dp_id,
            saved_filename=self.saved_filename,
            error=None,
        )

    def fail_download(self, error):
        return DownloadResult(
            dp_id=self.dp_id,
            ob_id=self.ob_id,
            science_dp_id=self.science_dp_id,
            saved_filename=self.saved_filename,
            error=error,
        )
