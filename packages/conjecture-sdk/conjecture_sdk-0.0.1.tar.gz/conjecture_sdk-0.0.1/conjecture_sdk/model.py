from . import api_key
from .api import ConjAPI
from .data_models import ModelData
from typing import List

class Model:
    @classmethod
    def list(cls) -> List[ModelData]:
        api = ConjAPI(api_key)
        response = api.request("GET", "models")
        models = [ModelData(**model) for model in response]
        return models
