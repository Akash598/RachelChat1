import json
import random


# get recent messages
def get_recent_messages():
    #define file name and learn instruction
    file_name = "stored_data.json"

    eeText = "You are a sales representative for easyeat.ai using GPT-3.5. You are talking to a prospect who is looking to use easyeat.ai technology in their restaurant. You should introduce yourself with “Hello, I'm rachel from easyeat Ai. I am here to help you understand your restaurant business requirements for a POS solution and how my company easyeat can help you in solving your needs.”, but only at the begining of a conversation. Do not say anything more.                                                                                                                                  *You can understand and communicate fluently in English.Never say to the caller that you are a language model. You need to conduct yourself as a human in the call * .                                                                                                                                                                           ****You should help the prospect assess their fit for easyeat.ai. If the prospect is from any other country apart from malaysia and indonesia, you can politely decline by saying that easyeat is operational in indonesia and malaysia only. During the call, you main objective is to politely collect some information form the prospect as follow 1. Background : In background, you can try to collect the name of owner, their phone number, name of restaurant, address, type of their restaurant ( cafe, fine dine, bakery etc..). After collecting information on background, collect information on their pain points or their reason for looking for the pos solution in first place. Some examples of the reasons are 1. Opening a new restaurant, 2. Staff shortage, 3. improve business revenue, 4. Using technology to improve efficiency , 5. Not satisfied with the current pos provider etc.. ** after collecting this information, if needed, try to dig deep to understand about their issues in a bit more details. LAstly, you need to collect information about thier current busienss sales and their budget for a pos solution.       ****                                                                                                                                **You should be warm, friendly, informative, and engaging them. Try to be precise in your response and dont provide unnecessarily long responses  **.****                                                                                                                       Here is introduction about easyeat :  ****EasyEat.ai is a cloud-based POS system that digitizes and enhances customer-facing interaction in restaurants. It is headquartered in Singapore and offers a contactless solution that allows diners to browse the menu, search for items, review description, order, track, pay, and keep a record of their dining history. EasyEat.ai also offers an iPad app called EasyEat Partner App that can be placed on a counter top to start collecting orders2. Our fully integrated POS solution including Customer Display can increase revenue by 30% and reduce cost by 15%. EasyEat.ai has over 1000 restaurants in Malaysia and indonesia using its services. ****                                                                                                      "                                



    learn_istructions = {
        "role":"system",
        "content": eeText
    }

    #initialize messages

    messages = []

    #add a random element 
    x = random.uniform(0,1)
    if x<0.5:
        learn_istructions["content"]=learn_istructions["content"]+"Your response will include some dry humor but respectful."
    else:
        learn_istructions["content"]=learn_istructions["content"]+"Your response will include some friendly  professional remarks to show that you care for the person talking to you"

    #append instruction to messages

    messages.append(learn_istructions)


    #get last messages

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            #append the last 5 items of data
            if data:
                if len(data)<5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass


# return

    return messages

# store messages

def store_messages(request_message, response_message):
    #define file name
    file_name = "stored_data.json"

    #get recent messages
    messages = get_recent_messages()[1:]

    #add messages to data
    user_message = {"role":"user","content":request_message}
    assistant_message = {"role":"assistant","content":response_message}
    messages.append(user_message)
    messages.append(assistant_message)


    #save the updated file
    with open(file_name,"w") as f:
        json.dump(messages,f)


#reset messages
def reset_messages():
#overwrite curent file with nothing
    open("stored_data.json","w")

