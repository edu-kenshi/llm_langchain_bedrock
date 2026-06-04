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

# 2. 환경변수 로드
load_dotenv()

# 3. BedrockMCPAgent 클레스 구성
class BedrockMCPAgent:
    # 생성자
    def __init__(self, server_script: str = 'server.py', use_bedrock: bool = True):
        self.server_script = server_script
        self.use_bedrock   = use_bedrock # LLM의 출처 구분
        self.llm   = None  # ChatBedrock, LLM 자체
        self.tools = []
        self.graph = None  # Langgraph workflow # LLM, 도구등 배치하는 그래프 
        self.mcp_adpater = None # mcp_tools_adapter내 객체와 MCP 서버와 연동


    # 초기화
    async def initialize( self ):

        # LLM 생성
        self._init_llm()

        pass
    # llm 생성
    async def _init_llm(self):
        try:
            self.llm = ChatBedrock( 
                    model_id    = os.getenv('MODEL_ID'),
                    client      = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION') ),
                    model_kwargs= {"temperature":0.7, "max_tokens":2000}
            )
            print('Bedrock LLM 객체 생성 완료')
        except Exception as e:
            # 특정 회사 라이브러리 설치하면 가능
            # pip install anthropic openai ....
            # from langchain_anthropic import ChatAnthropic
            # 다른 모델 사용, 특정 회사 모델 직접 사용(클로드, gpt, 제미나이등)
            print('Bedrock LLM 객체 생성 실패 {e}')
            pass
        pass
    # 그래프 구성
    
    # 사용자 요청 처리(프럼프트 처리)
    
    # 메모리 정리(뒷정리)
    pass

# 4. 메인함수
async def main():
    # BedrockMCPAgent 에이전트 생성
    # 사용자 입력 대기(프럼프트 입력 대기) -> 무한루프? 1회성?
    # BedrockMCPAgent 에이전트의 `사용자 요청 처리` 함수 호출
    pass

# 5. 서비스가동
if __name__ == '__main__':    
    asyncio.run( main() )