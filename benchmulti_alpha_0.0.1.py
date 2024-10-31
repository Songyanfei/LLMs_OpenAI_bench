from openai import OpenAI
import threading
import time

# 初始化客户端
client = OpenAI(
    base_url="http://192.168.3.53:18127/v1",
    api_key="token-abc123",
)

# 定义全局存储
results = {
    "total_time_accumulated": 0,
    "decode_time_accumulated": 0,
    "total_encoded_words": 0,
    "total_decoded_words": 0,
    "first_token_times": [],
    "count": 0
}

# 锁对象，用于线程同步写入数据
lock = threading.Lock()

def send_request():
    content = "请你讲一个4000字的故事..."
    start_time = time.time()

    # 开启流式传输
    stream = client.chat.completions.create(
        model="kaiwu",
        messages=[
            {"role": "system", "content": "你是个很有帮助的chat助手, 请你回答我的问题."},
            {"role": "user", "content": content}
        ],
        max_tokens=4096,
        stream=True
    )

    encoded_words = len(content)
    first_token_received = False
    decoded_words = 0
    for response in stream:
        if not first_token_received:
            first_token_time = time.time() - start_time
            with lock:
                results["first_token_times"].append(first_token_time)
            first_token_received = True
        
        if hasattr(response, 'choices') and response.choices:
            current_text = response.choices[0].delta.content if response.choices[0].delta else ""
            decoded_words += len(current_text)

    end_time = time.time()
    total_time = end_time - start_time
    decode_time = end_time - start_time

    # 更新全局结果
    with lock:
        results["total_time_accumulated"] += total_time
        results["decode_time_accumulated"] += decode_time
        results["total_encoded_words"] += encoded_words
        results["total_decoded_words"] += decoded_words
        results["count"] += 1

# 创建并启动线程
threads = []
num_requests = 10
for _ in range(num_requests):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

# 计算平均结果
average_first_token_time = sum(results["first_token_times"]) / results["count"]
average_total_time = results["total_time_accumulated"] / results["count"]
average_decode_time = (results["decode_time_accumulated"] / results["count"]) - average_first_token_time
average_encoded_words = results["total_encoded_words"] / results["count"]
average_decoded_words = results["total_decoded_words"] / results["count"]
average_encoding_speed = results["total_encoded_words"] / results["total_time_accumulated"]
average_decoding_speed = results["total_decoded_words"] / results["decode_time_accumulated"]

# 让我看起来开心一点
total_encoding_speed = average_encoding_speed * num_requests
total_decoding_speed = average_decoding_speed * num_requests

# 输出结果
print(f"Average first token response time: {average_first_token_time:.2f} seconds")
print(f"Average total response time: {average_total_time:.2f} seconds")
print(f"Average decode time: {average_decode_time:.2f} seconds")
print(f"Average encoded words per request: {average_encoded_words:.2f}")
print(f"Average decoded words per request: {average_decoded_words:.2f}")
print(f"Average encoding speed: {average_encoding_speed:.2f} words per second")
print(f"Average decoding speed: {average_decoding_speed:.2f} words per second")
print(f"Total encoding speed: {total_encoding_speed:.2f} words per second")
print(f"Total decoding speed: {total_decoding_speed:.2f} words per second")

