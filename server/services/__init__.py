# The content of this file was generated by IBM Cloud
# Do not modify it as it might get overridden

from ibmcloudenv import IBMCloudEnv
from . import service_manager
from flask_mqtt import Mqtt
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1 
from ibm_watson import LanguageTranslatorV3
from dotenv import load_dotenv
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import os, platform

# IBMCloudEnv.init()

def initServices(app):
    # Setup MQTT
    app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
    app.config['MQTT_BROKER_PORT'] = 1883
    mqtt = Mqtt(app)
    app.config['MQTT_CLIENT'] = mqtt

    # Setup IBM Watson
    load_dotenv()
    authenticator = IAMAuthenticator(os.getenv("STT_API_KEY")) 
    service = SpeechToTextV1(authenticator=authenticator) 
    service.set_service_url(os.getenv("STT_URL"))
    app.config['SPEECH_TO_TEXT'] = service

    authenticator_translate = IAMAuthenticator(os.getenv("TRANSLATE_API_KEY")) 
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator_translate
    )
    language_translator.set_service_url(os.getenv("TRANSLATE_URL"))
    app.config['LANGUAGE_TRANSLATOR'] = language_translator

    # IBM COS
    app.config['COS_ENDPOINT'] = os.getenv("COS_ENDPOINT")
    if not app.config['COS_ENDPOINT'].startswith('http') or not app.config['COS_ENDPOINT'].startswith('https'):
           app.config['COS_ENDPOINT'] = 'https://' + app.config['COS_ENDPOINT']
           
    cos = ibm_boto3.resource("s3",
        ibm_api_key_id=os.getenv("COS_API_KEY"),
        ibm_service_instance_id=os.getenv("COS_IAM_ROLE_CRN"),
        ibm_auth_endpoint='https://iam.cloud.ibm.com/identity/token',
        config=Config(signature_version="oauth"),
        endpoint_url=app.config['COS_ENDPOINT'] 
    )
    app.config['COS'] = cos
    app.config['COS_BUCKET_NAME'] = os.getenv("COS_BUCKET_NAME")
    

    # Setup config
    # app.config['BASE'] = os.path.join(os.path.dirname(os.getcwd()),'cfc-covid-19-video-transcriber-starter') 
    app.config['BASE'] = os.path.join(os.path.dirname(os.getcwd()),'/app') 
    app.config['BASE'] = os.path.join(app.config['BASE'], 'server')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.config['BASE'], 'video_uploads')
    app.config['AUDIO_FOLDER'] = os.path.join(app.config['BASE'], 'audio_extractions')
    app.config['OUTPUT_FOLDER'] = os.path.join(app.config['BASE'], 'output_transcripts')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    return
