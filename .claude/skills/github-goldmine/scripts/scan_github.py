#!/usr/bin/env python3
"""github-goldmine 候选扫描脚本(仅用 Python 标准库)。

用法:
  python3 scan_github.py --query "podcast transcript stars:>100" \
      [--query "..."] [--max-repos 15] [--issue-keywords "install,windows,中文,export"] \
      [--output candidates.json]

- 走 api.github.com;设置环境变量 GITHUB_TOKEN 可提升配额(未认证搜索约 10 次/分钟)。
- 若 API 被会话策略限制(仓库范围锁定的云环境),输出 {"restricted": true},
  调用方应降级到 gh CLI / GitHub MCP / WebSearch+WebFetch。
"""
import argparse, json, os, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://api.github.com"

def gh_get(path, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-goldmine",
        **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.environ.get("GITHUB_TOKEN") else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        if e.code in (403, 404) and ("not available" in body or "not enabled" in body or "bound" in body):
            return None, "restricted"
        if e.code == 403 and "rate limit" in body.lower():
            return None, "rate_limited"
        return None, f"http_{e.code}: {body}"
    except Exception as e:
        return None, f"error: {e}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", action="append", required=True, help="GitHub 搜索式,可重复传入")
    ap.add_argument("--max-repos", type=int, default=15)
    ap.add_argument("--issue-keywords", default="install,windows,docker,中文,export,教程")
    ap.add_argument("--output", default="candidates.json")
    ap.add_argument("--skip-issues", action="store_true", help="只扫仓库元数据,省配额")
    a = ap.parse_args()

    seen, repos, warnings = {}, [], []
    for q in a.query:
        data, err = gh_get("/search/repositories", {"q": q, "sort": "stars", "per_page": 10})
        if err == "restricted":
            json.dump({"restricted": True, "hint": "API 被会话策略限制,请降级到 gh/MCP/WebFetch"}, sys.stdout)
            return
        if err:
            warnings.append(f"search '{q}': {err}")
            continue
        for it in data.get("items", []):
            if it["full_name"] not in seen:
                seen[it["full_name"]] = it
        time.sleep(2)  # 未认证搜索配额很紧

    items = sorted(seen.values(), key=lambda x: -x["stargazers_count"])[: a.max_repos]
    kws = [k.strip() for k in a.issue_keywords.split(",") if k.strip()]

    for it in items:
        full = it["full_name"]
        rec = {
            "repo": full,
            "url": it["html_url"],
            "description": it.get("description"),
            "stars": it["stargazers_count"],
            "pushed_at": it.get("pushed_at"),
            "archived": it.get("archived", False),
            "license": (it.get("license") or {}).get("spdx_id"),
            "open_issues": it.get("open_issues_count"),
            "has_release": None,
            "latest_release": None,
            "issue_signals": {},
        }
        rel, err = gh_get(f"/repos/{full}/releases/latest")
        if rel:
            rec["has_release"] = True
            rec["latest_release"] = {
                "tag": rel.get("tag_name"), "published_at": rel.get("published_at"),
                "assets": [x.get("name") for x in rel.get("assets", [])][:10],
            }
        elif err and err.startswith("http_404"):
            rec["has_release"] = False
        if not a.skip_issues:
            for kw in kws:
                d, err = gh_get("/search/issues", {"q": f"repo:{full} {kw} is:issue", "per_page": 1})
                if d is not None:
                    rec["issue_signals"][kw] = d.get("total_count")
                elif err == "rate_limited":
                    warnings.append("issue search rate limited,后续关键词跳过")
                    a.skip_issues = True
                    break
                time.sleep(2)
        repos.append(rec)

    out = {"restricted": False, "queries": a.query, "repos": repos, "warnings": warnings}
    with open(a.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"已写入 {a.output}: {len(repos)} 个候选" + (f",{len(warnings)} 条警告" if warnings else ""))

if __name__ == "__main__":
    main()
