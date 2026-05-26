# 后端基础-HTTP与请求响应

## 目录

- [第1章 HTTP 基础](#第1章-http-基础)
  - [1.1 HTTP](#11-http)
  - [1.2 URL](#12-url)
  - [1.3 请求方法](#13-请求方法)
  - [1.4 状态码](#14-状态码)
- [第2章 Header 与状态附着](#第2章-header-与状态附着)
  - [2.1 Header](#21-header)
  - [2.2 Cookie](#22-cookie)
  - [2.3 Authorization](#23-authorization)
- [第3章 请求体格式](#第3章-请求体格式)
  - [3.1 Content-Type](#31-content-type)
  - [3.2 JSON](#32-json)
  - [3.3 x-www-form-urlencoded](#33-x-www-form-urlencoded)
  - [3.4 multipart-form-data](#34-multipartform-data)
  - [3.5 登录接口为什么常用 form](#35-登录接口为什么常用-form)
- [第4章 协议实现与传输](#第4章-协议实现与传输)
  - [4.1 HTTP-11](#41-http11)
  - [4.2 HTTP-2](#42-http2)
  - [4.3 HTTP-3](#43-http3)
  - [4.4 HTTPS](#44-https)
- [第5章 请求处理顺序](#第5章-请求处理顺序)
  - [5.1 请求到达后端后的处理顺序](#51-请求到达后端后的处理顺序)

## 第1章 HTTP 基础

### 1.1 HTTP

- HTTP 是应用层协议，用来定义客户端和服务端如何交换请求与响应。
- 一次 HTTP 交互最小包含：
  - 请求行
  - 请求头
  - 请求体
  - 响应行
  - 响应头
  - 响应体

### 1.2 URL

- URL 表示请求地址。
- 常见组成：
  - 协议
  - 主机
  - 端口
  - 路径
  - 查询字符串

```text
https://api.example.com:443/users/1?active=true
```

- `https`：协议
- `api.example.com`：主机
- `443`：端口
- `/users/1`：路径
- `active=true`：查询参数

### 1.3 请求方法

- `GET`：读取资源
- `POST`：创建资源或提交动作
- `PUT`：整体更新资源
- `PATCH`：局部更新资源
- `DELETE`：删除资源

### 1.4 状态码

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

## 第2章 Header 与状态附着

### 2.1 Header

- Header 用来携带附加元数据。

常见请求头：

- `Authorization`
- `Content-Type`
- `Accept`
- `Cookie`

常见响应头：

- `Content-Type`
- `Set-Cookie`
- `Cache-Control`
- `Location`

### 2.2 Cookie

- Cookie 是浏览器保存的一小段键值数据。
- 服务端通过 `Set-Cookie` 下发，浏览器后续通过 `Cookie` 请求头回传。
- Cookie 常用于保存 Session ID，而不是直接保存完整用户状态。

### 2.3 Authorization

- `Authorization` 是显式认证请求头。
- 常见格式：

```text
Authorization: Bearer <token>
```

- `Bearer` 表示后面携带的是访问令牌。
- 这种方式常见于前后端分离、移动端、开放接口。
- 它和 Cookie 的区别是：
  - Cookie 更偏浏览器自动携带
  - `Authorization` 更偏客户端显式控制

## 第3章 请求体格式

### 3.1 Content-Type

- `Content-Type` 用来声明请求体或响应体的数据格式。
- 后端处理参数前，会先看 `Content-Type` 决定如何解析 body。

常见类型：

- `application/json`
- `application/x-www-form-urlencoded`
- `multipart/form-data`
- `text/plain`

### 3.2 JSON

- `application/json` 是前后端 API 最常见的数据格式。
- 适合结构化数据传输，不适合直接带文件内容。

```json
{
  "name": "alice",
  "age": 18
}
```

### 3.3 x-www-form-urlencoded

- `application/x-www-form-urlencoded` 是传统表单编码格式。
- 数据会被编码成查询字符串形态放进请求体。

```text
name=alice&age=18
```

- 登录接口经常使用这种格式，尤其是在 OAuth2 password flow 场景下。
- 这时请求体虽然不在 URL 上，但编码形态仍然像查询字符串。

常见登录请求体：

```text
username=study_user&password=study_pass_123
```

### 3.4 multipart/form-data

- `multipart/form-data` 主要用于文件上传。
- 请求体会被拆成多个 part，每个 part 都有自己的头和内容。
- 一个请求里可以同时包含文件字段和普通字段。

### 3.5 登录接口为什么常用 form

- 登录接口不一定必须使用 `application/json`。
- 在 OAuth2 password flow 里，约定更常见的是 `application/x-www-form-urlencoded`。
- 这也是很多后端框架在“账号密码登录”场景下优先提供表单解析器的原因。

所以要区分两件事：

- 登录接口提交用户名密码时，常用 form
- 后续访问受保护接口时，常用 `Authorization: Bearer <token>`

## 第4章 协议实现与传输

### 4.1 HTTP/1.1

- 基于文本报文。
- 一个请求对应一个响应。
- 支持长连接，但同一连接上的并发能力有限。

### 4.2 HTTP/2

- 仍然是 HTTP 语义，但传输层改成二进制分帧。
- 一个连接内可以复用多个请求与响应。
- 重点是多路复用、头部压缩、减少队头阻塞。

### 4.3 HTTP/3

- HTTP/3 基于 QUIC，而不是 TCP。
- 目标是降低连接建立和丢包场景下的延迟。
- 学习时先理解它是“更现代的传输实现”，不用一开始深究细节。

### 4.4 HTTPS

- HTTPS = HTTP + TLS。
- TLS 负责加密、完整性校验、服务端身份验证。
- 没有 HTTPS，HTTP 内容可能被窃听或篡改。

## 第5章 请求处理顺序

### 5.1 请求到达后端后的处理顺序

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
