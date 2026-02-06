@echo off
echo 正在启动大数据教学演示系统...
echo.

REM 检查Docker是否运行
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Docker未运行，请启动Docker Desktop
    pause
    exit /b 1
)

REM 停止并清理旧容器和卷
echo 清理旧容器和卷...
docker-compose down -v

REM 启动所有服务
echo 启动Docker容器...
docker-compose up -d

REM 等待服务启动
echo 等待服务启动（30秒）...
timeout /t 30 /nobreak >nul

echo.
echo ========================================
echo 大数据智能分析系统已启动！
echo ========================================
echo.
echo 访问地址：
echo Web应用：     http://localhost:5000
echo Jupyter Notebook： http://localhost:8888
echo Hadoop NameNode UI： http://localhost:9870
echo Spark Master UI：  http://localhost:8080
echo MySQL数据库：   localhost:3306 (用户: demo, 密码: demopassword)
echo.
echo 停止系统：运行 stop.bat
echo.
pause