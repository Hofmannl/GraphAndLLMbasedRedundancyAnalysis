# RedundancyAndConflictAnalysis

## Goal Definition
    - Main Part and Benefit analyse
    - Main Part: alles was nicht der Benefit ist
    - Benefit: the outcome of the action
    - In the first analyse we did not consider the annotations to keep the context as minimal as possible 
    - We wanted to compare the output with and without annotations === where same and where different
    - Just looked if the redundancies where discovered --> later one we could look deeper if the same count would be discovered
    - We could have with the Metrix just a rather binary decision but not human like thus we had a deeper look in the concreted differens
    - False positives are better as falls negatives as a human can look at them both other way around would be rather time consumeing

### Steps
    - Different abstractions redundant 0/1 full 0/1 partial 0/1
    - Do in future work just plain text and then non processed jsons
    - [] Using word net alown and combination with the graph approach
    - [] Using Gemini 
    - [] Using open sourc model like LLAMA from meta on MaRC3a https://www.uni-marburg.de/de/hrz/dienste/hochleistungsrechnen
    - [] Write an interface for batch processing https://platform.openai.com/docs/guides/batch/getting-started & https://github.com/brianSalk/JSONLgenerator (create for this a docker)
    - [] Improving the limitors for the threading and non-threading approach https://platform.openai.com/docs/guides/rate-limits/usage-tiers?context=tier-four & https://cookbook.openai.com/examples/how_to_handle_rate_limits & https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py 
    - [] Multi Agent strategy that another LLM is checking the response 
    - [] Make architecture diagram for the request and the check and reasking ChatGPT 
    - [X] Check if ChatGPT 4o is cheaper as 4 Turbo --> 4o is cheaper as Turbo 4 (Ressource)[https://openai.com/api/pricing/]
    - [] Build a json checker and send the data again to ChatGPT and ask for improvement (2xtime)
    - [] Integrate Amirs Repo as submodul
    - [] Implement a timer how long one US is needed to be analysed
    - [] Write a JSON validator for my format
    - [] Imrpvoe the prompting and send it to gabi for validation
    - [] Consider the email from Alex, and consider that often when a main part redundancy is found also a benefit redundancy is found
    - [] What to do with ChatGPT 4 turbo? This is pretty expensive 11€ for just G03 dataset
    - [] Mal eine Redundanzen aus den Daten von Amir raussuchen - Rausnehemen dann auch einfach die Daten dann aus den Analysen raus | schauen ob es besser wird mit dem oder neue beispiel 
    - [] Create time protocoll of how long is needed to analyse all in average
    - [] Create a token protokoll to check how long the single tokens are
    - [X] Hauptteil definieren
    - [X] Analyse von Hauptteil und Benefit gleichzeitig
    - [X] JSON format dafür vorbereiten
    - [X] Beispiele der JSON Datei überarbeiten
    - [] Analyse der Redundanzen gleichzeitig
    - [] Den Studenten fragen, wie das finale Format für die Redundanzen aussieht
    - [] Einmal nur die User Stories übergeben und einmal die User Stories mit den Annotations übergeben (Richtiger teil und nicht den Offset) (Das Delta bestimmen, was besser funktioniert)
    - [] First analyse the g03 dataset
    - [] Play with the parameterization of the model tempruature context etc.
    - [] Make similarity search by using word embeddings and vecoter database --> look for results
    - [] Simple similarity search based on an free word embedding (tokinizer) + simple simple similarity searches like: https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity where I pass just the main part or the benfit but not together plus annotations (optional)
    - [] Use hypothesis-jsonschema to create the json data needed for correct values

    --> Seperate the User Storys. All for "so that" is the main part and aftwards is the benefit. Grammatikalisch anuseinander ziehen wobei der Nebensatz der benefit ist.  
    --> Future Work: Building tooling for popular repositories

### Libaries to look inside
    - [] LongChain
    - [] Multi Agent suppport (find a libary)
    - [] Use word embeddings
    - [] Vector Database for User Story Clustering
    - [] Redundant requierments can be clustered together 
    - [] Create an interactive application to convert user stories to Henshin as vice versa


### Use
    - With local .venv
    - VSCode
    - jupyter notebook

### Use full links
    - https://dylancastillo.co/clustering-documents-with-openai-langchain-hdbscan/ (Simple Clusterin with just Word Embeddings and k-meas algorithm)
    - https://github.com/daniel-furman/awesome-chatgpt-prompts-clustering (Simpler Clustering)
    - https://pytorch.org/ (advanced machine learning libary)
    - https://platform.openai.com/tokenizer Tokenizer for chatgpt


Vector databases are specialized storage systems designed to handle vector embeddings, which are numerical representations of data (typically text) generated by machine learning models, including large language models (LLMs) like ChatGPT. These embeddings can capture the semantic properties of the data, making them useful for various tasks such as similarity search, recommendation systems, and more complex NLP tasks. Using vector databases in combination with LLMs can significantly enhance the performance and capabilities of AI applications. Here’s a guide on how to use vector databases with LLMs:

Step 1: Generate Embeddings Using LLMs
Select an LLM: Choose a suitable LLM for generating embeddings. GPT-3, BERT, or any of the models from Hugging Face's Transformers library are popular choices.
Process Text: Use the LLM to process your text data. This involves tokenization and passing the tokens through the model to get embeddings. For instance, you might use GPT-3 to generate embeddings for sentences, paragraphs, or documents.
Step 2: Store Embeddings in a Vector Database
Choose a Vector Database: Select a vector database that suits your needs. Popular vector databases include Pinecone, Milvus, Faiss (by Facebook AI), and Weaviate.
Indexing: Store the embeddings generated by the LLM in the vector database. This involves setting up an index for the embeddings, which can then be used to efficiently perform similarity searches or retrieve vectors.
Step 3: Querying the Vector Database
Perform Similarity Searches: Use the vector database to find embeddings that are similar to a given query embedding. This is useful in applications like semantic search, where you might want to find documents or text snippets that are semantically related to a query.
Use Cases: Integrate these capabilities into applications such as:
Semantic Search: Enhance search functionalities in applications by allowing users to search by meaning rather than by exact keyword match.
Recommendation Systems: Recommend content based on similarity to user preferences or previous interactions.
Data Clustering and Analysis: Cluster similar items together to discover patterns or group data in meaningful ways.
Step 4: Integration and Deployment
APIs and SDKs: Use APIs provided by the vector database for integration into your application. Most vector databases offer REST APIs, Python SDKs, or other library support.
Scalability and Performance: Ensure that your vector database setup is scalable and can handle the volume of embeddings and queries expected for your application. This may involve configuring the database for high performance, possibly in a distributed environment.

With ChatGPT and Pinecone