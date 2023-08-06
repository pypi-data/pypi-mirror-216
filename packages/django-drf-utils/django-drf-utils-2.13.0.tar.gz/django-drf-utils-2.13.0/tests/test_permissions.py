import pytest

from django.test import RequestFactory

from django_drf_utils.permissions import (
    IsRead,
    IsWrite,
    IsUpdate,
)


@pytest.mark.parametrize(
    "permission_class, method, allowed",
    (
        (IsUpdate, "GET", False),
        (IsUpdate, "HEAD", False),
        (IsUpdate, "OPTIONS", False),
        (IsUpdate, "PUT", True),
        (IsUpdate, "PATCH", True),
        (IsUpdate, "POST", False),
        (IsUpdate, "DELETE", False),
        (IsRead, "GET", True),
        (IsRead, "HEAD", True),
        (IsRead, "OPTIONS", True),
        (IsRead, "PUT", False),
        (IsRead, "PATCH", False),
        (IsRead, "POST", False),
        (IsRead, "DELETE", False),
        (IsWrite, "GET", False),
        (IsWrite, "HEAD", False),
        (IsWrite, "OPTIONS", False),
        (IsWrite, "PUT", True),
        (IsWrite, "PATCH", True),
        (IsWrite, "POST", True),
        (IsWrite, "DELETE", True),
    ),
)
def test_request_http_method_classes(permission_class, method, allowed):
    permission_object = permission_class()
    request = RequestFactory().request(REQUEST_METHOD=method)
    assert permission_object.has_permission(request, None) == allowed
