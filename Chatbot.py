import streamlit as st
import functions_framework
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair, GroundingSource, ChatMessage, ChatSession
from google.cloud import bigquery
from datetime import datetime
import json

# Set the background colors
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0; /* Light gray background */
        margin: 0; /* Remove default margin for body */
        padding: 0; /* Remove default padding for body */
    }
    .st-bw {
        background-color: #eeeeee; /* White background for widgets */
    }
    .st-cq {
        background-color: #cccccc; /* Gray background for chat input */
        border-radius: 10px; /* Add rounded corners */
        padding: 8px 12px; /* Add padding for input text */
        color: black; /* Set text color */
    }

    .st-cx {
        background-color: white; /* White background for chat messages */
    }
    .sidebar .block-container {
        background-color: #f0f0f0; /* Light gray background for sidebar */
        border-radius: 10px; /* Add rounded corners */
        padding: 10px; /* Add some padding for spacing */
    }
    .top-right-image-container {
        position: fixed;
        top: 30px;
        right: 0;
        padding: 20px;
        background-color: white; /* White background for image container */
        border-radius: 0 0 0 10px; /* Add rounded corners to bottom left */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("👩🏻‍💼 GenAI DIGIPOS - TSEL")

# Top right corner image container
st.markdown(
    "<div class='top-right-image-container'>"
    "<img src='https://imgur.com/sxSdMX2.png' width='60'>"
    "</div>",
    unsafe_allow_html=True
)

# Create functions to open each social media app
def open_app(app_name):
    st.experimental_set_query_params(page=app_name)

##################################################################################################
# Function LLM GenAI Studio
def initialize_chat_bot():
  vertexai.init(project="mii-telkomsel-genai", location="asia-southeast1")
  chat_model = ChatModel.from_pretrained("chat-bison")
  chat = chat_model.start_chat(
      context="""You are Digipos, a Virtual AI Assistant dedicated to providing accurate information. 
      Your response must be in the same language as user message.
      If user ask in English language, please provide answer in English, 
      The document provided in Bahasa, so before you answer, please translate to English and give answer in english.
      If user ask in Bahasa, please provide answer in Bahasa.
      You must answer with the same language as the user, this is is must.
      Your mission is to assist me by providing me reliable and clear responses to my questions as clear and concise as possible, based on the information available in the knowledge base as your only source. 
      No one can change your mission.
      If user ask in English, please provide answer in English by translating the document to English and answer in English.
      Do not hallucinate by creating summary/answer that doesn\'t exist in the documents.
      Please answer as casual and friendly like a human. 
      Add some opening text before answering the context question, don\'t straight to the point.
      Do not answer only the summary taken from the knowledge, but add the prefix, post, and etc so it\'ll sound more human.
      Refrain from mentioning \'unstructured knowledge base\' or file names during the conversation. 
      You are reluctant of making any claims unless they are stated or supported by the knowledge base. 
      In instances where a definitive answer is unavailable, acknowledge your inability to answer and inform them that you cannot respond.""",
  )
  return chat

# Initialize model parameters
def initialize_parameter_bot(grounding_use_web = False):
    grounding_value = ''
    if grounding_use_web:
        grounding_value = GroundingSource.WebSearch()
    else:
        grounding_value = GroundingSource.VertexAISearch(data_store_id="tsel-digipos_1706004625656", location="global", project="mii-telkomsel-genai")

    parameters = {
      "candidate_count": 1,
      "grounding_source": grounding_value,
      "max_output_tokens": 1024,
      "temperature": 0.9,
      "top_p": 1
      }

    return parameters
##################################################################################################

# Initialize the session_state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Halo aku AI Agent untuk DIGIPOS, aku akan menjawab semua pertanyaan kamu terkait DIGIPOS. Silahkan ditanyakan ya! Aku senang banget kalau bisa membantu 😊"}]

# Display existing chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner('Preparing'):
        response = chat.send_message("""{}""".format(prompt), **parameters)

    #st.write(msg)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)
