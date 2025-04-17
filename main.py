import requests
from concurrent.futures import ThreadPoolExecutor
import time


def test_proxy(proxy, proxy_type, test_url):
    proxies = {"http": f"{proxy_type}://{proxy}", "https": f"{proxy_type}://{proxy}"}
    # print(proxies)
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            # print(response.json().get('origin',{}))
            # print(response.elapsed)
            result = proxy + "      " + str(response.elapsed)
            print(result)
            return result
    except requests.RequestException:
        pass
    return None


def get_proxy(api_url, proxies):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # 检查请求是否成功
        try:
            data = response.json()
            new_proxies = data.get("data", {}).get("proxies", [])
            new_proxies = [proxy for proxy in new_proxies if proxy not in proxies]
            proxies.extend(new_proxies)
        except ValueError:
            print("API返回的数据格式不正确，无法解析JSON。")
            return
    except requests.RequestException as e:
        print(f"请求API时发生错误：{e}")
        return
    return proxies


def main():
    # 设置代理类型
    proxy_type = "http"  # 可以根据需要设置为 'http', 'https', 'socks4', 'socks5'
    print(f"代理类型：{proxy_type}")
    # 获取数量
    count = 500

    # 设置API URL和测试URL
    api_url = (
        "https://proxy.scdn.io/api/get_proxy.php?protocol=" + proxy_type + "&count="
    )
    # test_url = 'http://httpbin.org/ip'  # 替换为实际的测试URL
    # test_url = "https://github.com/"
    test_url='https://www.google.com'
    print(f"测试地址：{test_url}")

    # 从文件读取代理列表
    with open('proxies.txt', 'r') as file:
        proxies = file.read().splitlines()

    # 从API获取代理
    # proxies = []
    # if count > 20:
    #     for i in range(int(count / 20)):
    #         get_proxy(api_url + str(20), proxies)
    #         time.sleep(5)  # 延迟时间，单位秒
    #     if count % 20 > 0:
    #         get_proxy(api_url + str(count % 20), proxies)
    # else:
    #     get_proxy(api_url + str(count), proxies)

    # print(f"总共获取到 {len(proxies)} 个代理。")

    # 初始化结果列表
    results = []

    # 进行并发测试
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for proxy in proxies:
            futures.append(executor.submit(test_proxy, proxy, proxy_type, test_url))

        for future in futures:
            working_proxy = future.result()
            if working_proxy:
                results.append(working_proxy)

    # 输出测试结果
    working_proxies = len(results)
    print(
        f"总共 {len(proxies)} 个代理中，有 {working_proxies} 个 {proxy_type} 代理是可用的。"
    )
    # for proxy in results:
    #     print(proxy)


if __name__ == "__main__":
    main()
