import json
from typing import Any, get_type_hints, Collection
from typeguard import check_type


class Mixin:    # essa é uma classe do tipo mixin. Não tem funcionalidade própria, serve para fornecer funcionalidade a outras classes.

    protected_attributes = frozenset(('json_fields', 'type'))

    def to_dict(self):
        """
        Returns a json/dictionary representative of the card element
        """

        def get_json_dic(obj):
            # breakpoint()
            return {key: value for key in obj.json_fields if hasattr(obj, key) and (value := obj.__getattribute__(key)) is not None}

        # possível problema de circular reference ao passar o mesmo objeto em dois lugares diferentes do card. Averiguar depois.
        dic = json.loads(json.dumps(self, default=lambda obj: get_json_dic(obj)))
        return dic
    
    def is_collection(self, value):
        if isinstance(value, Collection) and not isinstance(value, str):
            return True
        return False

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in (type_hints := get_type_hints(self.__init__)):
            check_type(__value, type_hints[__name])
        if __name in self.protected_attributes and hasattr(self, __name):
            raise AttributeError(f"Can't set '{__name}' attribute")
        super().__setattr__(__name, __value)

    def __delattr__(self, __name: str) -> None:
        if __name in self.protected_attributes or hasattr(self, 'json_fields') and __name in self.json_fields:
            raise AttributeError(f"Cannot delete '{__name}' attribute")
