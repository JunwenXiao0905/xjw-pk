# 常用模式

## Skeleton 项目

实现新功能时：
1. 搜索久经考验的 skeleton 项目
2. 使用并行 agent 评估选项：
   - 安全评估
   - 可扩展性分析
   - 相关性评分
   - 实现规划
3. Clone 最佳匹配作为基础
4. 在已验证的结构内迭代

## 设计模式

### Repository 模式

将数据访问封装在一致的接口后：
- 定义标准操作：findAll、findById、create、update、delete
- 具体实现处理存储细节（数据库、API、文件等）
- 业务逻辑依赖抽象接口，而非存储机制
- 支持轻松切换数据源，简化 mock 测试

### API 响应格式

对所有 API 响应使用统一的封装结构：
- 包含 success/status 指示符
- 包含数据载荷（错误时可空）
- 包含错误消息字段（成功时可空）
- 分页响应包含元数据（total、page、limit）