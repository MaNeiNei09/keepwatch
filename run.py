#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安行情Dashboard 一键启停脚本
"""

import os
import sys
import subprocess
import signal
import time
import platform

# 解决Windows中文编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 项目路径
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = PROJECT_DIR
FRONTEND_DIR = os.path.join(PROJECT_DIR, "binance-dashboard")

# 进程列表
processes = []

def get_pid_file(name):
    return os.path.join(PROJECT_DIR, f".{name}.pid")

def save_pid(name, pid):
    with open(get_pid_file(name), 'w') as f:
        f.write(str(pid))

def read_pid(name):
    try:
        with open(get_pid_file(name), 'r') as f:
            return int(f.read().strip())
    except:
        return None

def delete_pid(name):
    try:
        os.remove(get_pid_file(name))
    except:
        pass

def is_process_running(pid):
    if pid is None:
        return False
    try:
        if platform.system() == "Windows":
            # Windows: 使用tasklist检查进程是否存在
            result = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'],
                                    capture_output=True, text=True)
            return str(pid) in result.stdout
        else:
            # Unix: 检查进程是否存活
            os.kill(pid, 0)
            return True
    except (ProcessLookupError, PermissionError, OSError):
        return False

def start_backend():
    """启动后端服务"""
    print("[1/2] 启动后端服务...")
    try:
        # 检查5001端口是否被占用
        if platform.system() == "Windows":
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            if ':5001' in result.stdout:
                print("  ⚠ 后端服务端口5001已被占用，尝试关闭现有进程...")
                for line in result.stdout.split('\n'):
                    if ':5001' in line and 'LISTENING' in line:
                        try:
                            pid = int(line.split()[-1])
                            subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
                            time.sleep(1)
                        except:
                            pass

        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        proc = subprocess.Popen(
            [sys.executable, "binance_server.py"],
            cwd=BACKEND_DIR,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if platform.system() == "Windows" else 0
        )
        processes.append(('backend', proc))
        save_pid('backend', proc.pid)
        print(f"  ✓ 后端服务已启动 (PID: {proc.pid})")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"  ✗ 后端启动失败: {e}")
        return False

def start_frontend():
    """启动前端服务"""
    print("[2/2] 启动前端服务...")
    try:
        # 检查3000端口
        if platform.system() == "Windows":
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            for port in [3000, 3001, 3002, 3003]:
                if f':{port}' in result.stdout:
                    print(f"  ⚠ 端口{port}已被占用，Vite会自动使用其他端口")

        proc = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=FRONTEND_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if platform.system() == "Windows" else 0
        )
        processes.append(('frontend', proc))
        save_pid('frontend', proc.pid)
        print(f"  ✓ 前端服务已启动 (PID: {proc.pid})")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"  ✗ 前端启动失败: {e}")
        return False

def stop_service(name):
    """停止指定服务"""
    pid = read_pid(name)
    if pid and is_process_running(pid):
        print(f"  停止 {name} 服务 (PID: {pid})...")
        try:
            if platform.system() == "Windows":
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
            else:
                os.kill(pid, signal.SIGTERM)
            time.sleep(1)
        except Exception as e:
            print(f"    停止失败: {e}")
    delete_pid(name)

def status_check():
    """检查服务状态"""
    backend_pid = read_pid('backend')
    frontend_pid = read_pid('frontend')

    print("\n=== 服务状态 ===")
    backend_running = is_process_running(backend_pid)
    frontend_running = is_process_running(frontend_pid)

    print(f"后端服务 (5001): {'✅ 运行中' if backend_running else '❌ 已停止'}")
    print(f"前端服务:        {'✅ 运行中' if frontend_running else '❌ 已停止'}")

    if backend_running:
        print(f"  → 访问地址: http://localhost:5001")
    if frontend_running:
        # 尝试获取实际端口
        print(f"  → 访问地址: http://localhost:3000 (或3001/3002)")

    return backend_running or frontend_running

def main():
    if len(sys.argv) < 2:
        print("""
=== 币安行情Dashboard 启停脚本 ===

用法:
  python run.py start   - 启动所有服务
  python run.py stop    - 停止所有服务
  python run.py restart - 重启所有服务
  python run.py status  - 查看服务状态

说明:
  - 后端: http://localhost:5001
  - 前端: http://localhost:3000 (或自动分配的端口)

""")
        status_check()
        return

    cmd = sys.argv[1].lower()

    if cmd == 'start':
        print("=" * 50)
        print("  启动币安行情Dashboard")
        print("=" * 50)

        # 检查是否已运行
        if status_check():
            print("\n⚠ 服务已在运行中，请先执行 stop 再启动")
            return

        start_backend()
        start_frontend()

        print("\n" + "=" * 50)
        print("  🎉 启动完成!")
        print("=" * 50)
        print("\n请在浏览器访问:")
        print("  → http://localhost:3000 (或3001/3002)")
        print("\n按 Ctrl+C 停止服务，或运行: python run.py stop")

    elif cmd == 'stop':
        print("=" * 50)
        print("  停止所有服务")
        print("=" * 50)
        stop_service('frontend')
        stop_service('backend')
        print("\n✓ 所有服务已停止")

    elif cmd == 'restart':
        print("=" * 50)
        print("  重启服务")
        print("=" * 50)
        stop_service('frontend')
        stop_service('backend')
        time.sleep(1)
        start_backend()
        start_frontend()
        print("\n✓ 重启完成!")

    elif cmd == 'status':
        status_check()

    else:
        print(f"未知命令: {cmd}")
        print("可用命令: start, stop, restart, status")

if __name__ == '__main__':
    main()