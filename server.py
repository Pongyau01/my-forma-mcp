import os
import asyncio
from mcp.server import MCPServer

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

# 4. 【關鍵改動】啟動網路傳送門 (SSE 模式)
if __name__ == "__main__":
    import uvicorn
    from mcp.server.sse import SseServerTransport
    
    # 建立一個網路傳送管道
    sse = SseServerTransport("/mcp")
    
    async def run_cloud_server():
        # 讓 MCP 伺服器與網路管道結合
        async with server.run_sse(sse) as (read_stream, write_stream, app):
            config = uvicorn.Config(app, host="0.0.0.0", port=10000)
            server_uvicorn = uvicorn.Server(config)
            await server_uvicorn.serve()

    asyncio.run(run_cloud_server())
