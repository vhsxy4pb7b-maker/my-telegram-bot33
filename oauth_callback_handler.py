"""OAuth 回调处理 - 帮助提取访问令牌"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


@app.get("/oauth/callback", response_class=HTMLResponse)
async def oauth_callback(request: Request):
    """处理 OAuth 回调并显示访问令牌"""
    # 获取 URL fragment（# 后面的部分）
    fragment = request.url.fragment

    if fragment:
        # 解析参数
        from urllib.parse import parse_qs
        params = parse_qs(fragment)

        if 'access_token' in params:
            access_token = params['access_token'][0]
            expires_in = params.get('expires_in', ['N/A'])[0]
            token_type = params.get('token_type', ['bearer'])[0]

            # 生成 HTML 页面显示令牌
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Facebook OAuth 回调</title>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 50px auto;
                        padding: 20px;
                        background: #f5f5f5;
                    }}
                    .container {{
                        background: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    h1 {{
                        color: #1877f2;
                    }}
                    .success {{
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        color: #155724;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 20px 0;
                    }}
                    .token {{
                        background: #f8f9fa;
                        padding: 15px;
                        border-radius: 5px;
                        word-break: break-all;
                        font-family: monospace;
                        margin: 10px 0;
                    }}
                    .button {{
                        background: #1877f2;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        margin: 5px;
                    }}
                    .button:hover {{
                        background: #166fe5;
                    }}
                    .info {{
                        background: #d1ecf1;
                        border: 1px solid #bee5eb;
                        color: #0c5460;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 20px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>✅ Facebook OAuth 授权成功！</h1>
                    
                    <div class="success">
                        <strong>访问令牌已获取</strong>
                    </div>
                    
                    <h3>访问令牌信息：</h3>
                    <div class="token" id="token">{access_token}</div>
                    
                    <div class="info">
                        <strong>令牌类型:</strong> {token_type}<br>
                        <strong>过期时间:</strong> {expires_in} 秒 ({int(expires_in) // 86400 if expires_in != 'N/A' and expires_in.isdigit() else 'N/A'} 天)
                    </div>
                    
                    <h3>下一步操作：</h3>
                    <ol>
                        <li>复制上面的访问令牌</li>
                        <li>运行以下命令提取并保存：</li>
                    </ol>
                    
                    <div class="token">
                        python extract_token.py "{request.url}"
                    </div>
                    
                    <p>或手动编辑 .env 文件添加：</p>
                    <div class="token">
                        FACEBOOK_ACCESS_TOKEN={access_token}
                    </div>
                    
                    <h3>提示：</h3>
                    <ul>
                        <li>这是短期令牌（1-2小时）</li>
                        <li>建议交换为长期令牌（60天）</li>
                        <li>运行: <code>python exchange_token.py</code></li>
                    </ul>
                </div>
                
                <script>
                    // 自动复制功能
                    function copyToken() {{
                        const token = document.getElementById('token').textContent;
                        navigator.clipboard.writeText(token).then(() => {{
                            alert('访问令牌已复制到剪贴板！');
                        }});
                    }}
                </script>
            </body>
            </html>
            """
            return html
        else:
            return """
            <html>
            <body>
                <h1>OAuth 回调</h1>
                <p>未找到访问令牌，请检查 URL 是否正确。</p>
            </body>
            </html>
            """
    else:
        return """
        <html>
        <body>
            <h1>OAuth 回调</h1>
            <p>等待 Facebook 重定向...</p>
            <p>如果授权成功，这里会显示访问令牌。</p>
        </body>
        </html>
        """

if __name__ == "__main__":
    print("=" * 60)
    print("OAuth 回调处理器")
    print("=" * 60)
    print("\n服务将在 http://localhost:8000/oauth/callback 监听")
    print("授权成功后，Facebook 会重定向到这里")
    print("页面会自动显示访问令牌信息")
    print("\n按 Ctrl+C 停止服务")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000)
