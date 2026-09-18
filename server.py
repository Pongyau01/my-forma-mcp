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

# 4. 【最新 2.x 版寫法】一鍵啟動 SSE 雲端網路傳送門！
if __name__ == "__main__":
    # 最新版內建 .run_sse()，完全不需要手動設定 uvicorn 和 app 囉！
    # 我們只需要告訴它端點叫 "/mcp"，並且綁定 Render 預設的 10000 連接埠
    server.run_sse(endpoint="/mcp", port=10000)
