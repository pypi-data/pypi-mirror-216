import json
from abc import abstractmethod, ABC
from copy import copy
from typing import Optional, Generator

import anthropic  # type: ignore
import openai

from .completions import CompletionChunk, PromptTemplateWithMetadata, CompletionResponse, ChatCompletionResponse, \
    ChatMessage
from .errors import APIKeyMissingError
from .llm_parameters import LLMParameters


class Flavor(ABC):
    @property
    @abstractmethod
    def record_format_type(self) -> str:
        raise NotImplementedError()

    @property
    def _model_params_with_defaults(self) -> LLMParameters:
        return LLMParameters.empty()

    @abstractmethod
    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        pass

    @abstractmethod
    def call_service(self, formatted_prompt: str, llm_parameters: LLMParameters) -> CompletionResponse:
        pass

    @abstractmethod
    def call_service_stream(self, formatted_prompt: str, llm_parameters: LLMParameters) -> Generator[
        CompletionChunk, None, None]:
        pass

    def _get_model_params(self, llm_parameters: LLMParameters) -> LLMParameters:
        return self._model_params_with_defaults.merge_and_override(llm_parameters)


class ChatFlavor(Flavor, ABC):
    @abstractmethod
    def continue_chat(
            self,
            previous_messages: list[ChatMessage],
            new_messages: Optional[list[ChatMessage]],
            llm_parameters: LLMParameters
    ) -> ChatCompletionResponse:
        pass


class OpenAI(Flavor, ABC):
    def __init__(self, openai_api_key: str, openai_api_base: Optional[str] = None):
        super().__init__()
        if openai_api_base:
            openai.api_base = openai_api_base

        if not openai_api_key or not openai_api_key.strip():
            raise APIKeyMissingError("OpenAI API key not set. It must be set to make calls to the service.")

        openai.api_key = openai_api_key


class OpenAIText(OpenAI):
    record_format_type = "openai_text"
    _model_params_with_defaults = LLMParameters({
        "model": "text-davinci-003"
    })

    def __init__(self, openai_api_key: str, openai_api_base: Optional[str] = None):
        super().__init__(openai_api_key, openai_api_base)

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        return prompt_template.content.format(**variables)

    def call_service(self, formatted_prompt: str, llm_parameters: LLMParameters) -> CompletionResponse:
        completion = openai.Completion.create(
            prompt=formatted_prompt,
            **self._get_model_params(llm_parameters)
        )  # type: ignore
        return CompletionResponse(
            content=completion.choices[0].text,
            is_complete=completion.choices[0].finish_reason == "stop"
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        completion = openai.Completion.create(
            prompt=formatted_prompt,
            stream=True,
            **self._get_model_params(llm_parameters)
        )  # type: ignore

        for chunk in completion:
            yield CompletionChunk(
                text=chunk.choices[0].text,
                is_complete=chunk.choices[0].finish_reason == "stop"
            )


class OpenAIChat(OpenAI, ChatFlavor):
    record_format_type = "openai_chat"
    _model_params_with_defaults = LLMParameters({
        "model": "gpt-3.5-turbo"
    })

    def __init__(self, openai_api_key: str, openai_api_base: Optional[str] = None):
        super().__init__(openai_api_key, openai_api_base)

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        # Extract messages JSON to enable formatting of individual content fields of each message. If we do not
        # extract the JSON, current variable interpolation will fail on JSON curly braces.
        messages_as_json = json.loads(prompt_template.content)
        formatted_messages = [
            {"content": message['content'].format(**variables), "role": message['role']} for message in
            messages_as_json]
        return json.dumps(formatted_messages)

    def call_service(self, formatted_prompt: str, llm_parameters: LLMParameters) -> CompletionResponse:
        messages = json.loads(formatted_prompt)
        completion = openai.ChatCompletion.create(
            messages=messages,
            **self._get_model_params(llm_parameters)
        )  # type: ignore
        return CompletionResponse(
            content=completion.choices[0].message.content,
            is_complete=completion.choices[0].finish_reason == "stop"
        )

    def continue_chat(
            self,
            previous_messages: list[ChatMessage],
            new_messages: Optional[list[ChatMessage]],
            llm_parameters: LLMParameters
    ) -> ChatCompletionResponse:
        messages = copy(previous_messages)
        if new_messages is not None:
            messages.extend(new_messages)
        completion = openai.ChatCompletion.create(
            messages=messages,
            **self._get_model_params(llm_parameters)
        )  # type: ignore
        messages.append(completion.choices[0].message.to_dict())
        return ChatCompletionResponse(
            content=completion.choices[0].message.content,
            message_history=messages,
            is_complete=completion.choices[0].finish_reason == "stop"
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        messages = json.loads(formatted_prompt)
        completion = openai.ChatCompletion.create(
            messages=messages,
            stream=True,
            **self._get_model_params(llm_parameters)
        )  # type: ignore
        for chunk in completion:
            # Not all chunks have a "content" field -- if they don't, keep chunking.
            yield CompletionChunk(
                text=chunk.choices[0].delta.get('content', ""),
                is_complete=chunk.choices[0].finish_reason == "stop"
            )


class AnthropicClaudeText(Flavor):
    record_format_type = "anthropic_text"
    _model_params_with_defaults = LLMParameters({
        "model": "claude-v1",
        "max_tokens_to_sample": 100
    })

    def __init__(self, anthropic_api_key: str):
        self.client = anthropic.Client(anthropic_api_key)

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        interpolated_prompt = prompt_template.content.format(**variables)
        # Anthropic expects a specific Chat format "Human: $PROMPT_TEXT\n\nAssistant:". We add the wrapping for Text.
        chat_formatted_prompt = f"{anthropic.HUMAN_PROMPT} {interpolated_prompt} {anthropic.AI_PROMPT}"
        return chat_formatted_prompt

    def call_service(self, formatted_prompt: str, llm_parameters: LLMParameters) -> CompletionResponse:
        anthropic_response = self.client.completion(
            prompt=formatted_prompt,
            **self._get_model_params(llm_parameters)
        )
        return CompletionResponse(
            content=anthropic_response['completion'],
            is_complete=anthropic_response['stop_reason'] == 'stop_sequence'
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        anthropic_response = self.client.completion_stream(
            prompt=formatted_prompt,
            **self._get_model_params(llm_parameters)
        )

        # Yield incremental text completions. Claude returns the full text output in every chunk.
        # We want to predictably return a stream like we do for OpenAI.
        prev_chunk = ''
        for chunk in anthropic_response:
            if len(prev_chunk) != 0:
                incremental_new_text = chunk['completion'].split(prev_chunk)[1]
            else:
                incremental_new_text = chunk['completion']

            prev_chunk = chunk['completion']
            yield CompletionChunk(
                text=incremental_new_text,
                is_complete=chunk['stop_reason'] == 'stop_sequence'
            )
