@echo off
chcp 65001
set /p tag="Please input container tag: "
set /p message="Please input commit message: "
set image_name="porkerll/libm:%tag%"
set commit_messgae="%message%"

git add .
git commit -m %commit_messgae%
git push github master:main

echo --------正在构建镜像 - %image_name%------------------------
docker build -t %image_name% .
echo --------镜像 %image_name% 构建完成-------------------------
echo --------镜像 %image_name% 准备上传-------------------------
docker push %image_name%
echo --------镜像 %image_name% 上传完成-------------------------