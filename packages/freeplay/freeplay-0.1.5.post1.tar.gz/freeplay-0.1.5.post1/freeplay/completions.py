from dataclasses import dataclass

ChatMessage = dict[str, str]


@dataclass
class CompletionResponse:
    content: str
    is_complete: bool


@dataclass
class ChatCompletionResponse:
    content: str
    is_complete: bool
    message_history: list[ChatMessage]


@dataclass
class PromptTemplateWithMetadata:
    project_version_id: str
    prompt_template_id: str
    name: str
    content: str


@dataclass
class PromptTemplates:
    templates: list[PromptTemplateWithMetadata]


@dataclass
class CompletionChunk:
    text: str
    is_complete: bool
