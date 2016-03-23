# -*- coding: utf-8 -*-
import collections
from datetime import datetime
from pytest import raises
from watson.form import fields


class TestFieldMixin(object):
    def test_remove_validators(self):
        field = fields.FieldMixin(validators=[123], definition=False)
        assert len(field.validators) == 1

    def test_render_with_label(self):
        with raises(NotImplementedError):
            field = fields.FieldMixin(definition=False)
            field.render_with_label()


class TestLabel(object):

    def test_create(self):
        label = fields.Label(text='Testing')
        assert label() == '<label >Testing</label>'

    def test_update(self):
        label = fields.Label(text='Testing')
        assert label(text='Te', for_='test') == '<label for="test">Te</label>'


class TestInputField(object):

    def test_create(self):
        field = fields.Input(name='test', type='blah', definition=False)
        assert field.value is None
        assert field.name == 'test'
        assert str(field) == '<input name="test" type="blah" />'
        assert repr(field) == '<watson.form.fields.Input name:test>'

    def test_modify_label_attributes(self):
        field = fields.Input(
            name='test',
            type='text',
            label='Test',
            _class='text',
            label_attrs={'class': 'inline'},
            definition=False)
        assert field.render_with_label(
        ) == '<label class="inline" for="test">Test</label><input class="text" id="test" name="test" type="text" />'


class TestDateField(object):
    def test_create(self):
        field = fields.Date(filters=[1234], definition=False)
        assert len(field.filters) == 3

    def test_render(self):
        field = fields.Date(value=datetime.now(), definition=False)
        assert isinstance(field.render(), str)


class TestTextInputField(object):

    def test_create(self):
        field = fields.Text(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Text(name='test', definition=False)
        assert str(field) == '<input name="test" type="text" />'
        field_with_value = fields.Text(name='test', value=1, definition=False)
        assert str(
            field_with_value) == '<input name="test" type="text" value="1" />'

    def test_render_with_label(self):
        field = fields.Text(name='test', definition=False)
        assert field.render_with_label(
        ) == '<label for="test">test</label><input id="test" name="test" type="text" />'

    def test_unspecified_attribute(self):
        field = fields.Text(name='test', placeholder='Enter some data here', definition=False)
        assert str(
            field) == '<input name="test" placeholder="Enter some data here" type="text" />'


class TestPasswordInputField(object):

    def test_create(self):
        field = fields.Password(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Password(name='test', definition=False)
        assert str(field) == '<input name="test" type="password" />'
        field_with_value = fields.Password(name='test', value=1, definition=False)
        assert str(
            field_with_value) == '<input name="test" type="password" value="1" />'

    def test_render_with_label(self):
        field = fields.Password(name='test', definition=False)
        assert field.render_with_label(
        ) == '<label for="test">test</label><input id="test" name="test" type="password" />'


class TestDateInputField(object):

    def test_create(self):
        field = fields.Date(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Date(name='test', definition=False)
        assert str(field) == '<input name="test" type="date" />'
        field_with_value = fields.Date(
            name='test', value='2013-09-12', definition=False)
        assert str(
            field_with_value) == '<input name="test" type="date" value="2013-09-12" />'

    def test_render_with_label(self):
        field = fields.Date(name='test', definition=False)
        assert field.render_with_label(
        ) == '<label for="test">test</label><input id="test" name="test" type="date" />'


class TestEmailInputField(object):

    def test_create(self):
        field = fields.Email(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Email(name='test', definition=False)
        assert str(field) == '<input name="test" type="email" />'
        field_with_value = fields.Email(name='test', value=1, definition=False)
        assert str(
            field_with_value) == '<input name="test" type="email" value="1" />'

    def test_render_with_label(self):
        field = fields.Email(name='test', definition=False)
        assert field.render_with_label(
        ) == '<label for="test">test</label><input id="test" name="test" type="email" />'


class TestFileInputField(object):

    def test_create(self):
        field = fields.File(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render(self):
        field = fields.File(name='test', definition=False)
        assert str(field) == '<input name="test" type="file" />'
        field_with_value = fields.File(name='test', value=1, definition=False)
        assert str(
            field_with_value) == '<input name="test" type="file" />'

    def test_render_with_label(self):
        field = fields.File(name='test', definition=False)
        assert field.render_with_label(
        ) == '<label for="test">test</label><input id="test" name="test" type="file" />'


class TestSubmitInputField(object):

    def test_create(self):
        field = fields.Submit(name='test', definition=False)
        assert field.value == 'test'
        assert field.name == 'test'

    def test_render(self):
        field = fields.Submit(name='test', definition=False)
        assert str(field) == '<input name="test" type="submit" value="test" />'
        field_with_value = fields.Submit(name='test', value=1, definition=False)
        assert str(
            field_with_value) == '<input name="test" type="submit" value="1" />'

    def test_render_with_label(self):
        field = fields.Submit(name='test', definition=False)
        assert field.render_with_label(
        ) == '<input name="test" type="submit" value="test" />'
        field_label = fields.Submit(name='test', label='My Submit', definition=False)
        assert field_label.render_with_label(
        ) == '<input name="test" type="submit" value="My Submit" />'

    def test_render_button_mode(self):
        field = fields.Submit(name='test', button_mode=True, definition=False)
        assert str(field) == '<button name="test" type="submit">test</button>'
        field_label = fields.Submit(
            name='test',
            button_mode=True,
            label='My Submit',
            definition=False)
        assert str(
            field_label) == '<button name="test" type="submit">My Submit</button>'

    def test_render_with_label_button_mode(self):
        field = fields.Submit(name='test', button_mode=True, definition=False)
        assert field.render_with_label(
        ) == '<button name="test" type="submit">test</button>'


class TestRadioInputField(object):

    def test_create(self):
        field = fields.Radio(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render_label_wrapped_left(self):
        field = fields.Radio(name='test', definition=False)
        field_with_value_label = fields.Radio(
            name='test',
            label='My Radio',
            values=1,
            definition=False)
        field_with_value = fields.Radio(
            name='test', values=(('Test', 1),), definition=False)
        field_with_multiple_values = fields.Radio(
            name='test', label='My Radio Group',
            values=(('Test', 1), ('Testing', 2)), definition=False)
        assert str(
            field) == '<label for="test">test<input id="test" name="test" type="radio" /></label>'
        assert str(
            field_with_value_label) == '<label for="test">My Radio<input id="test" name="test" type="radio" value="1" /></label>'
        assert str(
            field_with_value) == '<label for="test">Test<input id="test" name="test" type="radio" value="1" /></label>'
        assert str(
            field_with_multiple_values) == '<label for="test_0">Test<input id="test_0" name="test" type="radio" value="1" /></label><label for="test_1">Testing<input id="test_1" name="test" type="radio" value="2" /></label>'

    def test_render_label_wrapped_right(self):
        field = fields.Radio(name='test', definition=False)
        field.label_position = 'right'
        field_with_value_label = fields.Radio(
            name='test',
            label='My Radio',
            values=1,
            definition=False)
        field_with_value_label.label_position = 'right'
        field_with_value = fields.Radio(
            name='test', values=(('Test', 1),), definition=False)
        field_with_value.label_position = 'right'
        field_with_multiple_values = fields.Radio(
            name='test', label='My Radio Group',
            values=(('Test', 1), ('Testing', 2)), definition=False)
        field_with_multiple_values.label_position = 'right'
        assert str(
            field) == '<label for="test"><input id="test" name="test" type="radio" />test</label>'
        assert str(
            field_with_value_label) == '<label for="test"><input id="test" name="test" type="radio" value="1" />My Radio</label>'
        assert str(
            field_with_value) == '<label for="test"><input id="test" name="test" type="radio" value="1" />Test</label>'
        assert str(
            field_with_multiple_values) == '<label for="test_0"><input id="test_0" name="test" type="radio" value="1" />Test</label><label for="test_1"><input id="test_1" name="test" type="radio" value="2" />Testing</label>'

    def test_render_with_wrapped_fieldset(self):
        field = fields.Radio(
            name='test', label='My Radio Group',
            values=(('Test', 1), ('Testing', 2)), definition=False)
        single_field_value = fields.Radio(
            name='test',
            label='My Radio',
            values=1,
            definition=False)
        assert field.render_with_label(
        ) == '<fieldset><legend>My Radio Group</legend><label for="test_0">Test<input id="test_0" name="test" type="radio" value="1" /></label><label for="test_1">Testing<input id="test_1" name="test" type="radio" value="2" /></label></fieldset>'
        assert single_field_value.render_with_label(
        ) == '<label for="test">My Radio<input id="test" name="test" type="radio" value="1" /></label>'

    def test_render_label_without_wrapped(self):
        field = fields.Radio(
            name='test', label='My Radio Group',
            values=(('Test', 1), ('Testing', 2)), definition=False)
        field.wrapped = False
        assert str(
            field) == '<label for="test_0">Test</label><input id="test_0" name="test" type="radio" value="1" /><label for="test_1">Testing</label><input id="test_1" name="test" type="radio" value="2" />'
        field_right = fields.Radio(
            name='test', label='My Radio Group',
            values=(('Test', 1), ('Testing', 2)), definition=False)
        field_right.wrapped = False
        field_right.label_position = 'right'
        assert str(
            field_right) == '<input id="test_0" name="test" type="radio" value="1" /><label for="test_0">Test</label><input id="test_1" name="test" type="radio" value="2" /><label for="test_1">Testing</label>'

    def test_checked_value(self):
        field = fields.Radio(
            name='test', label='My Radio Group',
            values=(('Test', 1), ('Testing', 2)), value=2, definition=False)
        assert str(
            field) == '<label for="test_0">Test<input id="test_0" name="test" type="radio" value="1" /></label><label for="test_1">Testing<input checked="checked" id="test_1" name="test" type="radio" value="2" /></label>'


class TestCheckboxInputField(object):

    def test_create(self):
        field = fields.Checkbox(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_label_position(self):
        field = fields.Checkbox(label_position='right', definition=False)
        assert field.label_position == 'right'

    def test_render_checkbox_attrs(self):
        field = fields.Checkbox(
            name='test', label='My Checkbox Group',
            values=(('Test', 1), ('Testing', 2)), definition=False)
        single_field_value = fields.Checkbox(
            name='test',
            label='My Checkbox',
            values=1,
            definition=False)
        checked_field = fields.Checkbox(
            name='test',
            label='My Checkbox',
            values=1,
            value=1,
            definition=False)
        assert str(
            field) == '<label for="test_0">Test<input id="test_0" name="test" type="checkbox" value="1" /></label><label for="test_1">Testing<input id="test_1" name="test" type="checkbox" value="2" /></label>'
        assert str(
            single_field_value) == '<label for="test">My Checkbox<input id="test" name="test" type="checkbox" value="1" /></label>'
        assert str(
            checked_field) == '<label for="test">My Checkbox<input checked="checked" id="test" name="test" type="checkbox" value="1" /></label>'

    def test_render_checkbox_multiple_values(self):
        field = fields.Checkbox(
            name='test', label='My Checkbox Group',
            values=(('Test', 1), ('Testing', 2), ('Testing Again', 3)),
            value=(1, 2), definition=False)
        assert str(field) == '<label for="test_0">Test<input checked="checked" id="test_0" name="test" type="checkbox" value="1" /></label><label for="test_1">Testing<input checked="checked" id="test_1" name="test" type="checkbox" value="2" /></label><label for="test_2">Testing Again<input id="test_2" name="test" type="checkbox" value="3" /></label>'

    def test_render_checkbox_multiple_input(self):
        field = fields.Checkbox(
            name='test[]', id='test',
            values=(('test', 1), ('testing', 2)), definition=False)
        assert str(field) == '<label for="test_0">test<input id="test_0" name="test[]" type="checkbox" value="1" /></label><label for="test_1">testing<input id="test_1" name="test[]" type="checkbox" value="2" /></label>'


class TestHiddenInputField(object):

    def test_create(self):
        field = fields.Hidden(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Hidden(name='test', definition=False)
        assert str(field) == '<input name="test" type="hidden" />'
        field_with_value = fields.Hidden(name='test', value=1, definition=False)
        assert str(
            field_with_value) == '<input name="test" type="hidden" value="1" />'

    def test_render_with_label(self):
        field = fields.Hidden(name='test', definition=False)
        assert field.render_with_label(
        ) == '<label for="test">test</label><input id="test" name="test" type="hidden" />'


class TestTextareaField(object):

    def test_create(self):
        field = fields.Textarea(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Textarea(name='test', definition=False)
        assert str(field) == '<textarea name="test"></textarea>'
        field_with_value = fields.Textarea(
            name='test', value=1, definition=False)
        assert str(field_with_value) == '<textarea name="test">1</textarea>'

    def test_render_with_label(self):
        field = fields.Textarea(name='test', label='My Test', definition=False)
        assert field.render_with_label(
        ) == '<label for="test">My Test</label><textarea id="test" name="test"></textarea>'


class TestButtonField(object):

    def test_create(self):
        field = fields.Button(name='test', definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Button(name='test', definition=False)
        assert str(field) == '<button name="test">test</button>'
        field_with_value = fields.Button(
            name='test', value=1, definition=False)
        assert str(
            field_with_value) == '<button name="test" value="1">test</button>'

    def test_render_with_label(self):
        field = fields.Button(name='test', label='My Test', definition=False)
        assert field.render_with_label(
        ) == '<button name="test">My Test</button>'


class TestSelectField(object):

    def test_create(self):
        field = fields.Select(name='test', options=[], definition=False)
        assert field.value is None
        assert field.name == 'test'

    def test_render_no_options(self):
        field = fields.Select(name='test', options=[], definition=False)
        assert str(field) == '<select name="test"></select>'

    def test_render_options_list(self):
        field = fields.Select(name='test', options=[1, 2, 3], definition=False)
        assert str(
            field) == '<select name="test"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select>'
        field_with_value = fields.Select(
            name='test', options=[1, 2, 3], value=2, definition=False)
        assert str(
            field_with_value) == '<select name="test"><option value="1">1</option><option value="2" selected="selected">2</option><option value="3">3</option></select>'
        field_with_key_value = fields.Select(
            name='test', options=[(1, 'Test'), (2, 'Testing')], definition=False)
        assert str(
            field_with_key_value) == '<select name="test"><option value="1">Test</option><option value="2">Testing</option></select>'

    def test_render_options_dict(self):
        field = fields.Select(
            name='test', options={'Test': 'Value'}, definition=False)
        assert str(
            field) == '<select name="test"><option value="Value">Test</option></select>'

    def test_render_with_label(self):
        field = fields.Select(name='test', label='My Test', definition=False)
        assert field.render_with_label(
        ) == '<label for="test">My Test</label><select id="test" name="test"></select>'

    def test_single_value(self):
        field = fields.Select(
            name='test', value=1, options=[1, 2, 3, 4], definition=False)
        assert str(
            field) == '<select name="test"><option value="1" selected="selected">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select>'
        field = fields.Select(
            name='test', value='1', options=[1, 2, 3, 4], definition=False)
        assert str(
            field) == '<select name="test"><option value="1" selected="selected">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select>'

    def test_multiple_values(self):
        field = fields.Select(
            name='test', value=(1, 2), options=[1, 2, 3, 4], definition=False)
        assert str(
            field) == '<select multiple="multiple" name="test"><option value="1" selected="selected">1</option><option value="2" selected="selected">2</option><option value="3">3</option><option value="4">4</option></select>'
        field = fields.Select(
            name='test', value=('1', 2), options=[1, 2, 3, 4], definition=False)
        assert str(
            field) == '<select multiple="multiple" name="test"><option value="1" selected="selected">1</option><option value="2" selected="selected">2</option><option value="3">3</option><option value="4">4</option></select>'

    def test_optgroup(self):
        field = fields.Select(name='test', options=collections.OrderedDict(
            [('Group One', [1, 2]), ('Group Two', [3, 4])]), definition=False)
        assert str(
            field) == '<select name="test"><optgroup label="Group One"><option value="1">1</option><option value="2">2</option></optgroup><optgroup label="Group Two"><option value="3">3</option><option value="4">4</option></optgroup></select>'
        field_with_key_value = fields.Select(
            name='test',
            options=collections.OrderedDict(
                [('Group One', [(1, 'Test'),
                                (2, 'Testing')]),
                 ('Group Two', [3, 4])]),
            definition=False)
        assert str(
            field_with_key_value) == '<select name="test"><optgroup label="Group One"><option value="1">Test</option><option value="2">Testing</option></optgroup><optgroup label="Group Two"><option value="3">3</option><option value="4">4</option></optgroup></select>'
