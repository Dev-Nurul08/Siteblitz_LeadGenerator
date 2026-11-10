"""
SiteBlitz Lead Intelligence OS — Unified Full-Stack Runner
Starts FastAPI backend and Vite frontend concurrently.
"""
import os
import sys
import time
import subprocess

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # The project's virtual environment is .venv; venv is the older name. Without either, the
    # backend would start on whatever Python launched this script, which usually lacks the deps.
    venv_python = sys.executable
    for venv_dir in (".venv", "venv"):
        candidate = os.path.join(root_dir, venv_dir, "Scripts", "python.exe")
        if os.path.exists(candidate):
            venv_python = candidate
            break

    frontend_dir = os.path.join(root_dir, "frontend")

    print("=" * 64)
    print("   SiteBlitz Lead Intelligence OS — Unified System Startup")
    print("=" * 64)
    print(" [1/2] Backend API : http://127.0.0.1:8000 (FastAPI + Swagger Docs)")
    print(" [2/2] Frontend UI : http://localhost:5173  (Vite + React Matrix OS)")
    print("=" * 64)
    print("Press Ctrl+C to terminate both servers concurrently.\n")

    backend_proc = subprocess.Popen(
        [venv_python, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=root_dir
    )

    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=frontend_dir
    )

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print(f"[!] Backend process exited with code {backend_proc.returncode}")
                break
            if frontend_proc.poll() is not None:
                print(f"[!] Frontend process exited with code {frontend_proc.returncode}")
                break
    except KeyboardInterrupt:
        print("\nGracefully shutting down both services...")
    finally:
        for proc in [backend_proc, frontend_proc]:
            try:
                proc.terminate()
            except Exception:
                pass
        print("Both servers stopped cleanly.")

if __name__ == "__main__":
    main()

