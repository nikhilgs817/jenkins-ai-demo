#!/usr/bin/env python3
"""Reads a Jenkins build log + recent git diff, asks a LOCAL Ollama model
why the build failed, and prints the answer into the Jenkins console."""
import argparse, json, os, subprocess, urllib.request

def read_log(path, max_lines=250):
    if not os.path.exists(path):
        return "(build log not found)"
    with open(path, errors="ignore") as f:
        return "".join(f.readlines()[-max_lines:])

def git_context(repo):
    def run(args):
        try:
            return subprocess.run(args, capture_output=True, text=True).stdout.strip()
        except Exception:
            return ""
    commit = run(["git", "-C", repo, "log", "-1", "--pretty=%h %an %s"])
    diff   = run(["git", "-C", repo, "diff", "HEAD~1", "HEAD"])
    return commit, diff[:4000]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--model", default=os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:3b"))
    ap.add_argument("--url", default=os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate"))
    a = ap.parse_args()

    log = read_log(a.log)
    commit, diff = git_context(a.repo)

    prompt = f"""You are a senior DevOps engineer helping triage a failed Jenkins CI/CD pipeline.
Using the build log and the most recent code change, respond in exactly these sections:

ROOT CAUSE: what failed and why (name the file/line if visible).
EVIDENCE: the exact log line(s) that prove it.
FIX: the concrete change to make (show the corrected snippet if relevant).

Be concise and specific.

=== MOST RECENT COMMIT ===
{commit}

=== RECENT CODE DIFF (truncated) ===
{diff}

=== BUILD LOG (tail) ===
{log}
"""
    payload = json.dumps({
        "model": a.model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_ctx": 8192},
    }).encode()

    print("\n" + "=" * 78)
    print("   AI-ASSISTED FAILURE ANALYSIS   (local model: %s)" % a.model)
    print("=" * 78)
    try:
        req = urllib.request.Request(a.url, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read().decode())
        print(data.get("response", "(no response)").strip())
    except Exception as e:
        print("Could not reach local LLM:", e)
    print("=" * 78 + "\n")

if __name__ == "__main__":
    main()
