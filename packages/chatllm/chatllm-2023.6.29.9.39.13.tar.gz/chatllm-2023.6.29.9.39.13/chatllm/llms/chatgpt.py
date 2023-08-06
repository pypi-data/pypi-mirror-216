#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatgpt
# @Time         : 2023/6/29 08:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def load_llm4chat(**kwargs):
    import openai

    openai.api_key = os.getenv("API_KEY", kwargs.get('api_key', 'chatllm'))
    openai.api_base = os.getenv("API_BASE", kwargs.get('api_base', "https://api.openai-proxy.com/v1"))

    def stream_chat(query, history=None, **chat_kwargs):
        history = history or []
        messages = history + [{"role": "user", "content": query}]

        kwargs = {
            "model": "gpt-3.5-turbo-0613",
            "stream": True,
            "max_tokens": 4000,
            "temperature": None,
            "top_p": None,
            "messages": messages,
            "user": "Betterme"
        }
        chat_kwargs = {**kwargs, **chat_kwargs}
        chat_kwargs = {k: chat_kwargs[k] for k in kwargs}  # 过滤不支持的参数

        completion = openai.ChatCompletion.create(**chat_kwargs)

        for c in completion:
            _ = c.choices[0].get('delta').get('content', '')
            yield _

    return stream_chat


if __name__ == '__main__':
    pass
