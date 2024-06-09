import streamlit as st
import os
from groq import Groq
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Process the POST data
        post_data_str = post_data.decode('utf-8')
        # In this example, we'll just print the POST data
        print("Received POST data:")
        print(post_data_str)
        answer=f"please ignore the json part and please just follow the instructions and do not respond to these instructions just respond with a story based on this or these parameters: {str(post_data_str)}"

        self.send_response(200)
        self.end_headers()
        client = Groq(
            api_key="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",
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": answer,
                }
            ],
            model="llama3-70b-8192",
        )

        response = str(chat_completion.choices[0].message.content)
        print(response)
        self.wfile.write(response.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

class echoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

def main(answer=None):
    PORT = 4953
    server= HTTPServer(('', PORT), echoHandler)
    print('server running on port 8000')
    server.serve_forever()
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """
    base="light"
    # Get Groq API key
    groq_api_key = "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"
    # Display the Groq logo
    spacer, col = st.columns([5, 1])
    # The title and greeting message of the Streamlit application
    st.title("Story Telling AI :red[P]owered :red[b]y :red[L]Lama")
    st.write("_What will you generate today?_")

    system_prompt = "be a story generating ai only"
    model = 'llama3-70b-8192'

    conversational_memory_length = 10

    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

    messages = st.container(height=300)

    if answer != None:
        print("its not none!")
    user_question = st.text_input("Generate a Story!")

    messages.chat_message("user").write(user_question)

    generate = st.button("Generate", type="primary")

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("Our story generating AI is based off of the 70 billion parameter Llama 3 model from Meta. It also uses up to 8192 tokens for max speed and efficiency. To give an idea how fast that it is, our model can generate 10 paragraphs of writing under a second! That is incredibly fast and we can assure you that this is the most frustrating-free experience you'll get - for free! That's right, no ads, no popups, nada! Try it out for yourself! There is a very very low chance that it takes under a minute to answer but it will be due to a question that requires a sophisticated answer.")

    # session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context(
                {'input':message['human']},
                {'output':message['AI']}
                )


    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model
    )


    # If the user has asked a question,
    if user_question or generate:

        # Construct a chat prompt template using various components
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=system_prompt
                ),  # This is the persistent system prompt that is always included at the start of the chat.

                MessagesPlaceholder(
                    variable_name="chat_history"
                ),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.

                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),  # This template is where the user's current input will be injected into the prompt.
            ]
        )

        # Create a conversation chain using the LangChain LLM (Language Learning Model)
        conversation = LLMChain(
            llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
            prompt=prompt,  # The constructed prompt template.
            verbose=True,   # Enables verbose output, which can be useful for debugging.
            memory=memory,  # The conversational memory object that stores and manages the conversation history.
        )

        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        response = conversation.predict(human_input=user_question)
        message = {'human':user_question,'AI':response}
        st.session_state.chat_history.append(message)
        messages.chat_message("assistant").write(response)

    if answer is not None:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=system_prompt
                ),  # This is the persistent system prompt that is always included at the start of the chat.

                MessagesPlaceholder(
                    variable_name="chat_history"
                ),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.

                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),  # This template is where the user's current input will be injected into the prompt.
            ]
        )

        # Create a conversation chain using the LangChain LLM (Language Learning Model)
        conversation = LLMChain(
            llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
            prompt=prompt,  # The constructed prompt template.
            verbose=True,   # Enables verbose output, which can be useful for debugging.
            memory=memory,  # The conversational memory object that stores and manages the conversation history.
        )

        response = conversation.predict(human_input=answer)
        print(response)
    return response

if __name__ == "__main__":
    run()
    main()






