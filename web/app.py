import streamlit as st
import requests as req

# 환경변수, 상수
API_URL = 'http://localhost:8000/chat'
# 프런트 외관
st.set_page_config(page_title='식사 메뉴 해결사')
st.title('AI 식사 메뉴 해결사 - KING')
st.caption('점심/저녁등 시점, 날씨, 기분, 단체여부, 예산, MBTI등등 알려주시면 메뉴를 추천해 드립니다.')

# 대화 내용을 기억하는 공간 -> st.session_state 관리
# 최초
if "messages" not in st.session_state: # 1회만 수행
    # 내용 추가(기본 가이드) -> 어떤 서비스를 이용하지 최초 가이드 채팅 제공
    st.session_state.messages = [
        # 페르소나는 추후 백엔드에서 고정하여 제공-> 필요시 고객이 선택
        {
            'role':'assistant',
            'content':'안녕하세요!. 오늘 식사는 어떤 메뉴를 추천해 드릴까요? 현재 상황, 기분 등등 알려주세요'
        }
    ]

# 이전 대화 내용 화면 출력
for msg in st.session_state.messages:
    # 존재하는 모든 대화 내용 출력
    with st.chat_message( msg['role'] ):
        st.markdown( msg['content'] )

# 입력창 필요 -> 음성, `텍스트`, ...
if prompt := st.chat_input('현재 상황을 자세하게 입력하세요..'):
    # 전역 상태 창에서 관리하는 저장 공간에 대화 내용 추가
    st.session_state.messages.append({
        'role'   :'user',
        'content': prompt
    })
    
    # 화면에 표기
    with st.chat_message( 'user' ):
        st.markdown( prompt )

    # 백엔드 요청 -> LLM에게 추천
    # 1. 생각 하는 연출 진행
    with st.chat_message( 'assistant' ):
        msg_holder = st.empty()
        msg_holder.markdown( '심각한 고민중 ㅡ,.ㅡ^..' )

    # 2. 실제 LLM에게 질의 -> FASTAPI 요청 ~/chat
    result = None
    try:
        # 요청
        res = req.post(API_URL, json={"query":prompt})
        # 200 체크
        if res.status_code == 200: # 응답 성공
            result = res.json().get('response', '일시적 장애입니다.잠시후 다시 시도해주세요')
        else:
            result = f'서버측 오류 {res.status_code}'
    except Exception as e:
        print( e )
        result = f'오류 {e}'
    
    # 화면처리
    msg_holder.markdown( result )

    # 대화 내용 추가
    st.session_state.messages.append({
        'role'   :'assistant',
        'content': result
    })
