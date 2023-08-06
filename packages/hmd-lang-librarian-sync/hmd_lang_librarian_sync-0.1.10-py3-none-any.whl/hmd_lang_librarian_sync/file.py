

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class File(Noun):

    _entity_def = \
        {'name': 'file', 'namespace': 'hmd_lang_librarian_sync', 'metatype': 'noun', 'attributes': {'path': {'type': 'string', 'description': 'The canonical path to the file'}, 'content_path': {'type': 'string', 'description': 'The path to put the file in librarian'}, 'content_item_type': {'type': 'string', 'description': 'The path to put the file in librarian'}, 'modified': {'type': 'epoch', 'description': 'Timestamp of the last time the file was modified'}, 'hash': {'type': 'string', 'description': 'The hash of the file currently located at the path'}, 'hash_synced': {'type': 'string', 'description': 'The hash of the file the last time it was successfully synced'}, 'librarians_synced': {'type': 'mapping', 'description': 'The hash of the file mapped to librarian it was synced with'}, 'source_name': {'type': 'string', 'description': 'The name of the configured source the file is attached to'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return File._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(File._entity_def)


    

    
        
    @property
    def path(self) -> str:
        return self._getter("path")

    @path.setter
    def path(self, value: str) -> None:
        self._setter("path", value)
    
        
    @property
    def content_path(self) -> str:
        return self._getter("content_path")

    @content_path.setter
    def content_path(self, value: str) -> None:
        self._setter("content_path", value)
    
        
    @property
    def content_item_type(self) -> str:
        return self._getter("content_item_type")

    @content_item_type.setter
    def content_item_type(self, value: str) -> None:
        self._setter("content_item_type", value)
    
        
    @property
    def modified(self) -> Any:
        return self._getter("modified")

    @modified.setter
    def modified(self, value: Any) -> None:
        self._setter("modified", value)
    
        
    @property
    def hash(self) -> str:
        return self._getter("hash")

    @hash.setter
    def hash(self, value: str) -> None:
        self._setter("hash", value)
    
        
    @property
    def hash_synced(self) -> str:
        return self._getter("hash_synced")

    @hash_synced.setter
    def hash_synced(self, value: str) -> None:
        self._setter("hash_synced", value)
    
        
    @property
    def librarians_synced(self) -> Dict:
        return self._getter("librarians_synced")

    @librarians_synced.setter
    def librarians_synced(self, value: Dict) -> None:
        self._setter("librarians_synced", value)
    
        
    @property
    def source_name(self) -> str:
        return self._getter("source_name")

    @source_name.setter
    def source_name(self, value: str) -> None:
        self._setter("source_name", value)
    

    
        
    def get_to_file_file_hmd_lang_librarian_sync(self):
        return self.to_rels["hmd_lang_librarian_sync.file_file"]
    
    
        
    def get_from_file_file_hmd_lang_librarian_sync(self):
        return self.from_rels["hmd_lang_librarian_sync.file_file"]
    