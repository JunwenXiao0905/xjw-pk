1. **JSDoc 注释**：所有函数使用中文 JSDoc 注释。
    
2. **Fail fast and loudly**：Do not write fallback logic unless explicitly required. Throw errors immediately.
    
3. **Let errors bubble up**：Do not handle errors inside business layers. Let them bubble up to the unified error handler.
    
4. **Valid tests**：Tests must prove bugs exist by failing. Tests that only pass prove nothing.