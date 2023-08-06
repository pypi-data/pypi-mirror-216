"""
Helper classes and functions for handling a single program request.
"""
from attrs import define, field

from .auth import get_user_session
from .pooled_writer import PooledWriter
from .tap import get_science_datalink_urls


@define
class ProgramRequest:
    """
    Container class for a single program request.
    """
    program_id = field()
    username = field()
    base_dir = field()

    def get_session(self, **kwargs):
        return get_user_session(username=self.username, **kwargs)

    def get_science_results(self, *, session=None):
        if session is None:
            session = self.get_session()
        return get_science_datalink_urls(
            session=session, program_id=self.program_id
        )

    def get_writer(self, *, session=None, writer_cls=None, **kwargs):
        if writer_cls is None:
            writer_cls = PooledWriter

        if session is None:
            session = self.get_session()

        return writer_cls(session=session, base_dir=self.base_dir, **kwargs)

    def download_files(
        self, *, writer=None, session=None, writer_cls=None, **kwargs
    ):
        if writer is not None and session is None:
            session = writer.session
        if session is None:
            session = self.get_session()
        if writer is None:
            writer = self.get_writer(session=session, writer_cls=writer_cls)
        try:
            for result in self.get_science_results(session=session):
                writer.handle_tap_result(result=result, **kwargs)
                try:
                    # Do a short cleanout of done downloads
                    writer.finalise(timeout=0.01)
                except TimeoutError:
                    pass
        except KeyboardInterrupt:
            print("Finishing downloads...")
            writer.finalise()
        else:
            writer.finalise()

    def log_start(self):
        # pylint: disable=consider-using-f-string
        print("Starting download for {p_id} with username {u} into {d}".format(
            p_id=self.program_id, u=self.username, d=self.base_dir,
        ))

    def log_end(self):
        # pylint: disable=consider-using-f-string
        print("Finished download for {p_id} with username {u} into {d}".format(
            p_id=self.program_id, u=self.username, d=self.base_dir,
        ))
