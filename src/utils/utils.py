# src/utils/utils.py
import tiktoken
from pydantic import create_model
import inspect
from inspect import Parameter
from typing import Callable, Dict, Any

from config.logging_config import logger

class Utils:
    def count_number_of_tokens(self, text: str) -> int:
        """
        Counts the number of tokens in a given text using the GPT-4o-mini encoding.
        """
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        tokens = encoding.encode(text)
        n_tokens = len(tokens)
        logger.info("[UTILS] count_number_of_tokens called (tokens=%d)", n_tokens)
        return n_tokens

    def count_number_of_characters(self, text: str) -> int:
        """
        Counts the number of characters in a given text.
        """
        n_chars = len(text)
        logger.info("[UTILS] count_number_of_characters called (chars=%d)", n_chars)
        return n_chars

    def jsonschema(self, f: Callable) -> Dict[str, Any]:
        """
        Generate a JSON schema for the input parameters of the given function.
        """
        logger.info("[UTILS] jsonschema() called for function %s", f.__name__)
        kw = {
            n: (o.annotation, ... if o.default == Parameter.empty else o.default)
            for n, o in inspect.signature(f).parameters.items()
        }
        s = create_model(f"Input for `{f.__name__}`", **kw).schema()
        return dict(name=f.__name__, description=f.__doc__, parameters=s)
