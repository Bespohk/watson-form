# -*- coding: utf-8 -*-
from io import BytesIO, BufferedReader
from pytest import raises
from watson.form import Form, Multipart
from watson.http.messages import Request
from tests.watson.form.support import (LoginForm, UploadForm, User, MultipleForm,
                                       form_user_mapping, Contact, Other,
                                       sample_environ, ProtectedForm,
                                       SampleFormValidator, environ_with_file,
                                       ValuesProvider, FieldTypeForm,
                                       FieldTypeObject)


class TestForm(object):

    def test_form_create(self):
        form = Form('test')
        assert len(form) == 0
        assert len(form.fields) == 0
        assert repr(
            form) == '<watson.form.types.Form name:test method:post action:/ fields:0>'
        form2 = LoginForm('test')
        assert len(form2) == 5

    def test_class_attribute(self):
        form = Form(_class='test')
        assert form.open() == '<form action="/" class="test" enctype="application/x-www-form-urlencoded" method="post" name="Form">'

    def test_form_create_no_name(self):
        form = Form()
        assert form.name == 'Form'
        login_form = LoginForm()
        assert login_form.name == 'LoginForm'

    def test_form_start_tag(self):
        form = Form('test')
        assert form.open(
        ) == '<form action="/" enctype="application/x-www-form-urlencoded" method="post" name="test">'

    def test_form_end_tag(self):
        form = Form('test')
        assert form.close() == '</form>'

    def test_set_data_on_form(self):
        form = LoginForm('test')
        post_data = {
            'username': 'simon',
            'password': 'test',
            'first_name': None,
            'last_name': None,
            'email': None}
        form.data = post_data
        assert form.data == post_data
        environ = environ_with_file()
        request = Request.from_environ(environ)
        form.data = request
        assert form.data['first_name'] == '1234'

    def test_bind_object_to_form_with_mapping(self):
        form = LoginForm('test')
        user = User(username='simon', password='test')
        user.personal.first_name = 'Simon'
        user.personal.contact.email = 'simon.coulton@gmail.com'
        form.bind(user, form_user_mapping)
        assert form.username == 'simon'
        assert form.first_name == 'Simon'
        assert form.email == 'simon.coulton@gmail.com'
        assert form.password == 'test'
        form.data = {'password': 'newpass'}
        assert form.password == 'newpass'

    def test_hydrate_form_to_object_with_mapping(self):
        form = LoginForm('test')
        form.data = {
            'username': 'simon',
            'password': 'test',
            'email': 'simon.coulton@gmail.com'}
        user = User()
        form.bind(user, form_user_mapping, hydrate=False)
        form.is_valid()
        assert user.username == 'simon'
        assert user.password == 'test'
        assert user.personal.contact.email == 'simon.coulton@gmail.com'

    def test_bind_object_to_form_without_mapping(self):
        form = LoginForm('test')
        user = User(username='simon', password='test')
        form.bind(user)
        assert form.username == 'simon'
        assert form.password == 'test'
        form.data = {'password': 'newpass'}
        assert form.password == 'newpass'

    def test_hydrate_form_to_object_without_mapping(self):
        form = LoginForm('test')
        form.data = {'username': 'simon', 'password': 'test'}
        user = User()
        form.bind(user, hydrate=False)
        form.is_valid()
        assert user.username == 'simon'
        assert user.password == 'test'

    def test_hydrate_form_to_object_with_mapping_invalid_class(self):
        with raises(AttributeError):
            form = LoginForm('test')
            form.data = {'username': 'simon', 'password': 'test'}
            user = Contact()  # obviously not a user
            form.bind(user, {'username': ('firstname', 'test')}, hydrate=False)
            form.is_valid()

    def test_hydrate_object_with_mapping_invalid_class(self):
        with raises(AttributeError):
            form = LoginForm('test')
            user = Other()
            user.test = 'test'
            form.bind(user, {'username': ('blah', 'field')})

    def test_alter_form_multipart(self):
        form = UploadForm('test')
        assert form.enctype == 'multipart/form-data'

    def test_setting_raw_data(self):
        form = LoginForm('test')
        data = {'username': 'simon'}
        expected_data = {
            'first_name': None,
            'last_name': None,
            'password': None,
            'username': 'simon',
            'email': None}
        form.data = data
        assert form.username == 'simon'
        assert form.data == expected_data
        assert form.raw_data == expected_data

    def test_filter_and_validate_input(self):
        form = LoginForm('test')
        data = {'username': 'simon '}
        form.data = data
        form.is_valid()
        assert form.username == 'simon'
        assert form.fields['username'].original_value == 'simon '
        assert form.errors == {
            'password': {
                'messages': [
                    'Value is required'],
                'label': 'password'}}

    def test_validate_form_success(self):
        form = LoginForm(validators=[SampleFormValidator()])
        form.data = {'username': 'Simon', 'password': 'Test'}
        valid = form.is_valid()
        assert valid

    def test_validate_form_invalid(self):
        form = LoginForm(validators=[SampleFormValidator()])
        form.data = {'username': 'Simone', 'password': 'test'}
        valid = form.is_valid()
        assert not valid
        assert form.errors == {'form': {'messages': ['Username does not match.'], 'label': 'Form'}}

    def test_render_entire_form(self):
        form = LoginForm('test')
        rendered_form = str(form)
        assert rendered_form == '<form action="/" enctype="application/x-www-form-urlencoded" method="post" name="test"><div><label for="username">username</label><input id="username" name="username" required="required" type="text" /></div><div><label for="password">password</label><input id="password" name="password" required="required" type="password" /></div><div><label for="first_name">first_name</label><input id="first_name" name="first_name" type="text" /></div><div><label for="last_name">last_name</label><input id="last_name" name="last_name" type="text" /></div><div><label for="email">email</label><input id="email" name="email" type="text" /></div></form>'

    def test_custom_method(self):
        form = LoginForm('test', method='PUT')
        assert form.http_request_method == 'PUT'
        assert form.close(
        ) == '<input name="HTTP_REQUEST_METHOD" type="hidden" value="PUT" /></form>'

    def test_ignored_fields(self):
        form = LoginForm('test')
        user = User()
        form.bind(user, ignored_fields=('username',))
        form.data = {'username': 'should be ignored', 'password': 'test'}
        form.is_valid()
        assert not form.username
        assert form.password

    def test_multiple_values(self):
        form = MultipleForm('test')
        data = 'checkbox[]=1&checkbox[]=2'
        environ = sample_environ(
            REQUEST_METHOD='POST',
            CONTENT_LENGTH=len(data))
        environ['wsgi.input'] = BufferedReader(
            BytesIO(data.encode('utf-8')))
        request = Request.from_environ(
            environ, 'watson.http.sessions.Memory')
        form.data = request
        assert form.test == ['1', '2']

    def test_values_provider(self):
        form = MultipleForm('test', values_provider=ValuesProvider())
        assert len(form.fields['test'].values) == 2


class TestMultiPartForm(object):

    def test_multi_part(self):
        form = Multipart('test')
        assert form.enctype == 'multipart/form-data'

    def test_form_start_tag(self):
        form = Multipart('test')
        assert form.open(
        ) == '<form action="/" enctype="multipart/form-data" method="post" name="test">'
        assert form.open(action='/put') == '<form action="/put" enctype="multipart/form-data" method="post" name="test">'


class TestFormProcessingCsrfRequest(object):

    def setup(self):
        data = 'form_csrf_token=123456&test=blah'
        environ = sample_environ(
            HTTP_COOKIE='watson.session=123456;',
            REQUEST_METHOD='POST',
            CONTENT_LENGTH=len(data))
        environ['wsgi.input'] = BufferedReader(
            BytesIO(data.encode('utf-8')))
        self.request = Request.from_environ(
            environ, 'watson.http.sessions.Memory')

    def teardown(self):
        self.request.session.destroy()
        del self.request

    def test_valid_csrf_token(self):
        self.request.session['form_csrf_token'] = '123456'
        form = ProtectedForm('form', session=self.request.session)
        form.data = self.request
        valid = form.is_valid()
        assert valid

    def test_invalid_csrf_token(self):
        form = ProtectedForm('form', session=self.request.session)
        form.data = self.request
        valid = form.is_valid()
        assert not valid


class TestMultipleInputTypes(object):

    def test_value_types(self):
        form = FieldTypeForm()
        form.data = {
            'checkbox': 3,
            'radio': 3,
            'select': 'test',
            'select_multiple': ['test', 'testing'],
            'radio_enum': 'red',
            'text': None
        }
        assert form.checkbox == [3]
        assert form.radio == 3
        assert form.select == 'test'
        assert form.select_multiple == ['test', 'testing']
        assert form.text == 'Test'
        assert form.radio_enum == 'red'
        assert '<input checked="checked" id="radio_enum_0"' in str(form.fields['radio_enum'])


class TestMultipleInputTypesBind(object):

    def test_value_types(self):
        form = FieldTypeForm()
        form.bind(FieldTypeObject())
        assert form.text == 'Test'
        assert form.radio == 'test'
        assert form.checkbox == [1, 2]
        assert form.checkbox_multi == [1]
        assert form.radio_enum == 'red'
