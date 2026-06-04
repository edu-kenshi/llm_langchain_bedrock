'''
MCP 1.27.2
외부 도구를 구현한 MCP 서버, FastMCP를 이용하여 간결하게 구성
'''
# 1. 모듈 가져오기
import sys
import logging
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# 2. 로깅 설정
#    출력값 섞이면 불편 => stderr 출력 조정
logging.basicConfig(
    level  = logging.INFO,
    format = '[MCP Server] %(levelname)s: %(message)s',
    stream = sys.stderr
)
logger = logging.getLogger(__name__)

# 3. MCP 서버 설정
mcp = FastMCP('6ToolsMCPServer')
logger.info('MCPServer 구성(초기화) 중..')

# 4. 인메모리 -> 메모/임시데이터를 저장할 tool 용도로 dict 형태로 저장관리용 -> 기본 구성 x
note_memory = dict()

# 5. 툴 구현 (외부에 특정 리소스, s/w, 기타.. ), 편의상 간단한 기능 구성, 6개 구성
## Tool 1 : add (두 수를 더하기) -> 함수구성, 타입힌트 명시, 함수 주석
def add(a: float, b: float) -> str:
    '''
    두 수를 더하는 계신기

    Args:
        a: 첫 번째 수치
        b: 두 번째 수치
    
    Returns
        계산 결과
    '''
    result = a + b
    logger.info(f'Tool 1 add 호출: {a} + {b} = {result}')
    return f'계산 결과: {a} + {b} = {result}'

# 6. 서버 가동