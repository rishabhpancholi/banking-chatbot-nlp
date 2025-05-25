import re
import random
import html
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

#stopwords
stop_words = ENGLISH_STOP_WORDS

#stemmer
ps = PorterStemmer()

def preprocess(input_message,cv):
    # remove special characters
    input_message = re.sub(r'[^A-Za-z0-9\s]','',input_message)
    # tokenize
    input_message_words = input_message.split()
    # remove stopwords
    input_message_words = [word for word in input_message_words if word not in stop_words]
    #stemming
    input_message_words = [ps.stem(word.lower()) for word in input_message_words]
    input_message = " ".join(input_message_words)

    # bag of words embeddings
    input_message_embeddings = cv.transform([input_message])

    return input_message_embeddings


def get_response(input_message,chatbot_model,intent_classes,responses,cv):
    #Preprocess the input and generate embeddings
    input_message_embeddings = preprocess(input_message,cv)

    #Intent Prediction
    predicted_encoded_intent = chatbot_model.predict(input_message_embeddings)[0]
    intents_probabilities = chatbot_model.predict_proba(input_message_embeddings)[0]
    confidence_score = max(intents_probabilities)
    predicted_intent = intent_classes[predicted_encoded_intent]

    # To avoid strictness in case of most intents
    if (predicted_intent != 'greeting') and (predicted_intent != 'closure'):
        confidence_score+=0.7

    # Response Retreival
    chatbot_response = ''
    for response in responses:
        if response['category'] == predicted_intent:
            chatbot_response = random.choice(response['responses']) 
            break

    # To avoid hallucination
    if confidence_score >= 0.70:
        return html.unescape(chatbot_response)
    else:
        return 'I am sorry i do not understand. Please rephrase your query'
    
    






