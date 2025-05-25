# Legacy API MCP Server

DC Inside 갤러리 API를 MCP(Machine Conversation Protocol) 서버로 제공하는 애플리케이션입니다.

## 설치 방법

1. Python 3.11 이상이 필요합니다.

2. 필요한 패키지 설치:
```bash
uv pip install fastmcp aiohttp
```

## 실행 방법

1. API 서버가 실행 중인지 확인:
   - API 서버는 `http://127.0.0.1:8000`에서 실행되어야 합니다.

2. MCP 서버 실행:
```bash
python my_server.py
```

서버가 성공적으로 실행되면 다음 메시지가 표시됩니다:
```
Starting MCP server 'legacy-api-mcp-server' with transport 'streamable-http' on http://127.0.0.1:9000/mcp
```

## 사용 가능한 도구

1. `get_gallery_posts`
   - 갤러리의 게시글 목록을 가져옵니다.
   - 매개변수:
     - `id`: 갤러리 식별자 (필수)
     - `page`: 페이지 번호 (기본값: 1)
     - `list_num`: 페이지당 게시글 수 (기본값: 50)
     - `use_cache`: 캐시 사용 여부 (기본값: True)

2. `get_gallery_info`
   - 갤러리의 기본 정보를 가져옵니다.
   - 매개변수:
     - `id`: 갤러리 식별자 (필수)
     - `use_cache`: 캐시 사용 여부 (기본값: True)

## 주의사항

- API 서버(`http://127.0.0.1:8000`)가 실행 중이어야 합니다.
- MCP 서버는 `http://127.0.0.1:9000`에서 실행됩니다.
- 캐시 기능이 활성화되어 있어 동일한 요청에 대해 빠른 응답이 가능합니다.
