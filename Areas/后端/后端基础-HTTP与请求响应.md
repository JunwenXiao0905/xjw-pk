# 后端基础-HTTP与请求响应

## HTTP

- HTTP 是应用层协议，用来定义客户端和服务端如何交换请求与响应。
- 一次 HTTP 交互最小包含：请求行、请求头、请求体；响应行、响应头、响应体。

## URL

- URL 表示请求地址。
- 常见组成：协议、主机、端口、路径、查询字符串。

```text
https://api.example.com:443/users/1?active=true
```

- `https`：协议
- `api.example.com`：主机
- `443`：端口
- `/users/1`：路径
- `active=true`：查询参数

## 请求方法

- `GET`：读取资源
- `POST`：创建资源或提交动作
- `PUT`：整体更新资源
- `PATCH`：局部更新资源
- `DELETE`：删除资源

## 状态码

- `2xx`：请求成功
- `3xx`：重定向
- `4xx`：客户端请求有问题
- `5xx`：服务端处理失败

常见状态码：

- `200 OK`：成功
- `201 Created`：创建成功
- `204 No Content`：成功但无响应体
- `400 Bad Request`：参数错误
- `401 Unauthorized`：未认证
- `403 Forbidden`：已认证但无权限
- `404 Not Found`：资源不存在
- `500 Internal Server Error`：服务端异常

## Header

- Header 用来携带附加元数据。
- 常见请求头：
  - `Authorization`
  - `Content-Type`
  - `Accept`
  - `Cookie`
- 常见响应头：
  - `Content-Type`
  - `Set-Cookie`
  - `Cache-Control`
  - `Location`

## Cookie

- Cookie 是浏览器保存的一小段键值数据。
- 服务端通过 `Set-Cookie` 下发，浏览器后续通过 `Cookie` 请求头回传。
- Cookie 常用于保存 Session ID，而不是直接保存完整用户状态。

## Content-Type

- `Content-Type` 用来声明请求体或响应体的数据格式。
- 后端处理参数前，先看 `Content-Type` 决定如何解析 body。

常见类型：

- `application/json`
- `application/x-www-form-urlencoded`
- `multipart/form-data`
- `text/plain`

## JSON

- `application/json` 是前后端 API 最常见的数据格式。
- 适合结构化数据传输，不适合直接带文件内容。

```json
{
  "name": "alice",
  "age": 18
}
```

## x-www-form-urlencoded

- `application/x-www-form-urlencoded` 是传统表单编码格式。
- 数据会被编码成查询字符串形态放进请求体。

```text
name=alice&age=18
```

## multipart/form-data

- `multipart/form-data` 主要用于文件上传。
- 请求体会被拆成多个 part，每个 part 都有自己的头和内容。
- 一个请求里可以同时包含文件字段和普通字段。

## HTTP/1.1

- 基于文本报文。
- 一个请求对应一个响应。
- 支持长连接，但同一连接上的并发能力有限。

## HTTP/2

- 仍然是 HTTP 语义，但传输层改成二进制分帧。
- 一个连接内可以复用多个请求与响应。
- 重点是多路复用、头部压缩、减少队头阻塞。

## HTTP/3

- HTTP/3 基于 QUIC，而不是 TCP。
- 目标是降低连接建立和丢包场景下的延迟。
- 学习时先理解它是“更现代的传输实现”，不用一开始深究细节。

## HTTPS

- HTTPS = HTTP + TLS。
- TLS 负责加密、完整性校验、服务端身份验证。
- 没有 HTTPS，HTTP 内容可能被窃听或篡改。

## 请求到达后端后的处理顺序

1. 服务器接收连接
2. Web 服务器或框架解析 HTTP 报文
3. 路由匹配路径和方法
4. 按 `Content-Type` 解析参数
5. 执行认证和参数校验
6. 执行业务逻辑
7. 返回状态码、响应头、响应体

## 关联

- 接口如何设计：[[后端基础-API设计与OpenAPI]]
- 登录态如何附着在请求上：[[后端基础-认证与登录]]
- 服务端如何持续推送：[[后端基础-实时通信]]
