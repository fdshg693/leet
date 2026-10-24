# /// script
# requires-python = ">=3.10"
# dependencies = ["markdownify>=0.13"]
# ///
"""LeetCode の問題 URL から問題文を Markdown で出力する。

使い方:
    uv run leet2md.py https://leetcode.com/problems/two-sum/          # 標準出力
    uv run leet2md.py two-sum -o problems                             # 学習用フォルダを作成
    uv run leet2md.py two-sum -o problems --lang cpp                  # 解答ファイルの言語を指定
    uv run leet2md.py two-sum -o problems --solution hashmap          # 解答ファイルを追加
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

from markdownify import markdownify

GRAPHQL_URL = "https://leetcode.com/graphql"

QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    difficulty
    isPaidOnly
    content
    topicTags { name }
    hints
    codeSnippets { langSlug code }
  }
}
"""

# langSlug -> (拡張子, コードフェンス名, 行コメント記号)
LANGS = {
    "python3": ("py", "python", "#"),
    "python": ("py", "python", "#"),
    "cpp": ("cpp", "cpp", "//"),
    "c": ("c", "c", "//"),
    "java": ("java", "java", "//"),
    "csharp": ("cs", "csharp", "//"),
    "javascript": ("js", "javascript", "//"),
    "typescript": ("ts", "typescript", "//"),
    "golang": ("go", "go", "//"),
    "rust": ("rs", "rust", "//"),
    "kotlin": ("kt", "kotlin", "//"),
    "swift": ("swift", "swift", "//"),
    "scala": ("scala", "scala", "//"),
    "dart": ("dart", "dart", "//"),
    "php": ("php", "php", "//"),
    "ruby": ("rb", "ruby", "#"),
}

AI_REVIEW_HEADING = "## AI 講評"
AI_REVIEW_PLACEHOLDER = "<!-- AI が講評を追記する欄。日付見出し（### YYYY-MM-DD）ごとに追記していく -->"


def extract_slug(url_or_slug: str) -> str:
    m = re.search(r"leetcode\.(?:com|cn)/problems/([\w-]+)", url_or_slug)
    if m:
        return m.group(1)
    if re.fullmatch(r"[\w-]+", url_or_slug):
        return url_or_slug
    raise ValueError(f"問題の URL またはスラッグとして解釈できません: {url_or_slug}")


def fetch_question(slug: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"titleSlug": slug}}).encode()
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/problems/{slug}/",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.load(res)
    question = (data.get("data") or {}).get("question")
    if not question:
        raise LookupError(f"問題が見つかりません: {slug}")
    return question


def find_snippet(q: dict, lang: str) -> str | None:
    snippet = next((s for s in q["codeSnippets"] or [] if s["langSlug"] == lang), None)
    if snippet:
        return snippet["code"].rstrip()
    available = ", ".join(s["langSlug"] for s in q["codeSnippets"] or [])
    print(f"警告: 言語 '{lang}' のテンプレートがありません ({available})", file=sys.stderr)
    return None


def to_markdown(q: dict, lang: str | None, review: bool = False) -> str:
    url = f"https://leetcode.com/problems/{q['titleSlug']}/"
    tags = ", ".join(t["name"] for t in q["topicTags"]) or "-"
    lines = [
        f"# {q['questionFrontendId']}. {q['title']}",
        "",
        f"- URL: {url}",
        f"- Difficulty: {q['difficulty']}",
        f"- Tags: {tags}",
        "",
        "## Problem",
        "",
    ]

    if q["content"]:
        # 10<sup>4</sup> が "104" にならないよう、先に ^ 記法へ置き換える
        html = re.sub(r"<sup>(.*?)</sup>", r"^\1", q["content"])
        html = re.sub(r"<sub>(.*?)</sub>", r"_\1", html)
        content = markdownify(html, heading_style="ATX", bullets="-")
        content = content.replace("\xa0", " ")
        # "**Follow-up:**Can" のように太字直後に空白がない箇所を補う
        content = re.sub(r"(\*\*[^*\n]+\*\*)(?=\w)", r"\1 ", content)
        content = re.sub(r"\n{3,}", "\n\n", content).strip()
        lines.append(content)
    else:
        lines.append("_有料会員限定の問題のため、問題文を取得できませんでした。_")

    if q["hints"]:
        lines += ["", "## Hints", ""]
        for i, hint in enumerate(q["hints"], 1):
            lines.append(f"{i}. {markdownify(hint).strip()}")

    if lang:
        code = find_snippet(q, lang)
        if code:
            fence = LANGS.get(lang, (lang, lang, "#"))[1]
            lines += ["", "## Code", "", f"```{fence}", code, "```"]

    if review:
        lines += ["", "---", "", AI_REVIEW_HEADING, "", "<!-- 問題の着眼点・典型パターン・関連問題など -->", ""]

    return "\n".join(lines) + "\n"


def approach_template(q: dict, solution_file: str) -> str:
    return f"""# 解答方針 — {q['questionFrontendId']}. {q['title']}

## 問題の整理

- 入力:
- 出力:
- 制約から読み取れること:

## 方針 1

- アイデア:
- 計算量: 時間 O(?) / 空間 O(?)
- コード: [{solution_file}](./{solution_file})

## 詰まった点・気づき

-

---

{AI_REVIEW_HEADING}

{AI_REVIEW_PLACEHOLDER}
"""


def solution_template(q: dict, lang: str, name: str) -> str:
    c = LANGS.get(lang, (lang, lang, "#"))[2]
    code = find_snippet(q, lang) or f"{c} TODO"
    bar = f"{c} {'=' * 60}"
    return f"""{c} {q['questionFrontendId']}. {q['title']} — 解法: {name}
{c} 方針:
{c} 計算量: 時間 O(?) / 空間 O(?)

{code}


{bar}
{c} AI 講評
{c} (AI が講評を追記する欄。日付見出し「--- YYYY-MM-DD ---」ごとに追記していく)
{bar}
"""


def write_if_absent(path: Path, text: str) -> None:
    if path.exists():
        print(f"スキップ (既存): {path}")
        return
    path.write_text(text, encoding="utf-8")
    print(f"作成しました: {path}")


def scaffold(q: dict, out_dir: Path, lang: str, solution: str | None) -> None:
    folder = out_dir / f"{int(q['questionFrontendId']):04d}-{q['titleSlug']}"
    folder.mkdir(parents=True, exist_ok=True)
    ext = LANGS.get(lang, (lang, lang, "#"))[0]

    write_if_absent(folder / "problem.md", to_markdown(q, None, review=True))

    existing = sorted(folder.glob("solution-*"))
    if solution is None:
        if existing:
            # 初回以降は明示的に --solution を指定したときだけ解答ファイルを増やす
            first = existing[0].name
        else:
            first = f"solution-1.{ext}"
            write_if_absent(folder / first, solution_template(q, lang, "1"))
    else:
        first = existing[0].name if existing else f"solution-{solution}.{ext}"
        write_if_absent(folder / f"solution-{solution}.{ext}", solution_template(q, lang, solution))

    write_if_absent(folder / "approach.md", approach_template(q, first))


def main() -> None:
    parser = argparse.ArgumentParser(description="LeetCode の問題を Markdown で出力")
    parser.add_argument("url", help="問題の URL またはスラッグ (例: two-sum)")
    parser.add_argument(
        "--lang",
        help="コードテンプレートの言語 (例: python3, cpp, java)。-o 指定時の既定は python3",
    )
    parser.add_argument(
        "-o", "--out-dir", type=Path, help="指定するとその下に問題ごとの学習用フォルダを作成"
    )
    parser.add_argument(
        "--solution", metavar="NAME", help="解答ファイル solution-NAME.{ext} を追加 (例: hashmap)"
    )
    args = parser.parse_args()

    if args.solution and not re.fullmatch(r"[\w-]+", args.solution):
        sys.exit(f"エラー: --solution には英数字・_・- のみ使えます: {args.solution}")

    try:
        slug = extract_slug(args.url)
        q = fetch_question(slug)
    except (ValueError, LookupError, OSError) as e:
        sys.exit(f"エラー: {e}")

    if args.out_dir:
        scaffold(q, args.out_dir, args.lang or "python3", args.solution)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(to_markdown(q, args.lang))


if __name__ == "__main__":
    main()
