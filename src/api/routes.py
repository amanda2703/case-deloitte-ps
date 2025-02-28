from api.input_handling.input_validation import PayloadSchema
from api.services.genai.genai_service import GenAIService
from flask import request, make_response, jsonify

def chatbot():
    
    try:

        data = PayloadSchema().load(request.get_json())

        genai_service = GenAIService()
        result = genai_service.process(data)

        if 'error_message' in result:
            return make_response(jsonify(result), 400)    

        return make_response(jsonify(result), 200) 
    
    except Exception as e:
        error_message = f'Uma exceção do tipo {type(e)} foi lançada. Exceção: {e}'
        result = {'error_message': error_message}
        return make_response(jsonify(result), 400) 

def configure_routes(app):
    app.add_url_rule('/api/v1/chatbot', 'chatbot', chatbot, methods=['POST'])