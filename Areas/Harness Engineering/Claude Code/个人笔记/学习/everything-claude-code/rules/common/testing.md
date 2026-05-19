# 测试要求

## 最低测试覆盖率：80%

测试类型（全部必需）：
1. **单元测试** - 单个函数、工具、组件
2. **集成测试** - API 端点、数据库操作
3. **E2E 测试** - 关键用户流程（按语言选择框架）

## 测试驱动开发

强制流程：
1. 先写测试（RED）
2. 运行测试 - 应失败
3. 写最小实现（GREEN）
4. 运行测试 - 应通过
5. 重构（IMPROVE）
6. 验证覆盖率（80%+）

## 测试失败排查

1. 使用 **tdd-guide** agent
2. 检查测试隔离性
3. 验证 mock 正确性
4. 修复实现而非测试（除非测试有误）

## Agent 支持

- **tdd-guide** - 为新功能主动使用，强制先写测试

## 测试结构（AAA 模式）

测试优先采用 Arrange-Act-Assert 结构：

```typescript
test('calculates similarity correctly', () => {
  // Arrange
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // Assert
  expect(similarity).toBe(0)
})
```

### 测试命名

使用描述性名称说明被测试的行为：

```typescript
test('returns empty array when no markets match query', () => {})
test('throws error when API key is missing', () => {})
test('falls back to substring search when Redis is unavailable', () => {})
```