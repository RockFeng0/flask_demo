#!/usr/bin/env bash
# for devops deploy

# 安装包名称
APP_PAGKAGE_NAME=flask-demo-tar.zip
BASE_DIR=/opt/deploy/rtsf
UPLOAD_DIR=~/devops/upload

# 判断程序目录是否存在
if [[ ! -d ${BASE_DIR}/flask-demo ]]
then
  mkdir -p ${BASE_DIR}/flask-demo
else
  rm -rf ${BASE_DIR}/flask-demo/*
fi

# 删除原目录下的代码
if [[ -d ${UPLOAD_DIR}/workspace ]]
then
  rm -rf ${UPLOAD_DIR}/workspace
fi

# 解压程序包
cd ${UPLOAD_DIR}
unzip -o ${APP_PAGKAGE_NAME}
tar zxvf ${UPLOAD_DIR}/workspace/flask-demo.tar.gz -C ${BASE_DIR}/flask-demo


# 选择对应的虚拟环境
source ~/.bashrc
workon pydspj

# 安装依赖, 可能镜像源要自己去捣鼓一下
cd ${BASE_DIR}/flask-demo
pip install -r requirements.txt > /dev/null 1>&1

# 安装依赖, 可能镜像源要自己去捣鼓一下
supervisorctl -c /opt/soft/supervisor/supervisord.conf restart flask-demo_5002
