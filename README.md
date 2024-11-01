# LLMs_OpenAI_bench

## Overview
`Naive_OpenAI_bench` is a simple benchmarking script designed to evaluate model throughput and identify system bottlenecks in business scenarios. It utilizes a multi-threaded approach to send concurrent requests to large model services, providing insights into performance under different load conditions.

## Features
- **Multi-threaded Requests**: Supports executing multiple requests simultaneously to simulate high-load scenarios.
- **Flexible Configuration**: Allows specification of different batch sizes to test various levels of concurrency.
- **Detailed Metrics**: Option to print detailed request and response metrics for in-depth analysis.

## Prerequisites
Ensure you have Python installed on your system to run the script. This script is tested with Python 3.7 and above.

## Installation
Clone this repository or download the script directly into your preferred directory:
```bash
git clone https://github.com/yourrepository/Naive_OpenAI_bench.git
cd LLMs_OpenAI_bench

## Usage
Run the script using Python with necessary arguments:
```bash
python bench.py --model /data/webapps/llms/Qwen2.5-72B-Instruct-AWQ -c "请给我讲个1000字的故事" -b 2 4 8 16

### Arguments
- `--model` (required): Path to the model you want to test.
- `--url` (optional): Server address, defaults to '192.168.3.54'.
- `--port` `-p` (optional): Server port, defaults to '19125'.
- `--api_key` (optional): API key for authentication.
- `--content` `-c` (optional): Content to send as request payload, defaults to 'r u ok?'.
- `--batch` `-b` (optional): Batch sizes to test, accepts multiple values for concurrent requests.
- `--detail` (optional): Set to True to print detailed information about each request and response.

## Examples
Run benchmark with default settings:
```bash
python bench.py --model /data/webapps/llms/Qwen2.5-72B-Instruct-AWQ

Run benchmark with custom server address and multiple batch sizes:
```bash
python bench.py --model /data/webapps/llms/Qwen2.5-72B-Instruct-AWQ --url 192.168.3.100 --port 18200 --api_key "your_api_key" -c "Test the large model server" -b 1 5 10

## Contributing
Contributions to `Naive_OpenAI_bench` are welcome! Please fork the repository and submit a pull request with your enhancements.

## License
Specify the license under which your tool is released.
