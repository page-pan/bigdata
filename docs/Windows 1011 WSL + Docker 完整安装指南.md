Windows 10/11上安装WSL和Docker的详细操作指导。

第一步：启用WSL功能

第二步：安装WSL2内核更新

第三步：安装Ubuntu发行版

第四步：安装Docker Desktop

第五步：配置Docker与WSL集成

第六步：验证安装和测试

# Windows 10/11 WSL + Docker 完整安装指南

## 第一步：启用WSL功能

### 方法一：使用管理员PowerShell命令（推荐）

1. 以管理员身份打开PowerShell
2. 执行以下命令启用WSL功能：

```powershell
# 启用WSL功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 启用虚拟机平台
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 启用Hyper-V可选组件（如果需要）
dism.exe /online /enable-feature /featurename:Microsoft-Hyper-V-All /all /norestart
```

1. 重启计算机：

```powershell
Restart-Computer
```

### 方法二：通过Windows设置界面

1. 打开"设置" → "应用" → "可选功能"
2. 点击"查看更多Windows功能"
3. 勾选以下选项：
   - ✅ 适用于Linux的Windows子系统
   - ✅ 虚拟机平台
4. 点击"确定"并重启电脑

## 第二步：安装WSL2内核更新包

1. 下载WSL2 Linux内核更新包：
   - 访问微软官方下载页面：https://aka.ms/wsl2kernel
   - 或直接下载：https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
2. 运行下载的MSI安装包，按提示完成安装
3. 设置WSL2为默认版本：

```powershell
wsl --set-default-version 2
```

## 第三步：安装Ubuntu发行版

### 方法一：通过Microsoft Store安装（最简单）

1. 打开Microsoft Store
2. 搜索"Ubuntu"（建议选择最新版本如Ubuntu 22.04 LTS）
3. 点击"获取"进行安装
4. 安装完成后，在开始菜单中点击Ubuntu图标启动
5. 首次运行时设置用户名和密码

### 方法二：使用命令行安装

```powershell
# 查看可用的Linux发行版
wsl --list --online

# 安装Ubuntu（选择合适的版本）
wsl --install -d Ubuntu-22.04

# 或者安装默认的Ubuntu
wsl --install
```

### Ubuntu基础配置

首次启动Ubuntu后执行：

```bash
# 更新包列表
sudo apt update

# 升级已安装的包
sudo apt upgrade -y

# 安装常用工具
sudo apt install -y curl wget vim git net-tools dnsutils
```

## 第四步：安装Docker Desktop

### 下载和安装Docker Desktop

1. 访问Docker官网下载页面：
   https://www.docker.com/products/docker-desktop/
2. 下载适用于Windows的Docker Desktop安装包
3. 以管理员身份运行安装程序：
   - 勾选"Use WSL 2 instead of Hyper-V"（推荐）
   - 其他选项保持默认即可
   - 完成安装后重启计算机

### Docker Desktop重要设置

安装完成后：

1. 启动Docker Desktop
2. 点击系统托盘中的Docker图标
3. 选择"Settings" → "Resources" → "WSL Integration"
4. 启用与Ubuntu的集成：
   - 打开"Enable integration with my default WSL distro"
   - 选择已安装的Ubuntu发行版

## 第五步：配置Docker与WSL集成

### 在Ubuntu中配置Docker客户端

1. 进入WSL Ubuntu环境：

```bash
wsl -d Ubuntu-22.04
```

1. 安装Docker客户端工具：

```bash
# 添加Docker官方GPG密钥
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

# 添加Docker仓库
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker客户端
sudo apt update
sudo apt install -y docker-ce-cli
```

1. 配置Docker上下文：

```bash
# 创建Docker上下文指向Windows Docker Desktop
docker context create desktop-windows --docker host=tcp://localhost:2375

# 设置为默认上下文
docker context use desktop-windows
```

### 验证WSL与Docker连接

```bash
# 测试Docker是否能正常工作
docker version
docker info

# 运行测试容器
docker run hello-world
```

## docker镜像下载优化配置

为了加速 Docker 镜像的拉取速度，可以配置国内镜像源。以下是针对不同平台的配置方法。

Linux 系统配置

**创建配置文件** 执行以下命令创建或编辑 Docker 的配置文件：

sudo mkdir -p /etc/docker

sudo vim /etc/docker/daemon.json


**添加镜像源** 在 *daemon.json* 文件中添加以下内容（可根据需要替换镜像地址）：

{

"registry-mirrors": [

"https://docker.xuanyuan.me",

"https://hub-mirror.c.163.com",

"https://docker.m.daocloud.io"

]

}

**重启 Docker 服务** 保存文件后，执行以下命令使配置生效：

sudo systemctl daemon-reload

sudo systemctl restart docker


Windows/macOS 配置

**打开设置** 右键点击任务栏中的 Docker 图标，选择 **Settings** → **Docker Engine**。

**修改 JSON 配置** 在配置框中添加如下内容：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "registry-mirrors": [
    "https://fba18z6h.mirror.aliyuncs.com",
    "https://docker.1ms.run",
    "https://docker.mirrors.ustc.edu.cn",
    "https://swr.cn-south-1.myhuaweicloud.com",
    "https://hub-mirror.c.163.com",
    "https://docker.m.daocloud.io",
    "https://mirror.baidubce.com",
    "https://docker.imgdb.de",
    "https://docker.xuanyuan.me",
    "https://xuanyuan.cloud"
  ]
}
```

**重启 Docker** 点击 **Apply & Restart**，等待 Docker 重启完成。

临时使用镜像源

无需修改全局配置，可直接在拉取镜像时指定镜像源：

docker pull docker.xuanyuan.me/library/nginx:latest


验证配置是否生效

检查镜像源是否生效：

docker info | grep "Registry Mirrors"


测试拉取速度对比：

time docker pull nginx:latest


推荐国内镜像源列表

轩辕镜像: *https://docker.xuanyuan.me*

阿里云: *https://<你的ID>.mirror.aliyuncs.com*

网易云: *http://hub-mirror.c.163.com*

中国科技大学: *https://docker.mirrors.ustc.edu.cn*

通过以上方法，Docker 镜像拉取速度可显著提升，有效优化开发效率！



## 第六步：验证安装和测试

### 全面验证测试

#### 1. WSL功能测试

```powershell
# 检查WSL版本
wsl --list --verbose

# 检查默认WSL版本
wsl --status
```

#### 2. Docker功能测试

```bash
# 在Ubuntu中测试基本Docker命令
docker --version
docker ps
docker images

# 运行Nginx测试容器
docker run -d -p 8080:80 --name nginx-test nginx

# 验证容器运行状态
docker ps

# 测试访问（在浏览器中访问 http://localhost:8080）
curl http://localhost:8080
```

#### 3. 文件系统互通测试

```bash
# Windows到WSL路径映射测试
# 在PowerShell中创建测试文件
echo "Hello from Windows" > C:\temp\test.txt

# 在WSL中访问Windows文件
cat /mnt/c/temp/test.txt

# WSL到Windows的访问测试
echo "Hello from WSL" > ~/test-wsl.txt
# 在PowerShell中查看
type \\wsl$\Ubuntu-22.04\home\$env:USERNAME\test-wsl.txt
```

#### 4. 性能基准测试

```bash
# CPU性能测试
time echo "scale=5000; 4*a(1)" | bc -l

# 磁盘I/O测试
dd if=/dev/zero of=testfile bs=1M count=1000
```

### 常见问题排查

#### 问题1：Docker无法连接

```bash
# 检查Docker Desktop是否运行
    Get-Process dockerd -ErrorAction SilentlyContinue

# 重启Docker服务
Get-Service com.docker.service | Restart-Service
```

#### 问题2：WSL发行版问题

```bash
# 重置WSL
wsl --unregister Ubuntu-22.04
wsl --install -d Ubuntu-22.04
```

#### 问题3：网络连接问题

```bash
# 在WSL中检查网络
ip addr show
ping google.com

# 重置网络适配器
netsh winsock reset
netsh int ip reset
```

### 优化建议

1. 内存分配优化

   ：

   - 在Docker Desktop设置中调整WSL资源限制
   - 建议：CPU 4核心，内存 8GB

2. **磁盘空间管理**：

```bash
# 清理Docker无用镜像和容器
docker system prune -a

# 检查WSL磁盘使用情况
wsl --list --verbose
```

1. **开发环境配置**：

```bash
# 安装开发常用工具
sudo apt install -y python3-pip nodejs npm build-essential

# 配置Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

现在您的Windows 10/11系统已经成功配置了WSL和Docker环境！这个环境将完美支持您之前规划的大数据分析系统的容器化部署。