import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.errors import (
    EconomyDisabledError,
    HTTPError,
    ItemNotFoundError,
    KumikoExceptionError,
    NoItemsError,
    NotFoundError,
    ValidationError,
)


def test_kumiko_exception():
    with pytest.raises(KumikoExceptionError) as e:
        raise KumikoExceptionError
    assert e.type == KumikoExceptionError


def test_item_not_found_error():
    with pytest.raises(ItemNotFoundError) as e:
        raise ItemNotFoundError
    assert e.type == ItemNotFoundError


def test_no_items_error():
    with pytest.raises(NoItemsError) as e:
        raise NoItemsError
    assert e.type == NoItemsError


def test_http_error_custom():
    with pytest.raises(HTTPError) as e:
        raise HTTPError(status=500, message="Internal Server Error")

    assert (
        (e.type == HTTPError)
        and (e.value.status == 500)
        and (e.value.message == "Internal Server Error")
    )


def test_http_error_default():
    with pytest.raises(HTTPError) as e:
        raise HTTPError(status=500, message=None)

    assert (
        (e.type == HTTPError)
        and (e.value.status == 500)
        and ("HTTP request failed (500)" in str(e.value))
    )


def test_not_found_error():
    with pytest.raises(NotFoundError) as e:
        raise NotFoundError

    assert (
        (e.type == NotFoundError)
        and (e.value.status == 404)
        and ("Resource or endpoint not found" in str(e.value))
    )


def test_validation_error():
    with pytest.raises(ValidationError) as e:
        raise ValidationError("There is an validation error")

    assert (e.type == ValidationError) and (
        "There is an validation error" in str(e.value)
    )


def test_economy_disabled_error():
    with pytest.raises(EconomyDisabledError) as e:
        raise EconomyDisabledError

    assert (e.type == EconomyDisabledError) and (
        "The economy module is disabled in this server. Please ask your server admin to enable it."
        in str(e.value)
    )
