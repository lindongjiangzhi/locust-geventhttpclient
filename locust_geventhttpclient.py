from locust import HttpLocust, TaskSet, task, between, events
import time,json,sys,socket,os
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL


# 请求的域名或ip地址
host = 'http://10.1.62.133'
# 任务
class UserTsak(TaskSet):
    def on_start(self):
        '''初始化数据'''
        url = URL(host)
        # 若为https请求，ssl设置为True
        self.http = HTTPClient(url.host,url.port,ssl=False,connection_timeout=20,network_timeout=20)

    @task
    def test(self):
        try:
            start_time = time.time()
            # get 请求
            res = self.http.get("/sz/api2/test")
            # post 请求示例
            # body = json.dumps({"username":"admin","password":"123456"})
            # res = self.http.post("/sz/api2/login",body = body)
            data = res.read()
            end_time = time.time()
            response_time =int((end_time - start_time)*1000)
            response_length = len(data)
            assert json.loads(data)['Error'] == 0

            if res.status_code == 200:
                # 统计正常的请求
                events.request_success.fire(request_type="GET", name="test_success", response_time = response_time, response_length=response_length)

        # 统计断言失败的请求
        except AssertionError:
            end_time = time.time()
            response_time =int((end_time - start_time)*1000)
            events.request_failure.fire(request_type="GET", name="test_failure", response_time=response_time,response_length=0,
                                        exception="断言错误。status_code：{}。接口返回：{}。".format(res.status_code,json.loads(data)))

        # 统计超时异常
        except socket.timeout:
            events.locust_error.fire(locust_instance=UserTsak, exception='Timeout', tb =sys.exc_info()[2])

        # 统计其他异常
        except Exception as e:
            events.locust_error.fire(locust_instance=UserTsak, exception='Error:{}。\nstatus_code：{}。\n接口返回：{}。'.format(e,res.status_code,data), tb=sys.exc_info()[2])

    def on_stop(self):
        '''运行结束，关闭http/https连接'''
        self.http.close()

class WebsiteUser(HttpLocust):
    host = host
    task_set = UserTsak
    wait_time = between(0, 0)

if __name__ == "__main__":
    # "IP地址"改成为你本机的IP
    os.system('locust -f stress_test.py --web-host IP地址 --web-port 8080')