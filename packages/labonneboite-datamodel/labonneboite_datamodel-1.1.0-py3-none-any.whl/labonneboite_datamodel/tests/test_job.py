from unittest import TestCase
from .. import Naf, Job
from pytest import raises


def _get_valid_job() -> dict:
    return {
        "rome": "M1234",
        "naf": "12",
        "label_naf": "Something",
        "label_rome": "Something",
        "hirings": 60

    }


def _get_valid_naf() -> dict:
    return {
        "naf": "1234Z",
        "label": "Something",
    }

# valid job


def test_job_valid() -> None:
    data = _get_valid_job()
    assert Job.validate(data).rome == "M1234"


def test_naf_valid() -> None:
    data = _get_valid_naf()
    assert Naf.validate(data).naf == "1234Z"

# invalid naf


def test_job_naf_invalid() -> None:
    data = _get_valid_job()

    for value in ["1f", "0", "abc2"]:

        data["naf"] = value

        with raises(ValueError):
            Job.validate(data)


def test_naf_naf_invalid() -> None:
    data = _get_valid_naf()

    for value in ["1f", "0", "abc2", "123f5", "f2345"]:

        data["naf"] = value

        with raises(ValueError):
            Naf.validate(data)

# invalid naf


def test_job_rome_invalid() -> None:
    data = _get_valid_job()

    for value in ["1".zfill(5), "0".zfill(4), "abc2".zfill(5)]:

        data["rome"] = value

        with raises(ValueError):
            Job.validate(data)
