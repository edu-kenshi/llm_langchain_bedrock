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
        # Server 접속시 필요한 정보 세팅
        server_params = StdioServerParameters(
            command = sys.executable,
            args    = [self.server_script],
            env     = None
        )
        print(f'sys.executable {sys.executable} server_script {self.server_script}')
        # 접속 -> I/O -> 예외상황 발생될수 있음
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    print(f'MCP 서버 연결 성공 : 서버측으로부터 입력, 출력에 대한 객체 획득')


        except Exception as e:
            print( f'MCP Server 접속 오류 : {e}' )
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