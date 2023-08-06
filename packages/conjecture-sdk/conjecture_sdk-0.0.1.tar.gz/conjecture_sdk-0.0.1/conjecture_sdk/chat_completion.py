from . import api_key
from .api import ConjAPI
from .data_models import ChatCompletionData, ChatMessage, ChatModel, ChatRequest, ModelData
from typing import List, Dict, Optional, Union

class ChatCompletion:
  @classmethod
  def create(cls, model: Union[str, ModelData, ChatModel], messages: Union[List[ChatMessage], List[Dict[str, str]]], options: Optional[ChatRequest] = None) -> ChatCompletionData:
    api = ConjAPI(api_key)
    messages_data = [ChatMessage(**m) if isinstance(m, dict) else m for m in messages]

    if options is None:
      options = ChatRequest(model=model, messages=messages_data)

    if not isinstance(model, str) and not isinstance(model, ChatModel):
      model = {
        "type": model.type,
        "provider": model.name,
        "modelName": model.name
      }

    data = {
      "model": model,
      "messages": [m.dict() for m in messages_data],
      "options": options.dict(),
    }

    response = api.request("POST", "chats/completion", data)
    chat_completion = ChatCompletionData(**response)

    return chat_completion