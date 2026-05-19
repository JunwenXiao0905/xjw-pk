---
paths:
  - "**/app/**/*.py"
  - "**/fastapi/**/*.py"
  - "**/*_api.py"
---
# FastAPI 规则

FastAPI 项目除通用 Python 规则外，还需遵守以下规则。

## 结构

- 将应用构建放在 `create_app()` 中。
- 保持 router 简洁；将持久化和业务行为移至 service 或 CRUD helper。
- 分离请求 schema、更新 schema 和响应 schema。
- 将数据库会话和认证放在 dependencies 中。

## 异步

- 执行 I/O 的端点使用 `async def`。
- 异步端点中使用异步数据库和 HTTP 客户端。
- 异步路由中禁止调用 `requests`、同步 SQLAlchemy 会话或阻塞文件/网络操作。

## 依赖注入

```python
@router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ...
```

路由处理器内禁止创建 `SessionLocal()` 或长生命周期客户端。

## Schema

- 响应模型中禁止包含密码、密码哈希、access tokens、refresh tokens 或内部认证状态。
- 返回应用数据的端点使用 `response_model`。
- Pydantic 能表达的规则使用字段约束而非手写验证。

## 安全

- CORS origins 保持环境特定。
- 禁止组合通配符 origins 与带凭证 CORS。
- 验证 JWT expiry、issuer、audience 和 algorithm。
- 对认证和高写入端点启用速率限制。
- 从日志中脱敏凭证、cookies、authorization headers 和 tokens。

## 测试

- Override `Depends` 使用的确切依赖。
- 测试后清除 `app.dependency_overrides`。
- 异步应用优先使用异步测试客户端。

参见 skill：`fastapi-patterns`。