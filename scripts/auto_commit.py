#!/usr/bin/env python3
"""自动将当天新闻 JSON 提交到 GitHub"""
import os
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DEPLOY_KEY = Path("/root/.openclaw/workspace/.deploy-keys/knews_deploy")


def push_news():
    today = datetime.now().strftime("%Y-%m-%d")

    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = (
        f"ssh -i {DEPLOY_KEY} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    )

    os.chdir(ROOT)

    # 配置 git（避免 isolated session 里没配置）
    subprocess.run(["git", "config", "user.email", "kimi-claw@openclaw.ai"], check=False)
    subprocess.run(["git", "config", "user.name", "Kimi Claw"], check=False)

    # 拉取最新代码（避免冲突）
    subprocess.run(["git", "pull", "origin", "main", "--rebase"], env=env, check=False)

    # 添加变更
    subprocess.run(["git", "add", "data/news/"], check=True)

    # 检查是否有变更需要提交
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode == 0:
        print("没有新变更，跳过提交")
        return

    # 提交并推送
    subprocess.run(
        ["git", "commit", "-m", f"auto: daily tech news for {today}"],
        check=True,
    )
    subprocess.run(["git", "push", "origin", "main"], env=env, check=True)
    print(f"✅ 已推送 {today} 的新闻到 GitHub")


if __name__ == "__main__":
    push_news()
