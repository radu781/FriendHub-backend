import pytest
import utils.validators.other as validators


@pytest.mark.unit
def test_password_ok():
    try:
        validators.check_password("Very Saf3 pass!!", force_validation=True)
    except ValueError:
        assert False, "Password validation failed for correct password"


@pytest.mark.unit
def test_password_nok():
    with pytest.raises(ValueError):
        validators.check_password("123", force_validation=True)


@pytest.mark.unit
def test_password_error():
    try:
        validators.check_password("123", force_validation=True)
    except ValueError as ex:
        assert ex.args[0] == "incorrect password format"


@pytest.mark.unit
def test_email_ok():
    try:
        validators.check_email("a@a.a", force_validation=True)
    except ValueError:
        assert False, "Email validation failed for correct password"


@pytest.mark.unit
def test_email_nok():
    with pytest.raises(ValueError):
        validators.check_email("email", force_validation=True)


@pytest.mark.unit
def test_email_error():
    try:
        validators.check_email("email", force_validation=True)
    except ValueError as ex:
        assert ex.args[0] == "incorrect email format"


@pytest.mark.unit
def test_name_ok():
    try:
        validators.check_name("Radu", force_validation=True)
    except ValueError:
        assert False, "Name validation failed for correct password"


@pytest.mark.unit
def test_name_nok():
    with pytest.raises(ValueError):
        validators.check_name("radu123", force_validation=True)


@pytest.mark.unit
def test_name_error():
    try:
        validators.check_name("radu123", force_validation=True)
    except ValueError as ex:
        assert ex.args[0] == "incorrect name format"
