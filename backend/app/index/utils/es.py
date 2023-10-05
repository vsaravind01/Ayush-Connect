from elasticsearch import Elasticsearch
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()


class ElasticSearchClient:
    def __init__(self, hosts: list = None):
        if hosts is None:
            hosts = [os.environ['ELASTICSEARCH_HOST']]
        self.client = Elasticsearch(hosts=hosts)

    def get_index_uuid(self, index: str) -> str:
        """
        Get uuid for given index

        Parameters
        ----------
        index: str
            Name of the index

        Returns
        -------
        str
            UUID

        Raises
        ------
        HTTPException
            404 - If index does not exist
            500 - If uuid fetch fails
        """
        if self.client.indices.exists(index=index):
            try:
                return self.client.indices.get_settings(index=index)[index]['settings']['index']['uuid']
            except Exception:
                raise HTTPException(status_code=500, detail="UUID fetch failed - Internal Server Error")
        else:
            raise HTTPException(status_code=404, detail=f"Index - '{index}' does not exists")

    def get_indices(self, header: str = "index") -> list:
        """
        Get all the indices in elasticsearch

        Returns
        -------
        list
            List of indices

        Raises
        ------
        HTTPException
            500 - If index fetch fails
        """
        try:
            return self.client.cat.indices(h=header, s='index').split()
        except Exception:
            raise HTTPException(status_code=500, detail="Index fetch failed - Internal Server Error")

    def index_exists(self, index_name: str) -> bool:
        """
        Check if an index exists or not

        Parameters
        ----------
        index_name: str

        """
        return self.client.indices.exists(index_name)

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
            except Exception:
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
            except Exception:
                raise HTTPException(status_code=500, detail="Index deletion failed - Internal Server Error")
        else:
            raise HTTPException(status_code=404, detail=f"Index - '{index}' does not exists")

    def create_alias(self, index: str, alias: str) -> bool:
        """
        Create alias for given index

        Parameters
        ----------
        index: str
            Name of the index
        alias: str
            Alias name for the index

        Returns
        -------
        bool
            Status of the alias creation

        Raises
        ------
        HTTPException
            404 - If index does not exist
            500 - If alias creation fails
        """
        if self.client.indices.exists(index):
            try:
                self.client.indices.put_alias(index=index, name=alias)
                return True
            except Exception:
                raise HTTPException(status_code=500, detail="Alias creation failed - Internal Server Error")
        else:
            raise HTTPException(status_code=404, detail=f"Index - '{index}' does not exists")

    def alias_exists(self, alias: str) -> bool:
        """
        Check if an alias exists or not

        Parameters
        ----------
        alias: str

        """
        return self.client.indices.exists_alias(alias)

    def delete_alias(self, index: str, alias: str) -> bool:
        """
        Delete alias for given index

        Parameters
        ----------
        index: str
            Name of the index
        alias: str
            Alias name for the index

        Returns
        -------
        bool
            Status of the alias deletion

        Raises
        ------
        HTTPException
            404 - If index does not exist
            500 - If alias deletion fails
        """
        if self.client.indices.exists(index):
            try:
                self.client.indices.delete_alias(index=index, name=alias)
                return True
            except Exception:
                raise HTTPException(status_code=500, detail="Alias deletion failed - Internal Server Error")
        else:
            raise HTTPException(status_code=404, detail=f"Index - '{index}' does not exists")

    def update_alias(self, index: str, alias: str) -> bool:
        """
        Update alias for given index

        Parameters
        ----------
        index: str
            Name of the index
        alias: str
            Alias name for the index

        Returns
        -------
        bool
            Status of the alias update

        Raises
        ------
        HTTPException
            404 - If index does not exist
            500 - If alias update fails
        """
        if self.client.indices.exists(index):
            try:
                # delete all existing aliases for the index
                for alias_name in self.client.indices.get_alias(index).keys():
                    self.delete_alias(index=index, alias=alias_name)
                # create new alias for the index
                return self.create_alias(index=index, alias=alias)
            except Exception:
                raise HTTPException(status_code=500, detail="Alias update failed - Internal Server Error")
        else:
            raise HTTPException(status_code=404, detail=f"Index - '{index}' does not exists")

    def index_or_alias_exists(self, index_or_alias: str) -> bool:
        """
        Check if an index or alias exists or not

        Parameters
        ----------
        index_or_alias: str

        """
        try:
            return self.client.indices.exists(index_or_alias) or self.client.indices.exists_alias(index_or_alias)
        except Exception:
            raise HTTPException(status_code=500, detail="Index or alias existence check failed - Internal Server Error")

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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
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
        except Exception:
            raise HTTPException(status_code=500, detail="Document update failed - Internal Server Error")

    def get_document_by_id(self, index: str, document_id: str) -> dict:
        """
        Get document in elasticsearch index

        Parameters
        ----------
        index: str
            Name of the index to be created
        document_id: str
            Id of the document to be fetched

        Returns
        -------
        dict
            Document

        Raises
        ------
        HTTPException
            500 - If document fetch fails
        """
        try:
            return self.client.get(index=index, id=document_id)
        except Exception:
            raise HTTPException(status_code=500, detail="Document fetch failed - Internal Server Error")
