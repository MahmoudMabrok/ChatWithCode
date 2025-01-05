# Chat with Code 
Local chat with your local git based repository, built using Ollama, HuggingFaceEmbeddings, LangChain. 


## Introduction 
This project provides ready to use chat with already codebase that was locally on machine, so it is readt to run and use. To use it please update knowledge base with your repo then run it again. 

## Why this project? 
I needed to have ability to chat with my private repo (suitable for company that seek privacy) so i developed this app. 


## Demo 
As example i used next [repo](https://github.com/MahmoudMabrok/QuranyApp) as knowledge base and result : 
![Screenshot 2025-01-05 at 3 31 19 PM](https://github.com/user-attachments/assets/5341074a-a535-4ba7-a8ee-852744bfac22)


## How to use 
- install **[Ollama](https://ollama.com)**
- pull model `deepseek-coder-v2` using `ollama pull deepseek-coder-v2:16b`
- install python 3.11
- run `pip3 install -r requirements.txt`
- run `python3.11 -m streamlit app.py`

## Update Knowledge base 
To update KB we need to chunck codebase and make embededings then save to **FAISS**

you need to add next snippits(let's assume codebase is JS based project): 

```python
# path to local git repo
repo_path = "./project/"
repo = Repo(repo_path)

# Extract text from the repository
file_texts = []
for file in repo.tree().traverse():
    if file.type == "blob":
        if file.name.endswith((".js", ".tsx", ".jsx")):  # Handle JavaScript files
            file_content = file.data_stream.read().decode("utf-8")

            js_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.JS, chunk_size=200, chunk_overlap=0
            )
            chunks = js_splitter.create_documents([file_content])
            file_texts.extend([chunk.page_content for chunk in chunks])            


# place this code after embeddings
vectorstore = FAISS.from_texts(file_texts, embeddings)

vectorstore.save_local("vector_store_index")


```
then when `vectorstore` is saved you can comment above lines, and use: 
```python
vectorstore = FAISS.load_local("vector_store_index",embeddings, allow_dangerous_deserialization=True )
```

# Inspiration
I have inspired from many projects, but i did not get what i want exactly. 
- [chat_with_github](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/chat_with_X_tutorials/chat_with_github)
- [QA-Pilot](https://github.com/reid41/QA-Pilot)

