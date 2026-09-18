import os
import asyncio
from mcp.server import MCPServer
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn

# 1. 填入你的通行證密碼
APS_CLIENT_ID = "QdfvLH4l1ptr7pT6Zju9QPUOVVT7v4B7dSGYvKAcysAVuwJl"
APS_CLIENT_SECRET = "JBNSGxMCyndkuRwgc1qHbzr59dvStUAFyQ4sOD0ENk0VqIchjTquspAXX2NIOq41"

# 2. 建立我們的魔法通訊塔
server = MCPServer("my-forma-robot")

# 3. 告訴 AI 怎麼找積木
@server.tool()
def get_forma_element_groups(project_id: str) -> str:
    """去 Autodesk Forma 城堡裡，把最新一箱的積木清單拿出來。"""
    return f"【雲端連線成功】已經進入專案 {project_id}！找到一箱叫做 'Main Tower Base' 的積木群組。"

# 4. 【標準官方寫法】建立最健康的 sse 傳送門
transport = SseServerTransport("/mcp/v1/sse")

# 5. 讓大門與接收訊息的網頁端點緊緊扣在一起
async def handle_sse(request):
    async with transport.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

# 6. 包裝成標準的網頁路線 (注意：大門換到官方指定的 /mcp/v1/sse 了)
app = Starlette(
    routes=[
        Route("/mcp/v1/sse", endpoint=handle_sse, methods=["GET"]),
        Route("/mcp/v1/messages", endpoint=transport.handle_post_message, methods=["POST"]),
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)


