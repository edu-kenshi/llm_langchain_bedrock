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
        # MCP Tool 로드
        print(f'MCP Server와 연결중..')
        # mcp_tools_adapter.py와 작업 기술

        # LLM 생성
        print(f'LLM 초기화 중..')
        self._init_llm()

        # langgraph 기반 에이전트 구성
        print(f'langgraph agent 구성 중..')
        self._setup_graph()

        print(f'초기화 완료\n 프럼프트 입력 대기..')
        return self
    
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
    def _setup_graph( self ):
        # 1. llm에 MCP 도구들을 바인딩 -> llm_with_tools 구성
        llm_with_tools = self.llm.bind_tools(self.tools)
        # 2. 상태(공유 메모리)를 가진 그래프 생성
        workflow = StateGraph(MessagesState)
        # 3. 그래프 노드 추가 ( MCP 도구 호출,  LLM 도구 )
        # 함수 내부에 함수가 존재 => 내부함수, 함수 내부에서만 사용 가능, 외부사용 X
        def call_agent(state:MessagesState) -> dict:
            '''LLM 호출하여 TOOL 선택, 응답 생성'''
            messages = state['messages']
            # 필요하면 퓨샷등 추가
            res      = llm_with_tools.invoke( messages )
            # 응답 내용 메세지로 구성            
            return {'messages':[res]}
            pass
        # 툴 노드 생성
        tool_node = ToolNode(self.tools)
        workflow.add_node('agent',  call_agent)
        workflow.add_node('tools',  tool_node)

        # 4. 엣지(규칙, 순서, 시작, 종료등) 설정(정의)
        # 시작점
        workflow.set_entry_point('agent') # llm 일차 판단
        def 조건부함수(state:MessagesState)->str:
            '''tool_calls 값 체크하여 툴로 진행, 끝낼지 판단'''
            messages = state['messages']
            # 마지막 메세지
            last_msg = messages[-1]
            if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                # 도구를 사용하라는 의미
                return 'tools'
            return 'end'
            pass

        # 판단 -> 조건부
        workflow.add_conditional_edges(
            'agent',
            조건부함수,
            {
                "tools":'tools',
                "end"  : END
            }
        )
        # 방향성
        workflow.add_edge('tools', 'agent') # tools 노드 -> agent 노드로 이동
        # 5. 그래프 컴파일
        self.graph = workflow.compile()
        pass
    
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