

# 3. 请求体解析机制 (Pydantic & Dataclass)
FastAPI 会根据路由函数的参数类型注解，自动解析请求体 JSON 并实例化模型。这一过程发生在你的函数代码执行之前。



  FastAPI 只能自动实例化带有结构化字段元数据的类：

```python
  ┌────────────────────┬─────────────────────────────────────────┬───────────────────────────┐
  │        类型        │                  示例                   │           能力            │
  ├────────────────────┼─────────────────────────────────────────┼───────────────────────────┤
  │ Pydantic BaseModel │ class NoteCreate(BaseModel): title: str │ ✅ 解析 + 验证 + 错误信息 │
  ├────────────────────┼─────────────────────────────────────────┼───────────────────────────┤
  │ dataclass          │ @dataclass class NoteCreate: title: str │ ✅ 解析（不做强类型验证） │
  ├────────────────────┼─────────────────────────────────────────┼───────────────────────────┤
  │ 普通 class         │ class NoteCreate: def __init__...       │ ❌ 不支持                 │
  └────────────────────┴─────────────────────────────────────────┴───────────────────────────┘
```



为什么普通类不支持？

  普通类的 **init** 里可以写任意逻辑（查库、计算、调用 API），FastAPI 无法预知如何把 JSON  
  映射到它上面。Pydantic 和 dataclass 则通过 **annotations** 暴露了字段和类型信息，FastAPI  
  能读取并自动实例化。



  执行流

  浏览器 POST /notes，Body: {"title": "hello"}  
         ↓  
  FastAPI 读取签名: def create(note: NoteCreate)  
         ↓  
  FastAPI 解析 JSON → dict  
         ↓  
  实例化: NoteCreate(title="hello")  ← 验证在这里发生  
         ↓  
  验证通过 → 调用你的函数: create(note=NoteCreate实例)  
  验证失败 → 直接返回 422，你的函数不执行

  关键点

+ 实例化由 FastAPI 在幕后完成，不是 Python 原生语法。Python 的类型注解本身只起标注作用。
+ 一个路由函数只能有一个 Pydantic/Dataclass 参数（一个请求体）。
+ 函数内拿到的参数已经是实例化后的对象，可直接调用 .model_dump() 等方法。

#   4. FastAPI 异常处理
## 4.1 伪代码
```python
  # FastAPI 内部实现（伪代码）
class FastAPI:
      handlers = {}

      def exception_handler(self, exc_type):
          def decorator(func):
              self.handlers[exc_type] = func   # 注册 handler
              return func
          return decorator

      # 处理请求时：
      def handle_request(self, request):
          try:
              response = route_handler(request)
          except Exception as exc:
              # 按异常类型找 handler
              handler = self.handlers.get(type(exc))
              if handler:
                  return handler(request, exc)
              # 没匹配到，返回 500
              return JSONResponse(status_code=500, content={"detail": str(exc)})
```



##   4.2. 完整流程
```python
  @app.exception_handler(NotFoundException)     ← 注册：NotFoundException → handler
  async def not_found_handler(request, exc):
      return JSONResponse(status_code=404, ...)

  notes.py:
      raise NotFoundException("Note")           ← 抛出异常
```

  FastAPI:

      捕获异常 → type(exc) 是 NotFoundException

      → 找到 handler → 调用 not_found_handler(request, exc)

      → 返回 JSONResponse

