from openai import OpenAI
import threading
import time
import argparse
import random




class Naive_bench():
    def __init__(self, model, url, port, api_key):
        # 初始化客户端
        self.client = OpenAI(
            base_url = "http://"+url+":"+port+"/v1",
            api_key = api_key,
        )
        # 定义全局存储
        self.results = {
            "total_time_accumulated": 0,
            "decode_time_accumulated": 0,
            "total_encoded_words": 0,
            "total_decoded_words": 0,
            "first_token_times": [],
            "count": 0
        }

        # 锁对象，用于线程同步写入数据
        self.lock = threading.Lock()
        self.model = model

    def send_request(self, ):
        
        start_time = time.time()

        

        # 开启流式传输
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是个很有帮助的chat助手, 请你回答我的问题."},
                {"role": "user", "content": str(random.randint(1,100)) + self.content}
            ],
            stream=True,
            max_tokens=self.fixed_out if self.fixed_out else None,
            temperature=99999 if self.fixed_out else 0.6,
        )

        encoded_words = len(self.content)
        first_token_received = False
        decoded_words = 0
        for response in stream:
            if not first_token_received:
                first_token_time = time.time() - start_time
                with self.lock:
                    self.results["first_token_times"].append(first_token_time)
                first_token_received = True
            
            if hasattr(response, 'choices') and response.choices:
                current_text = response.choices[0].delta.content if response.choices[0].delta else ""
                decoded_words += len(current_text)

        end_time = time.time()
        total_time = end_time - start_time
        decode_time = end_time - start_time

        # 更新全局结果
        with self.lock:
            self.results["total_time_accumulated"] += total_time
            self.results["decode_time_accumulated"] += decode_time
            self.results["total_encoded_words"] += encoded_words
            self.results["total_decoded_words"] += decoded_words
            self.results["count"] += 1

    def bench(self, content, num_requests, detail = False, fixed_out = False):
        self.content = content
        self.fixed_out = fixed_out
        # 创建并启动线程
        threads = []
        for _ in range(num_requests):
            thread = threading.Thread(target=self.send_request)
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 计算平均结果
        average_first_token_time = sum(self.results["first_token_times"]) / self.results["count"]
        average_total_time = self.results["total_time_accumulated"] / self.results["count"]
        average_decode_time = (self.results["decode_time_accumulated"] / self.results["count"]) - average_first_token_time
        
        if self.fixed_out:
            average_encoded_words = self.results["total_encoded_words"] / (self.results["count"] * 3)  # 输入token数为字符数/3
            average_decoded_words = self.fixed_out  # 输出token数为fixed_out指定的数量
        else:
            average_encoded_words = self.results["total_encoded_words"] / self.results["count"]
            average_decoded_words = self.results["total_decoded_words"] / self.results["count"]
            
        average_encoding_speed = self.results["total_encoded_words"] / self.results["total_time_accumulated"]
        average_decoding_speed = self.results["total_decoded_words"] / self.results["decode_time_accumulated"]

        total_encoding_speed = average_encoding_speed * num_requests
        total_decoding_speed = average_decoding_speed * num_requests

        unit = "tokens" if self.fixed_out else "words"

        # 输出结果
        print("\n" + "="*50)
        print(f"Model: {self.model}")
        if (detail):
            print(f"Test content: {self.content}")
        print(f"Concurrent requests: {num_requests}")
        print("="*50)
        print(f"Average first token response time: {average_first_token_time:.2f} seconds")
        print(f"Average total response time: {average_total_time:.2f} seconds")
        print(f"Average decode time: {average_decode_time:.2f} seconds")
        print(f"Average encoded {unit} per request: {average_encoded_words:.2f}")
        print(f"Average decoded {unit} per request: {average_decoded_words:.2f}")
        print(f"Average encoding speed: {average_encoding_speed:.2f} {unit} per second")
        print(f"Average decoding speed: {average_decoding_speed:.2f} {unit} per second")
        print(f"Total encoding speed: {total_encoding_speed:.2f} {unit} per second")
        print(f"Total decoding speed: {total_decoding_speed:.2f} {unit} per second")


if __name__ == "__main__":

    # 从命令行获取参数
    parser = argparse.ArgumentParser(description='Multi-threaded benchmark tool')
    parser.add_argument('--json_file', type=str, default='data/zh.json', help='JSONfile')
    parser.add_argument('--model', type=str, default='', help='Model name', required=True)
    parser.add_argument('--url', type=str, default='192.168.3.54', help='Server address')
    parser.add_argument('--port', '-p', type=str, default='19125', help='Server port')
    parser.add_argument('--api_key', type=str, default='token-abc123', help='API key')
    parser.add_argument('--content', '-c', type=str, default=None, help='Test content')
    parser.add_argument('--input_len', '-i', type=int, default=None, help='Input length')
    parser.add_argument('--output_len', '-o', type=int, default=None, help='Output length')
    parser.add_argument('--batch', '-b', type=int, nargs='+', default=[1], help='Number of concurrent requests')
    parser.add_argument('--detail', type=bool, default=False, help='Print request details')

    args = parser.parse_args()

    # 检查参数
    if args.content is None and (args.input_len is None or args.output_len is None):
        print("错误: 必须指定 content 或同时指定 input_len 和 output_len")
        exit(1)

    test_case = Naive_bench(args.model, args.url, args.port, args.api_key)

    # Run benchmark multiple times according to batch parameter list
    for batch_size in args.batch:
        print(f"\nStarting test with concurrency of {batch_size}...")
        
        test_content = args.content
        if test_content is None:
            # Concatenate "ops" string based on input_len, each "ops" as one token, since "oops" is hard to control
            test_content = "ops" * args.input_len
        test_case.bench(test_content, batch_size, args.detail, args.output_len)


