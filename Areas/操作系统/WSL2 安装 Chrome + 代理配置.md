
  1. 检查 GUI 支持
  ls /mnt/wslg/ && echo $DISPLAY
  # 有输出即支持

  2. 安装 Chrome
  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg
  echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
  sudo apt update && sudo apt install -y google-chrome-stable

  3. 代理配置（终端）
  # ~/.bashrc 添加
  export http_proxy="http://127.0.0.1:10090"
  export https_proxy="http://127.0.0.1:10090"

  4. 代理配置（Chrome GUI）
  # 启动命令
  google-chrome --proxy-server="http://127.0.0.1:10090"

  # 或创建快捷脚本
  echo 'google-chrome --proxy-server="http://127.0.0.1:10090" "$@"' > ~/chrome-proxy.sh
  chmod +x ~/chrome-proxy.sh

  ---
  关键点
  - WSL2 localhost 可直接转发到 Windows 代理
  - 终端用环境变量，GUI 用 --proxy-server 参数
  - 代理端口根据实际软件调整