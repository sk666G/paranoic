import json
import os
import re
import subprocess
import sys

ROLE_ID = "1568644775983456276"
CONTENT_LIMIT = 2000


def git(*args, check=True):
    return subprocess.run(
        ["git", *args], capture_output=True, encoding="utf-8", errors="replace", check=check
    )


def previous_commit(head):
    before = os.environ["CI_COMMIT_BEFORE_SHA"]
    if before == "0" * 40:
        if os.environ.get("CI_COMMIT_TAG"):
            return ""
        fetched = git("fetch", "--quiet", "--no-tags", "origin", os.environ["CI_DEFAULT_BRANCH"], check=False)
        if fetched.returncode == 0:
            return git("merge-base", "FETCH_HEAD", head, check=False).stdout.strip()
        return ""

    if git("cat-file", "-e", f"{before}^{{commit}}", check=False).returncode == 0:
        return before
    if git("fetch", "--quiet", "--no-tags", "origin", before, check=False).returncode == 0:
        return before
    return ""


def message_size(content):
    return len(content.encode("utf-16-le")) // 2


def main(zio_version, mc_version, download_url):
    head = os.environ["CI_COMMIT_SHA"]
    project = os.environ["CI_PROJECT_URL"]
    before = previous_commit(head)
    log_format = "--format=%H%x00%s"
    entries = git("log", "--reverse", log_format, f"{before}..{head}").stdout if before else ""
    if not entries:
        entries = git("log", "-1", log_format, head).stdout

    bullets = []
    for entry in entries.rstrip("\n").split("\n"):
        sha, subject = entry.split("\0", 1)
        subject = re.sub(r"([\\`*_~|\[\]<>])", r"\\\1", subject)
        bullets.append(f"- [{sha[:8]}]({project}/-/commit/{sha}) - {subject}")

    content = f"# Open Zio {zio_version} {mc_version}\n\n"
    footer = f"\n\n<@&{ROLE_ID}>"
    if download_url:
        footer = f"\n\n[Download the JAR on GitLab]({download_url})" + footer

    if message_size(content + "\n".join(bullets) + footer) > CONTENT_LIMIT:
        changes = f"{project}/-/compare/{before}...{head}?straight=true" if before else f"{project}/-/commit/{head}"
        overflow = f"- … [View the remaining changes on GitLab]({changes})"
        for bullet in bullets:
            if message_size(content + bullet + "\n" + overflow + footer) > CONTENT_LIMIT:
                break
            content += bullet + "\n"
        content += overflow
    else:
        content += "\n".join(bullets)

    print(json.dumps({"content": content + footer, "allowed_mentions": {"roles": [ROLE_ID]}, "flags": 4}))


if __name__ == "__main__":
    main(*sys.argv[1:])
