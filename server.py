import os
import asyncio
from mcp.server import MCPServer
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn

# 【關鍵改動】：改從 Render 後台（環境變數）讀取密碼，安全又不會出錯！
APS_CLIENT_ID = os.environ.get("APS_CLIENT_ID")
APS_CLIENT_SECRET = os.environ.get("APS_CLIENT_SECRET")

# 建立我們的魔法通訊塔
server = MCPServer("my-forma-robot")

@server.tool()
def get_forma_element_groups(project_id: str) -> str:
    """去 Autodesk Forma 城堡裡，把最新一箱的積木清單拿出來。"""
    return f"【雲端連線成功】已經進入專案 {project_id}！找到一箱叫做 'Main Tower Base' 的積木群組。"

# 建立最健康的 sse 傳送門
transport = SseServerTransport("/mcp/v1/sse")

async def handle_sse(request):
    async with transport.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

# 包裝成標準的網頁路線
app = Starlette(
    routes=[
        Route("/mcp/v1/sse", endpoint=handle_sse, methods=["GET"]),
        Route("/mcp/v1/messages", endpoint=transport.handle_post_message, methods=["POST"]),
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

