
## 1. 检查是否已有 SSH Key

先看当前用户目录下是否已有 `.ssh` 和现成密钥。

```powershell
Get-ChildItem $HOME\.ssh
```

如果看到类似文件：

```text
id_rsa
id_rsa.pub
id_ed25519
id_ed25519.pub
```

说明你之前生成过 SSH Key。

需要注意：

- `.pub` 是公钥，可以加到 GitHub / GitLab
- 没有 `.pub` 后缀的是私钥，不能泄露
- 如果已经有公司账号在用的 key，个人仓库最好单独再建一把，不要混用


## 2. 生成新的 SSH Key

现在更常见的是用 `ed25519`，比传统 `rsa` 更简洁。

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

如果你想给不同平台或不同身份分开管理，建议显式指定文件名：

```powershell
ssh-keygen -t ed25519 -C "3249554887@qq.com" -f "$HOME\.ssh\github_personal_ed25519"
```

执行后会问两件事：

1. 密钥保存路径  
默认回车即可；如果要和公司 key 区分，建议自定义名字。

2. passphrase  
可留空；如果设置了，每次使用时都需要解锁，或者依赖 `ssh-agent`。

生成后通常会得到：

```text
~/.ssh/github_personal_ed25519
~/.ssh/github_personal_ed25519.pub
```


## 3. 启动 SSH Agent 并添加密钥

如果你给私钥设置了口令，或者想统一由 agent 管理，可以这样做。

查看 agent：

```powershell
Get-Service ssh-agent
```

启动 agent：

```powershell
Set-Service ssh-agent -StartupType Manual
Start-Service ssh-agent
```

把私钥加进去：

```powershell
ssh-add "$HOME\.ssh\github_personal_ed25519"
```

查看当前已加载的 key：

```powershell
ssh-add -l
```

如果私钥没有口令，也可以不依赖 agent，直接在 SSH 配置里指定 `IdentityFile`。


## 4. 复制 SSH 公钥

直接查看公钥：

```powershell
Get-Content "$HOME\.ssh\github_personal_ed25519.pub"
```

复制到剪贴板：

```powershell
Get-Content "$HOME\.ssh\github_personal_ed25519.pub" | Set-Clipboard
```

要复制的是 `.pub` 文件内容，不是私钥文件。


## 5. 添加 SSH Key 到 GitHub / GitLab

### GitHub

路径：

`Settings -> SSH and GPG keys -> New SSH key`

填写时：

- `Title`：随便写，能看懂设备来源即可，比如 `Windows-Laptop`
- `Key type`：`Authentication Key`
- `Key`：粘贴 `.pub` 文件内容


## 6. 测试 SSH 连接

GitHub：

```powershell
ssh -T git@github.com
```

如果成功，通常会看到：

```text
Hi <your-username>! You've successfully authenticated, but GitHub does not provide shell access.
```

如果这里仍然报：

```text
Permission denied (publickey)
```

优先检查这几项：

- 你当前终端用的是哪一个用户目录
- SSH 实际加载的是哪把私钥
- 公钥是否已经加到正确账号
- 远端地址是不是 SSH 地址


## 7. 使用 SSH 配置区分个人和公司账号

如果同一台电脑上同时有公司仓库和个人仓库，推荐用别名分开。

`~/.ssh/config` 示例：

```sshconfig
Host github-personal
    HostName github.com
    User git
    IdentityFile C:\Users\你的用户名\.ssh\github_personal_ed25519
    IdentitiesOnly yes

Host github-company
    HostName github.com
    User git
    IdentityFile C:\Users\你的用户名\.ssh\github_company_ed25519
    IdentitiesOnly yes
```

这样个人仓库可以写成：

```text
git@github-personal:your-name/your-repo.git
```

公司仓库可以写成：

```text
git@github-company:company-name/company-repo.git
```

好处是：

- 不容易串号
- 不会误用公司 key 推个人仓库
- 排错时能明确知道当前走的是哪把 key


## 8. 让仓库改用 SSH 远端

查看当前远端：

```powershell
git remote -v
```

把远端改成 SSH：

```powershell
git remote set-url origin git@github.com:your-name/your-repo.git
```

如果使用了别名：

```powershell
git remote set-url origin git@github-personal:your-name/your-repo.git
```

之后再执行：

```powershell
git fetch
git push
```


## 9. 使用 SSH 克隆仓库

不要再用 HTTPS 地址：

```powershell
git clone https://github.com/your-name/your-repo.git
```

改用 SSH 地址：

```powershell
git clone git@github.com:your-name/your-repo.git
```

如果用了别名：

```powershell
git clone git@github-personal:your-name/your-repo.git
```
