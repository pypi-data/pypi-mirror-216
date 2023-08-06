from typing import List, Optional, Union
from pydantic import BaseModel, validator, Field

class ModelData(BaseModel):
  id: str
  name: str
  type: str
  object: str
  owned_by: str

class UnknownRoleException(Exception):
  pass

class ChatMessage(BaseModel):
  role: str
  content: str

  @validator('role')
  def validate_role(cls, role):
    if role not in ['user', 'assistant']:
      raise UnknownRoleException(role)
    return role
  
class ChatModel(BaseModel):
    provider: Optional[str]
    type: Optional[str]
    modelName: Optional[str]

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: float = Field(1.0, ge=0, le=2)
    top_p: float = Field(1.0, ge=0, le=1)
    top_k: int = Field(0, ge=0)
    max_tokens: int = Field(200, ge=0)
    presence_penalty: float = Field(0.1, ge=-2, le=2)
    frequency_penalty: float = Field(0.0, ge=0, le=2)
    logit_bias: Optional[List[float]] = None
    stream: bool = Field(False)

class Choice(BaseModel):
  finish_reason: str
  index: int
  logprobs: Optional[int]
  message: ChatMessage

class Usage(BaseModel):
  completion_tokens: int
  prompt_tokens: int
  total_tokens: int

class Message(BaseModel):
    role: str
    content: str

class CompletionOption(BaseModel):
    frequency_penalty: Optional[float]
    max_tokens: Optional[int]
    presence_penalty: Optional[float]
    stop: Optional[List[str]]
    stream: Optional[bool]
    temperature: Optional[float]
    top_k: Optional[int]
    top_p: Optional[float]

class ChatCompletionData(BaseModel):
    id: str
    createdAt: int
    choices: List[Choice]
    usage: Usage
