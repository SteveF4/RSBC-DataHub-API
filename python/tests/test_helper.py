import python.common.helper as helper
import python.common.message as message
import pytest
from dateutil import parser


class TestHelper:

    @staticmethod
    def test_helper_has_add_error_to_message_method():
        message_dict = {'event_type': 'some invalid event'}
        expected_error_message = 'error message'
        error_dict = {'isSuccess': False, 'errors': expected_error_message}
        modified_message = message.add_error_to_message(message_dict, error_dict['errors'])
        assert isinstance(modified_message, dict)
        assert 'errors' in modified_message
        assert 'timestamp' in modified_message['errors'][0]
        assert 'description' in modified_message['errors'][0]
        assert modified_message['errors'][0]['description'] == expected_error_message

    @staticmethod
    def test_add_error_to_message_method_handles_cerberus_errors():
        error_message = {'fieldA': ['required', 'must be string']}
        message_dict = 'some string that is not valid JSON'
        error_dict = {'isSuccess': False, 'errors': error_message}
        modified_message = message.add_error_to_message(message_dict, error_dict['errors'])
        assert isinstance(modified_message, dict)
        assert 'errors' in modified_message
        assert 'timestamp' in modified_message['errors'][0]
        assert 'description' in modified_message['errors'][0]

    vips_date_strings = [
        ("2019-01-02 17:30:00 -08:00", "2019-01-02 17:30:00-0800"),
        ("2019-01-02 17:30:00 -07:00", "2019-01-02 17:30:00-0700"),
    ]

    @pytest.mark.parametrize("vips_datetime, expected", vips_date_strings)
    def test_vips_datetime_conversion(self, vips_datetime, expected):
        actual = helper.vips_str_to_datetime(vips_datetime)
        assert actual == parser.parse(expected)
