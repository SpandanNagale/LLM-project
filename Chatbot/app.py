import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

import os 
from dotenv import load_dotenv
load_dotenv()


os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_PROJECT_NAME']="Debugging Chatbot"

prompts=ChatPromptTemplate.from_messages(
    [
        ("system","hey you have been very helpful for coding so please help user with this code , first understand the full code given by the user and then see what the what is the error provided by user and solve this error to your fullest capacity "),
        ("user", "full code : {code}"),
        ("user", "error : {error}")

    ]
)

def generate_response(code,error,engine,temperature):
    llm=OllamaLLM(model=engine)
    output_parser=StrOutputParser()
    chain=prompts|llm|output_parser
    answer=chain.invoke({'code': code, 'error': error})
    return answer

st.title("Debugging Chatbot ")


## Select the OpenAI model
llm=st.sidebar.selectbox("Select Open Source model",["gemma3","deepseek-r1"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)


## MAin interface for user input
st.write("Goe ahead give your full code and error")
code = st.text_area("Paste your full code here:")
error = st.text_area("Paste the error you're getting:")





if st.button("Submit"):
    try:
        if code and error:
            response = generate_response(code, error, llm, temperature)
            st.subheader("💡 Suggested Fix:")
            st.write(response)
    except Exception as e:
        st.error(f"Something went wrong: {e}")

