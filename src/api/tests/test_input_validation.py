from api.input_handling.input_validation import MessageHistoryItemSchema, PayloadSchema
from marshmallow import ValidationError
import pytest
import os

class TestMessageHistoryItemSchema:

    @pytest.fixture
    def valid_data(self):
        return {
            'role': 'user', 
            'content': 'Test message'
        }
    
    def test_valid_data(self, valid_data):
        result = MessageHistoryItemSchema().load(valid_data)
        assert result == valid_data

    def test_invalid_role(self, valid_data):
        with pytest.raises(ValidationError) as excinfo:
            valid_data['role'] = 'person'
            MessageHistoryItemSchema().load(valid_data)
        assert 'Must be one of' in str(excinfo.value.messages['role'])

    def test_none_content(self, valid_data):
        with pytest.raises(ValidationError) as excinfo:
            valid_data['content'] = None
            MessageHistoryItemSchema().load(valid_data)
        assert 'Field may not be null' in str(excinfo.value.messages['content'])
    
    def test_missing_content(self, valid_data):
        with pytest.raises(ValidationError) as excinfo:
            del valid_data['content']
            MessageHistoryItemSchema().load(valid_data)
        assert 'Missing data for required field' in str(excinfo.value.messages['content'])

class TestPayloadSchema:

    @pytest.fixture
    def valid_data(self):
        return {
            'user_message': 'How are you?',
            'message_history': [
                {'role': 'user', 'content': 'Hello World!'},
                {'role': 'assistant', 'content': 'Hello World!'}
            ]
        }

    def test_valid_data(self, valid_data):
        result = PayloadSchema().load(valid_data)
        assert result['user_message'] == valid_data['user_message']

    def test_user_message_max_length(self, valid_data):
        min_length = int(os.getenv('USER_MESSAGE_MIN_LENGTH', 1))
        max_length = int(os.getenv('USER_MESSAGE_MAX_LENGTH', 250))
        valid_data['user_message'] = 'a' * (max_length + 1)
        with pytest.raises(ValidationError) as excinfo:
            PayloadSchema().load(valid_data)
        assert f'Length must be between {min_length} and {max_length}' in str(excinfo.value.messages['user_message'])

    def test_missing_user_message(self, valid_data):
        del valid_data['user_message']
        with pytest.raises(ValidationError) as excinfo:
            PayloadSchema().load(valid_data)
        assert 'user_message is required' in str(excinfo.value.messages['user_message'])

    def test_invalid_message_history_item(self, valid_data):
        valid_data['message_history'][0]['role'] = 'invalid'
        with pytest.raises(ValidationError) as excinfo:
            PayloadSchema().load(valid_data)
        assert 'Must be one of' in str(excinfo.value.messages['message_history'][0]['role'])

    def test_empty_message_history(self, valid_data):
        valid_data['message_history'] = []
        result = PayloadSchema().load(valid_data)
        assert result['message_history'] == []

    def test_missing_message_history(self, valid_data):
        del valid_data['message_history']
        with pytest.raises(ValidationError) as excinfo:
            PayloadSchema().load(valid_data)
        assert 'Missing data for required field' in str(excinfo.value.messages['message_history'])
