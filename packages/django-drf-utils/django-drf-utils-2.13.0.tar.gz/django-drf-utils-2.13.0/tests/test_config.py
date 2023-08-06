import sys
from dataclasses import dataclass, field
from typing import Optional, Union

import pytest
from django_drf_utils.config import (
    BaseConfig,
    Email,
    Logging,
    Oidc,
    Session,
    unwrap_optional_type,
)

data = {
    "name": "no name",
    "description": None,
    "oidc": {
        "client_id": "test",
        "client_secret": "client_secret",
        "config_url": "https://keycloak.example/auth/realms/test/.well-known/openid-configuration",
        "login_redirect_url": "http://localhost",
        "logout_redirect_url": "http://localhost",
    },
    "email": {
        "host": "test.example",
        "port": 25,
        "use_tls": True,
        "user": "chuck",
        "password": "***",
        "from_address": "noreply@example.org",
        "subject_prefix": "Test prefix: ",
    },
    "session": {"expire_at_browser_close": True, "expire_seconds": 3600},
    "logging": {"level": "DEBUG"},
}


@dataclass
class ConfigTest(BaseConfig):
    name: str
    oidc: Oidc
    description: Optional[str] = None
    email: Optional[Email] = None
    logging: Logging = field(default_factory=Logging)
    session: Session = field(default_factory=Session)


def test_from_dict():
    cfg = ConfigTest.from_dict(data)
    assert cfg.name == data["name"]
    assert cfg.oidc == Oidc.from_dict(data["oidc"])
    assert cfg.email == Email.from_dict(data["email"])


def test_empty():
    cfg = ConfigTest.empty()
    # pylint: disable=no-member
    assert cfg.name == ""
    assert cfg.description is None
    assert cfg.oidc.client_id == ""
    assert cfg.oidc.login_redirect_url == "/"
    assert cfg.session.expire_at_browser_close is False
    assert cfg.session.expire_seconds == 86400
    # pylint: enable=no-member


@pytest.mark.parametrize(
    "t, expected",
    (
        (None, None),
        (str, str),
        (Optional[str], str),
        (Union[str, None], str),
        (Union[None, str], str),
        (ConfigTest, ConfigTest),
        (Optional[ConfigTest], ConfigTest),
    ),
)
def test_unwrap_optional_type(t, expected):
    assert unwrap_optional_type(t) == expected


if sys.version_info >= (3, 10):

    @pytest.mark.parametrize(
        "t, expected",
        (
            (int | None, int),
            (None | int, int),  # type: ignore
        ),
    )
    def test_unwrap_optional_type_union_type(t, expected):
        assert unwrap_optional_type(t) == expected
