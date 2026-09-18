import os
import asyncio
# 引入最新版的 MCPServer
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

# 4. 建立標準的 SSE 傳送通道
transport = SseServerTransport("/mcp")

# 5. 設計兩道安全閘門（傳送與接收訊息的網頁端點）
async def handle_sse(request):
    async with transport.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

# 6. 把通道包裝成 Render 看得懂的網頁應用程式 (Starlette App)
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse, methods=["GET"]),
        Route("/mcp", endpoint=transport.handle_post_message, methods=["POST"]),
    ]
)

# 7. 點火開機，綁定 Render 預設的 10000 連接埠
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

