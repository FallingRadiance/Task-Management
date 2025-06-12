import requests
import sys

# 状态检查脚本

def check_service():
    try:
        # 检查API根路径
        root_response = requests.get('http://127.0.0.1:8000')
        print(f"API根路径状态: {root_response.status_code}")
        print(f"响应内容: {root_response.json()}")
        
        # 检查tasks接口
        tasks_response = requests.get('http://127.0.0.1:8000/tasks/')
        print(f"Tasks接口状态: {tasks_response.status_code}")
        
        # 检查API文档
        docs_response = requests.get('http://127.0.0.1:8000/docs')
        print(f"API文档状态: {docs_response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("无法连接到服务器，请确保服务正在运行")
        sys.exit(1)
    except Exception as e:
        print(f"检查时发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    check_service()