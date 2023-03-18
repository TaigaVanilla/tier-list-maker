import pytest
from app import app
from forms import ListForm, LoginForm, RegistrationForm


@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client


def set_form_data(form, data):
    for field_name, value in data.items():
        field = getattr(form, field_name)
        field.data = value
        field.raw_data = [value]


def make_registration_form(username, password, confirm):
    form = RegistrationForm()
    form_data = {
        'username': username,
        'password': password,
        'confirm': confirm,
    }
    set_form_data(form, form_data)
    return form


def make_login_form(username, password):
    form = LoginForm()
    form_data = {
        'username': username,
        'password': password,
    }
    set_form_data(form, form_data)
    return form


def make_list_form(rank_list, content_list, comment_list):
    form = ListForm()
    for rank, content, comment in zip(rank_list, content_list, comment_list):
        form.rank.append_entry(rank)
        form.content.append_entry(content)
        form.comment.append_entry(comment)
    for i in range(len(form.rank.entries)):
        form.rank.entries[i].raw_data = [form.rank.entries[i].data]
        form.content.entries[i].raw_data = [form.content.entries[i].data]
        form.comment.entries[i].raw_data = [form.comment.entries[i].data]
    return form


def test_registration_form(client):
    # Valid registration
    form = make_registration_form('testuser', 'testpassword', 'testpassword')
    assert form.validate()

    # Passwords don't match
    form = make_registration_form('testuser', 'testpassword', 'mismatch')
    assert not form.validate()

    # Username is empty
    form = make_registration_form('', 'testpassword', 'testpassword')
    assert not form.validate()

    # Passwords are empty
    form = make_registration_form('testuser', '', '')
    assert not form.validate()

    # Username is too long
    form = make_registration_form('a' * 21, 'testpassword', 'testpassword')
    assert not form.validate()

    # Passwords are too short
    form = make_registration_form('testuser', 'a' * 5, 'a' * 5)
    assert not form.validate()

    # Valid max username and min passwords lengths
    form = make_registration_form('a' * 20, 'a' * 6, 'a' * 6)
    assert form.validate()


def test_login_form(client):
    # Valid registration
    form = make_login_form('testuser', 'testpassword')
    assert form.validate()

    # Username is empty
    form = make_login_form('', 'testpassword')
    assert not form.validate()

    # password is empty
    form = make_login_form('testuser', '')
    assert not form.validate()


def test_list_form(client):
    # Valid registration
    form = make_list_form([1, 2, 3], ['apple', 'banana', 'cherry'], ['best', 'better', 'ok'])
    assert form.validate()

    # Rank is empty
    form = make_list_form(['', '', ''], ['content1', 'content2', 'content3'], ['comment1', 'comment2', 'comment3'])
    assert not form.validate()

    # Valid content and comment are empty
    form = make_list_form([1, 2, 3], ['', '', ''], ['', '', ''])
    assert form.validate()

    # Rank is too large
    form = make_list_form([100000], ['item'], ['item'])
    assert not form.validate()

    # Rank is too small
    form = make_list_form([-1], ['item'], ['item'])
    assert not form.validate()

    # Content is too long
    form = make_list_form([1], ['a' * 81], ['item'])
    assert not form.validate()

    # Comment is too long
    form = make_list_form([1], ['item'], ['a' * 256])
    assert not form.validate()

    # Valid max rank and content and comment lengths
    form = make_list_form([99999], ['a' * 80], ['a' * 255])
    assert form.validate()
