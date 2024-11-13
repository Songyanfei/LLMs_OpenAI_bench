# LLMs_OpenAI_bench

## Overview
`LLMs_OpenAI_bench` is a simple benchmarking script designed to evaluate model throughput and identify system bottlenecks in business scenarios. It utilizes a multi-threaded approach to send concurrent requests to large model services, providing insights into performance under different load conditions.

## Features
- **Multi-threaded Requests**: Supports executing multiple requests simultaneously to simulate high-load scenarios.
- **Flexible Configuration**: Allows specification of different batch sizes to test various levels of concurrency.
- **Detailed Metrics**: Option to print detailed request and response metrics for in-depth analysis.

## Prerequisites
Ensure you have Python installed on your system to run the script. This script is tested with Python 3.10 and above.

## Installation
Clone this repository or download the script directly into your preferred directory:
```bash
git https://github.com/Songyanfei/LLMs_OpenAI_bench.git
cd LLMs_OpenAI_bench
```
## Usage
Run the script using Python with necessary arguments:

```bash
python bench.py --model /disk-56/syf/Qwen2.5-14B-Instruct-AWQ -b 2 --url 192.168.3.123 --p 8899 -i 1024 -o 1024
```

```bash
python bench.py --model /data/webapps/llms/Qwen2.5-72B-Instruct-AWQ -c "请给我讲个1000字的故事" -b 2 4 8 16
```



### Arguments
- `--json_file` (optional): Path to JSON file, defaults to 'data/zh.json'
- `--model` (required): Path to the model to test
- `--url` (optional): Server address, defaults to '192.168.3.54'
- `--port` `-p` (optional): Server port, defaults to '19125'
- `--api_key` (optional): API key for authentication, defaults to 'token-abc123'
- `--content` `-c` (optional): Test content
- `--input_len` `-i` (optional): Input length
- `--output_len` `-o` (optional): Output length
- `--batch` `-b` (optional): Number of concurrent requests, accepts multiple values, defaults to [1]
- `--detail` (optional): Print detailed request and response information, defaults to False

## Examples
Run benchmark with default settings:
```bash
python bench.py --model /data/webapps/llms/Qwen2.5-72B-Instruct-AWQ
```
Run benchmark with custom server address and multiple batch sizes:
```bash
python bench.py --model /data/webapps/llms/Qwen2.5-72B-Instruct-AWQ --url 192.168.3.100 --port 18200 --api_key "your_api_key" -c "Test the large model server" -b 1 5 10
```
## Contributing
Contributions to `LLMs_OpenAI_bench` are welcome! Please fork the repository and submit a pull request with your enhancements.

## License
Specify the license under which your tool is released.
