

## 3. 常用命令

### 3.1 容器管理

```bash
# 查看正在运行的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 启动/停止/重启容器
docker start <容器名>
docker stop <容器名>
docker restart <容器名>

# 删除容器（需先停止）
docker rm <容器名>

# 查看容器日志
docker logs <容器名>
docker logs -f <容器名>    # 实时跟踪
```

### 3.2 在容器内执行命令

```bash
# 执行一条命令，返回结果就结束
docker exec <容器名> <命令>

# 进入交互式终端（exit 退出）
docker exec -it <容器名> bash
```

### 3.3 镜像管理

```bash
# 查看本地镜像
docker images

# 拉取镜像
docker pull <镜像名>:<标签>      # 例: docker pull postgres:17

# 删除镜像
docker rmi <镜像名>
```

### 3.4 docker-compose 管理

```bash
# 启动所有服务（后台运行）
docker compose up -d

# 停止并删除所有服务
docker compose down

# 查看服务状态
docker compose ps
```

## 4. 实际操作示例

### 4.1 PostgreSQL 容器

```bash
# 查看容器
docker ps

# 进入容器内部
docker exec -it txwx-postgis bash

# 在容器里连数据库（不进入容器也行，直接用 docker exec）
docker exec txwx-postgis psql -U txwx -d txwx_db

# 执行 SQL 命令
docker exec txwx-postgis psql -U txwx -d txwx_db -c "CREATE DATABASE mydb;"

# 查看数据库列表
docker exec txwx-postgis psql -U txwx -d txwx_db -c "\l"

# 查看表
docker exec txwx-postgis psql -U fastapi_user -d fastapi_study -c "\dt"
```

### 4.2 典型工作流

```
本地开发需要 PostgreSQL
    │
    ▼
docker compose up -d        ← 一行命令启动 PG 容器
    │
    ▼
docker ps                   ← 确认容器在跑，记录端口号
    │
    ▼
项目 .env 里配置连接地址      ← localhost:5433
    │
    ▼
正常开发
    │
    ▼
docker compose down         ← 不需要时关闭
```
