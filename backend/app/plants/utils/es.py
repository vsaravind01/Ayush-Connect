from elasticsearch import Elasticsearch
from fastapi.exceptions import HTTPException


class ElasticSearchClient:
    def __init__(self, hosts: list):
        self.client = Elasticsearch(hosts=hosts)

    def create_index(self, index: str) -> bool:
        """
        Create elasticsearch index for given index name

        Parameters
        ----------
        index: str
            Name of the index to be created

        Returns
        -------
        bool
            Status of the index creation

        Raises
        ------
        HTTPException
            409 - If index already exists
            500 - If index creation fails
        """
        if self.client.indices.exists(index):
            raise HTTPException(status_code=409, detail=f"Index - '{index}' already exists")
        else:
            try:
                self.client.indices.create(index=index)
                return True
            except Exception as e:
                raise HTTPException(status_code=500, detail="Index creation failed - Internal Server Error")

    def delete_index(self, index: str) -> bool:
        """
        Delete elasticsearch index for given index name

        Parameters
        ----------
        index: str
            Name of the index to be deleted

        Returns
        -------
        bool
            Status of the index deletion

        Raises
        ------
        HTTPException
            404 - If index does not exist
            500 - If index deletion fails
        """
        if self.client.indices.exists(index):
            try:
                self.client.indices.delete(index=index)
                return True
            except Exception as e:
                raise HTTPException(status_code=500, detail="Index deletion failed - Internal Server Error")
        else:
            raise HTTPException(status_code=404, detail=f"Index - '{index}' does not exists")

    def index_document(self, index: str, document: dict) -> bool:
        """
        Index document in elasticsearch index

        Parameters
        ----------
        index: str
            Name of the index to be created
        document: dict
            Document to be indexed

        Returns
        -------
        bool
            Status of the document indexing

        Raises
        ------
        HTTPException
            500 - If document indexing fails
        """
        try:
            self.client.index(index=index, body=document)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail="Document indexing failed - Internal Server Error")

    def search_document(self, index: str, query: dict) -> dict:
        """
        Search document in elasticsearch index

        Parameters
        ----------
        index: str
            Name of the index to be created
        query: dict
            Query to be searched

        Returns
        -------
        dict
            Search results

        Raises
        ------
        HTTPException
            500 - If document search fails
        """
        try:
            return self.client.search(index=index, body=query)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Document search failed - Internal Server Error")

    def delete_document_by_id(self, index: str, document_id: str) -> bool:
        """
        Delete document in elasticsearch index

        Parameters
        ----------
        index: str
            Name of the index to be created
        document_id: str
            Id of the document to be deleted

        Returns
        -------
        bool
            Status of the document deletion

        Raises
        ------
        HTTPException
            500 - If document deletion fails
        """
        try:
            self.client.delete(index=index, id=document_id)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail="Document deletion failed - Internal Server Error")

    def delete_document_by_query(self, index: str, query: dict) -> bool:
        """
        Delete document in elasticsearch index

        Parameters
        ----------
        index: str
            Name of the index to be created
        query: dict
            Query to be searched

        Returns
        -------
        bool
            Status of the document deletion

        Raises
        ------
        HTTPException
            500 - If document deletion fails
        """
        try:
            self.client.delete_by_query(index=index, body=query)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail="Document deletion failed - Internal Server Error")

    def update_document_by_id(self, index: str, document_id: str, document: dict) -> bool:
        """
        Update document in elasticsearch index

        Parameters
        ----------
        index: str
            Name of the index to be created
        document_id: str
            Id of the document to be updated
        document: dict
            Document to be updated

        Returns
        -------
        bool
            Status of the document update

        Raises
        ------
        HTTPException
            500 - If document update fails
        """
        try:
            self.client.update(index=index, id=document_id, body={"doc": document})
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail="Document update failed - Internal Server Error")

    def update_document_by_query(self, index: str, query: dict, document: dict) -> bool:
        """
        Update document in elasticsearch index

        Parameters
        ----------
        index: str
            Name of the index to be created
        query: dict
            Query to be searched
        document: dict
            Document to be updated

        Returns
        -------
        bool
            Status of the document update

        Raises
        ------
        HTTPException
            500 - If document update fails
        """
        try:
            self.client.update_by_query(index=index, query=query, body={"doc": document})
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail="Document update failed - Internal Server Error")
