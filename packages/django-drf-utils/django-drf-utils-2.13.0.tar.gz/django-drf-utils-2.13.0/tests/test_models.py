import pytest
from django.core import exceptions

from django_drf_utils.models import NameField, CodeField


class TestModels:
    name_field = NameField()
    lower_code_field = CodeField()
    upper_code_field = CodeField(lower=False)

    def test_creation(self):
        CodeField()
        code_field = CodeField(lower=False)
        assert code_field.unique
        code_field = CodeField(lower=True, unique=False)
        assert not code_field.unique
        name_field = NameField()
        assert name_field.unique
        name_field = NameField(unique=False)
        assert not name_field.unique

    @pytest.mark.parametrize("value", ("", "name", "'new'-'name'", "new_name"))
    def test_name_field_validation(self, value):
        self.name_field.run_validators(value)

    @pytest.mark.parametrize("value", ("", "name", "new_code"))
    def test_lower_code_field_validation(self, value):
        self.lower_code_field.run_validators(value)

    @pytest.mark.parametrize("value", ("NAME",))
    def test_lower_code_field_validation_failing(self, value):
        with pytest.raises(exceptions.ValidationError) as e:
            self.lower_code_field.run_validators(value)
        assert e.value.args[0][0].message == 'Allowed characters: "a-z", "0-9", "_"'

    @pytest.mark.parametrize("value", ("", "NAME", "NEW_CODE"))
    def test_upper_code_field_validation(self, value):
        self.upper_code_field.run_validators(value)

    @pytest.mark.parametrize("value", ("name",))
    def test_upper_code_field_validation_failing(self, value):
        with pytest.raises(exceptions.ValidationError) as e:
            self.upper_code_field.run_validators(value)
        assert e.value.args[0][0].message == 'Allowed characters: "A-Z", "0-9", "_"'
