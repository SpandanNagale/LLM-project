from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_groq import ChatGroq
import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import AIMessage,HumanMessage,SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
#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   api key

st.title("Summarizing tool")
st.sidebar.title("settings")
api_key=st.sidebar.text_input("Enter your Groq API key:",type="password")

if api_key :
    text = st.text_input("Input Text", placeholder="Enter text which needs to be summarized")
    llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)
    generictemplate="""
        Write a summary of the following text:
        text:{text}
        """
    prompt=PromptTemplate(
            input_variables=["text"],
            template=generictemplate
        )
    if text :
        llm_chain=LLMChain(llm=llm,prompt=prompt)
        summary=llm_chain.run({'text':text})
        st.write(summary)
    
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        documents=[]
        for uploaded_file in uploaded_files:
            temppdf=f"./temp.pdf"
            with open(temppdf,"wb") as file:
                file.write(uploaded_file.getvalue())
                file_name=uploaded_file.name
            
            loader=PyPDFLoader(temppdf)
            documents.extend(loader.load())
        
        
        chain=load_summarize_chain(llm=llm,chain_type='stuff',prompt=prompt,verbose=True)
        try:
         output_summary=chain.run(documents)
         st.write(output_summary)
        except:
            st.write("pdf is too big for model try different method")
            methods=["map_reduce","refine"]
            method=st.selectbox("select method", methods)
            st.write("You selected:", method)
            final_documents=RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=100).split_documents(documents)
            if method=="map_reduce":
                final_prompt='''
                Provide the final summary of the entire speech with these important points.
                Add a Motivation Title,Start the precise summary with an introduction and provide the summary in number 
                points for the speech.
                Speech:{text}

                '''
                final_prompt_template=PromptTemplate(input_variables=['text'],template=final_prompt)
                map_chain=load_summarize_chain(
                llm=llm,
                chain_type=method,
                map_prompt=prompt,
                combine_prompt=final_prompt_template,
                verbose=True
                )
                output1=map_chain.run(final_documents)
                st.write(output1)
            else:
                refine_chain=load_summarize_chain(
                    llm=llm,
                    chain_type=method,
                    verbose=True
                )
                output2=refine_chain.run(final_documents)
                st.write(output2)
