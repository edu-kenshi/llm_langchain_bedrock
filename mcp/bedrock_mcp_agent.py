'''
- Agent 개발
    - Langchain, `Langgrap`  구성
    - Bedrock 기반 LLM 사용
    - MCP를 이용하여 tool 사용
'''
# 1. 모듈가져오기
import os
import boto3
import asyncio
from dotenv import load_dotenv

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode

from mcp_tools_adapter import MCPClient
