FastAPI 本身只是一个 Python 库（一堆函数），它不能自己监听端口。需要一个 HTTP 服务器来承载它。

  浏览器 ←→ uvicorn（HTTP 服务器） ←→ FastAPI（你的应用）

  uvicorn 的角色：

+ 监听 localhost:8000，接收 TCP 连接
+ 把 HTTP 请求解析成 Python 能理解的对象
+ 调用 FastAPI 的 app 处理
+ 把 FastAPI 的返回值转成 HTTP 响应返回



uv run uvicorn src.app.main:app --reload 的含义：

+ uv run — 在虚拟环境中运行
+ uvicorn — 启动 HTTP 服务器
+ src.app.main:app — 加载 src/app/main.py 里的 app 变量
+ --reload — 文件变动自动重启（开发用）



