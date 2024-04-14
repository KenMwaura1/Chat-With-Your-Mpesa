#Definin the app to run the front End
import streamlit as st
import datetime as dt
import pandas as pd
import plotly.express as px
import requests
from pdf_parser import pdf_parser,pdf_decrypt


#Defining the main function:
def main():
    st.set_page_config("Chatting with Mpesa")
    st.title("💬 Chat with Your Mpesa Statements:📊")

    #Decrpyt variable
    #Side Menu Bar
    with st.sidebar:
        st.title("🛠️ Configuration:⚙️")
        #Activating Demo Data
        st.text("Turn on to use demo data")
        demo_on = st.toggle("Use demo data: 📈")

    if demo_on:
        #impprting the demo data:
        df = pd.read_csv("Demo_Data/mpesa_demo_data.csv")
        st.text("Here are your transactions!💵")
        st.dataframe(df)
        chat_window(df)
    
    #Other option
    else:
        #Sidebar
        #Side Menu Bar
        with st.sidebar:
            st.text("Use your Mpesa Statement: 📝")
            pdf_file = st.file_uploader("Upload your Mpesa Statement",accept_multiple_files=False)
            pdf_password = st.text_input("Enter File password",type='password')
            #pdf_path = "\mpesa_statement_v2.pdf"
            if st.button("Submit & Process"):
                with st.spinner("Processing..."):
                    try:
                        pdf_decrypt(pdf_file=pdf_file,pdf_password=pdf_password)
            
                        st.success("Done")
        
                    except Exception as e:
                        st.error("Failed to decrypt the PDF. Please check you've uploaded your statement and entered the correct password.")
  
    #Loading the dataframe
    try:
        if pdf_file and pdf_password:
            df = pdf_parser(pdf_file=pdf_file,pdf_password=pdf_password)
            st.text("Here are your transactions!💵")
            st.dataframe(df)
            chat_window(df)
        else:
            st.code("Get Started by uploading your Mpesa Statement!")
    except Exception as e:
        print("Failed to decrypt the PDF. Please check you've uploaded your statement and entered the correct password.")

#Defining the function to Initialise the Chat Window
def chat_window(df):
    #Chat Window
    with st.chat_message("assistant"):
        st.write("What do you want to find out about your transactions today?🧐")

    #Initilizing message history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    #Displaying the message history on re-reun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            #priting the questions
            if 'question' in message:
                st.markdown(message["question"])
            #printing the code generated and the evaluated code
            elif 'code' in message:
                st.code(message['code'])
                st.write(eval(message['code']))
            #retrieving error messages
            elif 'error' in message:
                st.text(message['error'])
            

    #Getting the questions from the users
    user_question = st.chat_input("What would you like to find out about your Mpesa Transactions? ")

    if user_question:
        #Displaying the user question in the chat message
        with st.chat_message("user"):
            st.markdown(user_question)
        #Adding user question to chat history
        st.session_state.messages.append({"role":"user","question":user_question})
        
        
        try:           
            #Getting response from the API end-point
            response = requests.post("https://chat-pesa.onrender.com/generate_response", json={"question": user_question})
            
            #checking if the response from the server is successful
            if response.status_code == 200:
                #extracting the code from the JSON response
                code = response.json()["code"]
                st.code(code)
                st.write(eval(code))
            #Adding the assistant response to chat history
            st.session_state.messages.append({"role":"assistant","code":code})
        
        except Exception as TypeError:
            st.write(TypeError)
            error_message = "⚠️Error Occured! Please Submit & Process your Mpesa Statement first!"
            #Displaying the error message
            with st.chat_message("assistant"):  
                st.error(error_message)

            #Appending the error messaage to the session
            st.session_state.messages.append({"role":"assistant","error":error_message})
        
        
        except Exception as NameError:
            st.write(NameError)
            error_message = "⚠️Error Occured! Please Submit & Process your Mpesa Statement first!"
            #Displaying the error message
            with st.chat_message("assistant"):  
                st.error(error_message)

            #Appending the error messaage to the session
            st.session_state.messages.append({"role":"assistant","error":error_message})
        
        
        except Exception as e:
            st.write(e)
            error_message = "⚠️Error occured while fetching response from the server!"
            #Displaying the error message
            with st.chat_message("assistant"):  
                st.error(error_message)

            #Appending the error messaage to the session
            st.session_state.messages.append({"role":"assistant","error":error_message})
    
    
    #Function to clear history
    def clear_chat_history():
        st.session_state.messages = []
    #Button for clearing history
    st.sidebar.text("Click to Clear Chat history")
    st.sidebar.button("CLEAR 🗑️",on_click=clear_chat_history)
    #st.sidebar.image("Documents\mpesa_img.png")


if __name__ == "__main__":
    main()

