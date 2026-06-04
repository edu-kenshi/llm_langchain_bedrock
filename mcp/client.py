'''
MCP Client
MCP Server 와 통신
'''
# 1. 모듈 가져오기
import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters # 커넥션 담당
from mcp.client.stdio import stdio_client # 입력, 출력을 가진 클라이언트

# 2. MCPClient 클레스 구성
class MCPClient:
    '''MCP Server와 통신하는 클레스(역활:클라이언트)'''
    # 생성자
    def __init__(self, server_script: str = 'server.py'):
        '''
        Args:
            server_script: 실행할 Server측 스크립트 경로
        '''
        self.server_script = server_script
        self.tools = [] # MCP 서버에게 툴 목록 가져와서 저장
        pass
    
    # 실제 일을 수행하는 함수
    async def run(self):
        print(f'MCP Server 접속중...')
        pass

# 3. 비동기 main 함수 구성
async def main():
    '''비동기식 메인 함수'''
    # MCPClient 객체 생성
    client = MCPClient()
    # 가동
    await client.run()

# 4. 비동기 함수 호출 -> MCP 서버 연동
if __name__ == '__main__':
    # 비동기로 함수를 호출
    asyncio.run( main() )