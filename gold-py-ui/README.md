# 小金子具箱

#### 介绍
小金子具箱

#### 软件架构
- 前端：Vue3，Vue-Route，Axios
- 容器：pywebview，官方文档：https://pywebview.flowrl.com/guide/usage.html#basics
- 后端：Python,Flask,requests，百度OCR


#### 项目打包为exe可执行程序教程

1.  将前端项目编译打包生成静态文件
2.  在gold-py-ui目录下执行打包脚本
```shell
python3 build.py
```

#### Python服务端-使用说明

1.  安装依赖
```shell
pip install -r requirements.txt
```
2.  进入main.py 进行运行
```shell
python3 main.py
```
3. 开发模式和运行模式
- 在main.py的main方法中，可设置开发及运行模式启动应用
- 开发模式仅用于和前端进行联调是使用
```shell
# 开发模式
# mode = 'develop'
# 运行模式
mode = 'prodution'
```

#### Vue前端-使用说明

1.  进入前端项目根目录（`gold-py-ui/view`）安装依赖
```shell
npm install
```
2.  开发时运行程序
```shell
npm run dev
```
3.  编译打包生成静态文件
```shell
npm run build
```

