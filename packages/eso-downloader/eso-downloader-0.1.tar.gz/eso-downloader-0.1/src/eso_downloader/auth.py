"""
Helper functions and classes to manage authenticated access to the ESO archive.
"""
from datetime import datetime, timezone
from logging import getLogger

import keyring
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from . import __version__

KEYRING_SERVICE_NAME = "eso-downloader"
JWT_CREATION_URL = "https://www.eso.org/sso/oidc/token"
BASE_PARAMS_JWT_CREATION_URL = {
    "response_type": "id_token token",
    "grant_type": "password",
    "client_id": "clientid",
}
DEFAULT_SESSION_RETRIES = Retry(
    total=None,  # Disable the overall limit, use individual limits
    connect=10,
    read=10,
    redirect=10,
    status=10,
    other=10,
    backoff_factor=0.1,
    backoff_jitter=0.1,
)

logger = getLogger(__name__)


def _get_archive_jwt(*, username, password):
    params = {"username": username, "password": password}
    params.update(**BASE_PARAMS_JWT_CREATION_URL)
    resp = requests.get(JWT_CREATION_URL, params=params, timeout=60)
    resp.raise_for_status()
    json_resp = resp.json()
    return json_resp["id_token"]


def _parse_jwt(jwt_str):
    try:
        import jwt  # pylint: disable=import-outside-toplevel
    except ImportError:
        logger.info("Unable to import jwt, so unable to read jwt")
        return None

    # We not verifying or checking for expiry as we don't want to keep
    # track of the signing key, and expiry we'll check separately
    return jwt.JWT().decode(jwt_str, do_verify=False, do_time_check=False)


class ESOJWTAuth(requests.auth.AuthBase):
    """
    :class:`requests.auth.AuthBase` subclass which automatically gets the JWT
    for ESO archive access.

    This uses the ``keyring`` package to acquire the user's password,
    and if the ``jwt`` package is installed, can automatically refresh the JWT
    as needed.

    Parameters
    ----------
    username: str
        The ESO portal username to get the token for.
    service: str, optional
        The service name to use when querying ``keyring``.
    """
    def __init__(self, *, username, service=KEYRING_SERVICE_NAME):
        self.username = username
        self._service_name = service
        self._get_token()

    def _get_token(self):
        # TODO: Work out the best way to tell users what backends are available
        # if keyring fails to find a backend.
        password = keyring.get_password(self._service_name, self.username)
        if password is None:
            raise ValueError(f"No password set for {self.username}")
        self.token = _get_archive_jwt(
            username=self.username, password=password
        )
        self._token_content = _parse_jwt(self.token)

    @property
    def token_contents(self):
        """
        The parsed contents of the JWT. May be ``None`` if parsing failed.
        """
        return self._token_content

    def __call__(self, r):
        if self.token_contents:
            now = datetime.now(timezone.utc)
            not_before = datetime.fromtimestamp(
                self.token_contents["nbf"], timezone.utc
            )
            expires = datetime.fromtimestamp(
                self.token_contents["exp"], timezone.utc
            )
            if now >= expires:
                self._get_token()
            elif now < not_before:
                raise ValueError("Token not yet ready for use?!?")
        r.headers['Authorization'] = f"Bearer {self.token}"
        return r


def get_user_session(*, username, session_retries=None, **kwargs):
    """
    Get a :class:`requests.Session` wrapping a :class:`ESOJWTAuth` instance for
    authenticated access to the ESO archive.

    Parameters
    ----------
    username: str
        The ESO portal username to get the token for.
    session_retries: varies, optional
        Passed directly to ``urllib3``, see it for retry details.
    **kwargs : dict, optional
        Extra arguments to :class:`ESOJWTAuth` creation.

    Returns
    -------
    :class:`requests.Session`
        A :class:`requests.Session` instance with authentication configured and
        with useful headers set (see code for specifics).
    """
    if session_retries is None:
        session_retries = DEFAULT_SESSION_RETRIES
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=session_retries))
    session.mount('https://', HTTPAdapter(max_retries=session_retries))
    session.auth = ESOJWTAuth(username=username, **kwargs)
    session.headers["User-Agent"] = f"eso-downloader ({__version__})"
    return session


def store_eso_password(
    *, username, password, service_name=KEYRING_SERVICE_NAME
):
    """
    Store the provided username/password pair in the keyring.

    Parameters
    ----------
    username: str
        The ESO portal username to store.
    password: str
        The ESO portal password to store.
    service: str, optional
        The service name to use when querying ``keyring``.
    """

    return keyring.set_password(service_name, username, password)
