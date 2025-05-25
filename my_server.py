from fastmcp import FastMCP
import aiohttp
import json
from typing import Optional, Dict, Any

mcp = FastMCP(name="legacy-api-mcp-server")

# 캐시 저장소
_cache: Dict[str, Any] = {}

async def fetch_dcinside_data(endpoint: str, params: dict, use_cache: bool = True) -> dict:
    """
    DC Inside API에서 데이터를 가져옵니다.
    
    Args:
        endpoint: API 엔드포인트
        params: API 요청 매개변수
        use_cache: 캐시 사용 여부
    
    Returns:
        dict: API 응답 데이터
    """
    cache_key = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
    
    if use_cache and cache_key in _cache:
        return _cache[cache_key]
    
    base_url = "http://127.0.0.1:8000"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/{endpoint}", params=params) as response:
            if response.status != 200:
                raise Exception(f"API 요청 실패: {response.status}")
            
            data = await response.json()
            
            if use_cache:
                _cache[cache_key] = data
            
            return data

@mcp.tool()
def greet(name: str) -> str:
    """
    사용자의 이름을 받아 인사말을 반환합니다.
    
    Args:
        name: 인사할 사용자의 이름
    
    Returns:
        str: 사용자 이름을 포함한 인사말
    """
    print(f"Greeting {name}")
    return f"Hello, langcode {name}!"

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    두 숫자를 더합니다.
    
    Args:
        a: 첫 번째 숫자
        b: 두 번째 숫자
    
    Returns:
        int: 두 숫자의 합
    """
    print(f"Adding {a} and {b}")
    return a + b

@mcp.tool()
async def get_gallery_posts(
    id: str,
    page: int = 1,
    list_num: int = 50,
    use_cache: bool = True
) -> dict:
    """
    DC Inside 갤러리의 게시글 목록을 가져옵니다.
    
    Args:
        id: 갤러리 식별자 (예: 'mabinogimobile')
        page: 페이지 번호 (기본값: 1)
        list_num: 페이지당 게시글 수 (기본값: 50)
        use_cache: 캐시된 결과 사용 여부 (기본값: True)
    
    Returns:
        dict: 갤러리 게시글 목록 정보
    """
    print(f"Fetching posts from gallery {id}, page {page}")
    
    params = {
        "id": id,
        "page": page,
        "list_num": list_num
    }
    
    try:
        data = await fetch_dcinside_data("posts", params, use_cache)
        return {
            "gallery_id": id,
            "page": page,
            "posts": data.get("posts", []),
            "total_count": data.get("total_count", 0)
        }
    except Exception as e:
        print(f"Error fetching gallery posts: {e}")
        return {
            "gallery_id": id,
            "page": page,
            "posts": [],
            "error": str(e)
        }

@mcp.tool()
async def get_gallery_info(
    id: str,
    use_cache: bool = True
) -> dict:
    """
    DC Inside 갤러리의 정보를 가져옵니다.
    
    Args:
        id: 갤러리 식별자 (예: 'mabinogimobile')
        use_cache: 캐시된 결과 사용 여부 (기본값: True)
    
    Returns:
        dict: 갤러리 정보
    """
    print(f"Fetching info for gallery {id}")
    
    params = {
        "id": id
    }
    
    try:
        data = await fetch_dcinside_data("info", params, use_cache)
        return {
            "gallery_id": id,
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "total_posts": data.get("total_posts", 0),
            "total_comments": data.get("total_comments", 0),
            "created_at": data.get("created_at", ""),
            "last_updated": data.get("last_updated", "")
        }
    except Exception as e:
        print(f"Error fetching gallery info: {e}")
        return {
            "gallery_id": id,
            "error": str(e)
        }


if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    try:
        mcp.run(
            host="127.0.0.1",
            port=9000,
            transport="streamable-http",
            log_level="warning"
        )
    except Exception as e:
        if "ClosedResourceError" not in str(e):
            raise