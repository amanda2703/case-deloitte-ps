from marshmallow import Schema, fields, validate
import os

class MessageHistoryItemSchema(Schema):
    role = fields.String(
        required = True, 
        validate = validate.OneOf(['user', 'assistant']))
    content = fields.String(required = True, allow_none = False)

class PayloadSchema(Schema):
    
    user_message = fields.String(
        required = True,
        validate = validate.Length(
            min = int(os.getenv('USER_MESSAGE_MIN_LENGTH', 1)),
            max = int(os.getenv('USER_MESSAGE_MAX_LENGTH', 250))
        ),
        error_messages = {
            'required': 'user_message is required',
            'invalid': 'Invalid user_message'
        }
    )
    message_history = fields.List(
        fields.Nested(MessageHistoryItemSchema),
        required = True
    )
