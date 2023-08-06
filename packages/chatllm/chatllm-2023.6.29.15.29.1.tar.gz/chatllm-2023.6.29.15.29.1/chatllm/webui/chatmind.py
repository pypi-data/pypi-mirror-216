#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatmind
# @Time         : 2023/6/29 15:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from chatllm.applications.chatmind import ChatMind

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title='🔥ChatMind', layout='wide', initial_sidebar_state='collapsed')

html_str = ChatMind().mind_html()

html(html_str)
