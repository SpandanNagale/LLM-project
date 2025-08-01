import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from langchain.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchResults
import os
from dotenv import load_dotenv
from langchain.callbacks import StreamlitCallbackHandler

arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max= 200)
arxiv= ArxivQueryRun(api_wrapper=arxiv_wrapper)
wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max= 200)
wiki = WikipediaQueryRun(api_wrapper=wikipedia_wrapper)
search=DuckDuckGoSearchResults(name="search")

st.sidebar.title("settings")
api_key=st.sidebar.text_input("Enter your Groq API key:",type="password")

if "messages" not in st.session_state :
    st.session_state["messages"]=[
        {"role":"assistant", "content":"Hi,I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

if prompt:=st.chat_input(placeholder= "What is machine learning"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)
    tools=[search,arxiv,wiki]

    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)
#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 api key
