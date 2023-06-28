import requests
import time
import matplotlib.pyplot as plt

cdn_times = []
origin_times = []
get_number =  100
for i in range(get_number):
    start_time = time.time()
    result = requests.get("https://saugau.sapphirecdn.com/static/mainpage/images/chad.jpeg")
    end_time = time.time()
    cdn_time = end_time - start_time
    start_time = time.time()
    result = requests.get("https://saugau.com/static/mainpage/images/chad.jpeg")
    end_time = time.time()
    origin_time = end_time - start_time
    cdn_times.append(cdn_time)
    origin_times.append(origin_time)

plt.title('So sánh response time khi sử dụng CDN')
plt.ylabel('Response time (s)')

plt.plot([i for i in range(get_number)], cdn_times, label="Response server CDN")
plt.plot([i for i in range(get_number)], origin_times, label="Response time server origin")
plt.legend()
plt.show()
