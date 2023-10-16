import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.errors import (
    EconomyDisabledError,
    KumikoExceptionError,
    PinsDisabledError,
    RedirectsDisabledError,
    ValidationError,
)


def test_kumiko_exception():
    with pytest.raises(KumikoExceptionError) as e:
        raise KumikoExceptionError
    assert e.type == KumikoExceptionError


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


def test_redirects_disabled_error():
    with pytest.raises(RedirectsDisabledError) as e:
        raise RedirectsDisabledError

    assert (e.type == RedirectsDisabledError) and (
        "The redirects module is disabled in this server. Please ask your server admin to enable it."
        in str(e.value)
    )


def test_pins_disabled_error():
    with pytest.raises(PinsDisabledError) as e:
        raise PinsDisabledError

    assert (e.type == PinsDisabledError) and (
        "The pins module is disabled in this server. Please ask your server admin to enable it."
        in str(e.value)
    )
