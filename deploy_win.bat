@echo off
chcp 65001
set image_name="porkerll/libm:5.0"
echo --------正在构建镜像 - %image_name%----------
docker build -t %image_name% .
echo --------镜像构建完成-------------------------
docker push %image_name%
echo --------镜像上传完成-------------------------