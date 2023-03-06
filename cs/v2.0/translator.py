import requests
import json

API_ENDPOINTS = [
    'https://dep.haoda7.repl.co/translate',  # API1
    'https://deep.haoda7.repl.co/translate',  # API2
    'https://deep.haoda.repl.co/translate',  # API3
]

def test_api(api_endpoint):
    try:
        payload = {
            'text': 'test',
            'source_lang': 'auto',
            'target_lang': 'EN'
        }
        response = requests.post(api_endpoint, json=payload)
        response_json = json.loads(response.text)
        result = response_json['data']
        return True
    except:
        return False

def check_apis(api_endpoints):
    for api_endpoint in api_endpoints:
        if test_api(api_endpoint):
            return api_endpoint
    raise Exception("All APIs failed to connect.")

def remote_translate(text, api_endpoint, source_lang, target_lang):
    try:
        payload = {
            'text': text,
            'source_lang': source_lang,
            'target_lang': target_lang
        }
        response = requests.post(api_endpoint, json=payload)
        response_json = json.loads(response.text)
        result = response_json['data']
        return result
    except Exception as e:
        print(f"Failed to translate using {api_endpoint}: {str(e)}")
        print(f"Response: {response.text}")
        raise e

def translate(text, target_lang):
    text = text.replace('\n', ' ')
    if target_lang == '中文':
        target_lang = 'ZH'
    elif target_lang == '英文':
        target_lang = 'EN'
    else:
        raise ValueError('Invalid target language')

    api_endpoint = check_apis(API_ENDPOINTS)
    result = remote_translate(text, api_endpoint, 'auto', target_lang)
    return result