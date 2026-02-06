@echo off
echo 正在停止大数据教学演示系统...
echo.

REM 停止并删除容器
docker-compose down

echo.
echo 系统已停止。
echo.
pause