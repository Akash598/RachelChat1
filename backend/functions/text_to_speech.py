import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

#eleven labs
#convert text to speech

def convert_text_to_speech(message):

    # print("check1")
    # print(message)

#define data (body)

    body= {
        "text":message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0,
            "use_speaker_boost": "true"
        }
    }
    # print("check2")
    # print(body)


#define voice
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"

    #constructing headers and endpoints

    headers = {"xi-api-key" : ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept":"audio/mpeg"}

    # print("check3")
    # print(headers)
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    #send request

    try:
        response = requests.post(endpoint,json=body,headers=headers)

    except Exception as e:
        return
    
    #handle response

    if response.status_code==200:
        print("it worked")
        return response.content
    else:
        print("it did not work")
        return