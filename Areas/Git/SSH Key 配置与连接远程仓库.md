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
github_personal_ed25519
github_personal_ed25519.pub
```

说明之前已经生成过 SSH Key。

注意：

- `.pub` 是公钥，可以加到 GitHub / GitLab。
- 没有 `.pub` 后缀的是私钥，不能泄露。
- 如果已经有公司账号在用的 key，个人仓库最好单独再建一把，不要混用。


## 2. 生成新的 SSH Key

现在更常见的是 `ed25519`，比传统 `rsa` 更简洁。

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

如果你想给不同平台或不同身份分开管理，建议显式指定文件名：

```powershell
ssh-keygen -t ed25519 -C "3249554887@qq.com" -f "$HOME\.ssh\github_personal_ed25519"
```

说明：

- `-C` 是注释，通常写邮箱，方便识别。
- `-f` 是输出文件名。如果漏掉 `-f`，会报 `Too many arguments.`。
- `github_personal_ed25519` 只是本地文件名，不需要和 `git@github.com:xxx.git` 里的 `github.com` 保持任何对应关系。

执行后通常会得到：

```text
~/.ssh/github_personal_ed25519
~/.ssh/github_personal_ed25519.pub
```

如果提示输入 `passphrase`：

- 留空：使用更省事。
- 设置口令：更安全，但每次使用都要解锁，或者依赖 `ssh-agent`。


## 3. 启动 SSH Agent 并添加密钥

如果你给私钥设置了口令，或者想统一管理 key，可以用 `ssh-agent`。

先查看服务状态：

```powershell
Get-Service ssh-agent
```

如果 `StartType` 是 `Disabled`，需要先在管理员 PowerShell 里改成手动启动：

```powershell
Set-Service -Name ssh-agent -StartupType Manual
Start-Service ssh-agent
```

然后把私钥加入 agent：

```powershell
ssh-add "$HOME\.ssh\github_personal_ed25519"
```

查看当前已加载的 key：

```powershell
ssh-add -l
```

说明：

- `Disabled` 的意思是服务被禁用，直接 `Start-Service ssh-agent` 会失败。
- `Manual` 的意思是允许手动启动，不会每次开机自动运行。
- 如果私钥没有口令，也可以不依赖 agent，直接在 SSH 配置里指定 `IdentityFile`。


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

- `Title`：随便写，能看懂设备来源即可，比如 `My Windows PC`。
- `Key type`：选 `Authentication Key`。
- `Key`：粘贴 `.pub` 文件内容。


## 6. 测试 SSH 连接

GitHub：

```powershell
ssh -T git@github.com
```

如果成功，通常会看到：

```text
Hi <your-username>! You've successfully authenticated, but GitHub does not provide shell access.
```

注意：这句话虽然最后有 `does not provide shell access`，但它其实表示 SSH 认证成功了，不是报错。

如果这里仍然报：

```text
Permission denied (publickey)
```

优先检查：

- 当前终端是不是你期望的那个用户目录。
- 公钥是否已经加到了正确的 GitHub 账号。
- 私钥是否真的被 `ssh-agent` 加载了。
- 远端地址是不是 SSH 地址而不是 HTTPS 地址。


## 7. 使用 SSH 配置指定 GitHub 使用哪把 Key

如果同一台电脑上同时有多把 key，建议写 `~/.ssh/config`。

单账号场景也可以这样写：

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/github_personal_ed25519
  IdentitiesOnly yes
```

说明：

- `IdentityFile` 指定连接 GitHub 时要用哪把私钥。
- `IdentitiesOnly yes` 表示只使用这把 key，避免 SSH 乱试其他 key。

Windows 上要特别注意：

- 文件名必须叫 `config`，不能叫 `config.txt`。
- 可以用下面命令确认：

```powershell
Test-Path $HOME\.ssh\config
Get-Content $HOME\.ssh\config
```

如果你需要区分个人和公司账号，也可以用别名：

```sshconfig
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/github_personal_ed25519
  IdentitiesOnly yes

Host github-company
  HostName github.com
  User git
  IdentityFile ~/.ssh/github_company_ed25519
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

补充理解：

- 这不是改 GitHub 的真实地址，而是把 SSH 连接里的主机名从 `github.com` 换成了你在 `~/.ssh/config` 里定义的别名。
- 如果你只有一个 GitHub 账号，通常不需要这样做。直接把 `Host github.com` 绑定到你的那把 key 即可，远端地址继续保持 `git@github.com:your-name/your-repo.git`。
- 只有在“个人账号 / 公司账号”都要在同一台电脑上长期共存时，才更推荐用 `github-personal`、`github-company` 这种别名方案。


## 8. `ssh -T` 成功，但 `git clone` 仍然失败时怎么排查

这是一类很常见的现象：

- `ssh -T git@github.com` 成功。
- 但 `git clone git@github.com:xxx/yyy.git` 仍然报 `Permission denied (publickey)`。

这通常说明：

- SSH agent 里虽然有正确 key，
- 但 Git 触发的 SSH 连接没有稳定使用到那把 key，
- 或者 `~/.ssh/config` 没有真正生效。

建议按这个顺序查：

1. 看 `config` 文件是不是写成了 `config.txt`。
2. 看 agent 里是否真的有那把 key。
3. 用调试日志看 SSH 实际尝试了哪把 key。

```powershell
ssh-add -l
ssh -vT git@github.com
```

如果日志里出现类似内容：

```text
Offering public key: ...github_personal_ed25519
Authenticated to github.com ... using "publickey"
```

说明 key 本身是可用的。

如果 `ssh -T` 成功，但 `git ls-remote` 或 `git clone` 失败，再执行：

```powershell
git ls-remote git@github.com:your-name/your-repo.git
```

结果判断：

- 如果能返回 commit 哈希，说明 SSH 和仓库权限都正常。
- 如果还是失败，继续检查仓库地址是否正确、仓库是否存在、当前账号是否有访问权限。


## 9. 让仓库改用 SSH 远端

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


## 10. 使用 SSH 克隆仓库

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


## 11. 这次踩坑记录

这次 Windows 场景里实际遇到的坑有：

- `ssh-keygen` 命令漏了 `-f`，导致 `Too many arguments.`。
- `ssh-agent` 服务是 `Disabled`，所以一开始无法启动。
- `~/.ssh/config` 被保存成了 `config.txt`，导致 SSH 配置没有生效。
- `ssh -T` 成功并不自动等于 `git clone` 一定成功，仍然要检查仓库地址和权限。

以后如果又遇到 `Permission denied (publickey)`，优先看这四项，通常能很快定位。
