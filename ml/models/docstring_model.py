import re
import torch

from configs import local_model_settings as model_configs
from configs import prompts
from src import database_entities
from models import base_model as base_model_module


class DocstringApiModel(base_model_module.BaseApiModel):
    def __init__(
            self,
            model_name: str = "synthetic",
            model_type: str = "docstring",
            model_description: str = "llama70b api",
            prompt: str = prompts.DOCSTRING_PROMPT,
            prompt_desc: str = "",
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            prompt=prompt,
            prompt_desc=prompt_desc,
        )

    def _get_final_result(self, model_response: str) -> str:
        regexp_result = re.search('([\'\"]{3})(.*?)([\'\"]{3})', model_response, re.DOTALL)
        return regexp_result.group(2) if regexp_result else model_response

    def get_prompt(
            self,
            data_row: database_entities.Function,
    ) -> str:
        context = (
            f"\nHere you can see examples of"
            f" usages of such function:\n{data_row.context[:model_configs.CONTEXT_MAX_LENGTH]}"
            if data_row.context else ""
        )
        full_prompt = self.prompt.format(code=data_row.code, context_info=context)
        return full_prompt


class DocstringLocalModel(base_model_module.BaseLocalModel):
    def __init__(
            self,
            model_name: str,
            model_description: str,
            model_type: str = "docstring",
            prompt: str = prompts.DOCSTRING_PROMPT,
            prompt_desc: str = "",
            device: torch.device = model_configs.DEVICE,
            weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            device=device,
            weight_type=weight_type,
            prompt=prompt,
            prompt_desc=prompt_desc,
        )

    def _get_final_result(self, model_response: str) -> str:
        regexp_result = re.search('([\'\"]{3})(.*?)([\'\"]{3})', model_response, re.DOTALL)
        return regexp_result.group(2) if regexp_result else model_response

    def get_prompt(
            self,
            data_row: database_entities.Function,
    ) -> str:
        context = (
            f"\nHere you can see examples of"
            f" usages of such function:\n{data_row.context[:model_configs.CONTEXT_MAX_LENGTH]}"
            if data_row.context else ""
        )
        full_prompt = self.prompt.format(code=data_row.code, context_info=context)
        return full_prompt
