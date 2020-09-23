#1.支持 python3.x 不支持python2.x

#2.安装依赖环境：
pip install -r requirements.txt

#3.description：
geventhttpclient 中的 httpclient 使用协程实现，性能相对 requests 库提升5~6倍。然后使用 events（事件）重新定义客户端，events（事件）最终会把压测中产生的数据输出到 UI 界面
