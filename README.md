# Chat with Code 
Local chat with codebase app built using Ollama as LLM and lang chain as framework. 


## How to use 
- install **Ollama**
- pull model `deepseek-coder-v2`
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
             
            # text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
            # chunks = text_splitter.split_text(file_content)
            # file_texts.extend(chunks)

            js_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.JS, chunk_size=200, chunk_overlap=0
            )
            chunks = js_splitter.create_documents([file_content])
            file_texts.extend([chunk.page_content for chunk in chunks])            


# place this code after embeddings
vectorstore = FAISS.from_texts(file_texts, embeddings)

vectorstore.save_local("vector_store_index")


```
then when `vectorstore` is saved you can uncomment these lines, and use `vectorstore = FAISS.load_local("vector_store_index",embeddings, allow_dangerous_deserialization=True )
` normally. 
