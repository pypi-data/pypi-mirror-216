from sentence_transformers import SentenceTransformer


class BertEmbedding:
    def __init__(self) -> None:
        self.__model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def calculate_embedding(self,document):
        if isinstance(document,str) is False:
            raise ValueError("document is not str")
        doc_embedding = self.__model.encode(document)
        result = dict()
        result["success"] = True
        result["vec"] = doc_embedding
        return result