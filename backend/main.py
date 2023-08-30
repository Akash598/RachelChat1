# uvicorn main:app
# uvicorn main:app --reload
# get in venv source venv/bin/activate

#main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai 

#custom function imports
#...
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

#initiating the app
app = FastAPI()

# CORS - origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]

#CORS Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

#check health

@app.get("/health")
async def check_health():
    print("hhello akash")
    return {"message": "I am healthy"}


#reset messages

@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}


#get audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
#async def get_audio():

    # #get saved audio
    # audio_input = open("voice.mp3","rb")

    #save file from front end
    with open(file.filename,"wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename,"rb")

    #decode audio
    message_decoded = convert_audio_to_text(audio_input)

    #print(message_decoded)

    #guard : ensure message is decoded

    if not message_decoded:
        return HTTPException(status_code=400,detail="failed to decode audio")
    
    # get chat gpt response
    chat_response = get_chat_response(message_decoded)

    # print("check5")
    # print(chat_response)

    #guard : ensure chat response is received

    if not chat_response:
        return HTTPException(status_code=400,detail="failed to get chat response")

    #store messages
    store_messages(message_decoded,chat_response)

    #convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    # print("check4")
    # print(audio_output)

    #guard : ensure audio output is received

    if not audio_output:
        return HTTPException(status_code=400,detail="failed to get audio response from eleven labs")
    
    #create a generator that yeilds chunks of data
    def iterfile():
        yield audio_output

    #return audio file
    return StreamingResponse(iterfile(),media_type="application/octet-stream")
    #return StreamingResponse(iterfile(),media_type="audio/mpeg")

    #print(chat_response)

    #return "Done"


# #main end point post bot response
# #  note : not playig in browser when using post requests
# #

# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):
#     print("hello")



