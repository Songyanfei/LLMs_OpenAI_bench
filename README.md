# Naive_OpenAI_bench
一个简单的测试脚本用于评估业务场景下的模型吞吐和系统瓶颈.

python bench.py --model /data/webapps/llms/Qwen2.5-72B-Instruct-AWQ -c 请给我讲个100字的故事

parser = argparse.ArgumentParser(description='Multi-threaded benchmark tool')
    parser.add_argument('--model', type=str, default='', help='Model name', required=True)
    parser.add_argument('--url', type=str, default='192.168.3.54', help='Server address')
    parser.add_argument('--port', '-p', type=str, default='19125', help='Server port')
    parser.add_argument('--api_key', type=str, default='token-abc123', help='API key')
    parser.add_argument('--content', '-c', type=str, default='r u ok?', help='Test content')
    parser.add_argument('--batch', '-b', type=int, nargs='+', default=[1], help='Number of concurrent requests')
    parser.add_argument('--detail', type=bool, default=False, help='Print request details')
