import requests
import json
import numpy as np
import faiss
import openai
import warnings
from tenacity import retry, wait_exponential, stop_after_attempt
from tqdm import tqdm

warnings.filterwarnings("ignore")


class PigeonsDBError(Exception):
    pass


def get_embedding(input):
    text = text.replace("\n", " ")
    response = openai.Embedding.create(input, "text-embedding-ada-002")
    embedding = response['data'][0]['embedding']
    return np.array(embedding)


class PigeonsDB:
    __connection = None
    __index_p = None
    
    

    @staticmethod
    def get_db_info(api_key, db_name):
        url = "https://api.pigeonsai.com/api/v1/sdk/get-db-info"
        headers = {"Content-Type": "application/json"}
        data = {"api_key": api_key, "dbname": db_name}
        response = requests.post(url, headers=headers, data=json.dumps(data))

        db_info = response.json().get('DB info', {})
        index_p = db_info.get('s3_identifier')
        keys = ['dbname', 'user', 'password', 'host']
        connect = {key: db_info.get(key) for key in keys}
        return index_p, connect
    
    
    
    
    @staticmethod
    def init(API, DB_Name):
        index_p, connect = PigeonsDB.get_db_info(API, DB_Name)
        if connect:
            PigeonsDB.__connection = connect
            PigeonsDB.__index_p = index_p
        else:
            raise PigeonsDBError("API key or DB name not found")
  



    @staticmethod
    def search(query_text, k=5, metadata_filters=None, keywords=None):
        if PigeonsDB.__connection is None:
            raise PigeonsDBError("Connection not initialized.")
        url = "http://test-search-1248249294.us-east-2.elb.amazonaws.com:8080/search"

        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "query_text": query_text,
            "k": k,
            "metadata_filters": metadata_filters,
            "keywords": keywords
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        # print the response
        res = json.loads(response.text)
        return res
    
    
    
    

    @staticmethod
    @retry(wait=wait_exponential(multiplier=1, min=2, max=60), stop=stop_after_attempt(5))
    def add(documents: list, metadata_list=None):
       
        if PigeonsDB.__connection is None:
            raise PigeonsDBError("Connection not initialized.")
        # Ensure documents and metadata_list are lists
        if not isinstance(documents, list):
            documents = [documents]
        if metadata_list is not None and not isinstance(metadata_list, list):
            metadata_list = [metadata_list]
        
        # Set the chunk size to 70
        chunk_size = 100
        # Create a list of chunks
        chunks = [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]
        
        # Iterate through the chunks using a for loop and tqdm
        for chunk in tqdm(chunks):
            url = "http://add-dev-177401989.us-east-2.elb.amazonaws.com:8080/add_documents"
            headers = {"Content-Type": "application/json"}
            data = {
                "connection": PigeonsDB.__connection,
                "index_path": PigeonsDB.__index_p,
                "documents": chunk,
                "metadata_list": metadata_list
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            # print the response
            print(response)
            
            

    @staticmethod
    def delete_documents(object_ids):
        if PigeonsDB.__connection is None:
            raise PigeonsDBError("Connection not initialized.")
        url = "http://add-dev-177401989.us-east-2.elb.amazonaws.com/delete_documents"
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "object_ids": object_ids
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # print the response
        print(response.json())







class SemanticChunking:




    def ada(text, min_tokens, max_tokens):
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        print(sentences)
        # Convert sentences to embeddings using a pre-trained model
        embeddings = []
        for i in sentences:
            tensors = get_embedding(i)
            embeddings.append(tensors)
        embeddings = np.array((embeddings))
        # Calculate the number of clusters based on the desired token count
        total_tokens = sum([len(word_tokenize(sentence)) for sentence in sentences])
        num_clusters = max(1, int(total_tokens / max_tokens))

        # Train the k-means model on the embeddings
        kmeans = faiss.Kmeans(embeddings.shape[1], num_clusters, niter=20, verbose=False)
        kmeans.train(embeddings.astype(np.float32))

        # Cluster the sentences based on the k-means model
        _, cluster_assignments = kmeans.index.search(embeddings.astype(np.float32), 1)
        clusters = [[] for _ in range(num_clusters)]
        for i, assignment in enumerate(cluster_assignments):
            clusters[assignment[0]].append(sentences[i])

        # Create chunks based on the clusters and the desired token count
        chunks = []
        for cluster in clusters:
            chunk = []
            tokens_in_chunk = 0
            for sentence in cluster:
                tokens = word_tokenize(sentence)
                num_tokens = len(tokens)
                if tokens_in_chunk + num_tokens > max_tokens:
                    chunks.append(' '.join(chunk))
                    chunk = [sentence]
                    tokens_in_chunk = num_tokens
                elif tokens_in_chunk + num_tokens < min_tokens:
                    chunk.append(sentence)
                    tokens_in_chunk += num_tokens
                else:
                    chunk.append(sentence)
                    chunks.append(' '.join(chunk))
                    chunk = []
                    tokens_in_chunk = 0
            if chunk:
                chunks.append(' '.join(chunk))

        return chunks
    