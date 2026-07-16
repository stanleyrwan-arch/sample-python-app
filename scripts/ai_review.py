#!/usr/bin/env python3
"""
AI code review step for the CSE636 Week 2 lab.
Reads Python files and asks Claude for a concise code review.
"""
import os
import subprocess

import anthropic

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_python_files():
    """Return all tracked Python files in the repository."""
    result = subprocess.run(
        ["git", "ls-files", "*.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    return [f for f in result.stdout.strip().split("\n") if f.endswith(".py")]


def read_file(path):
    """Read a file as text."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def review_code(filename, content):
    """Ask Claude to review a single Python file."""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Please review the following Python file for correctness, "
                    "style issues, potential bugs, and readability. Be concise.\n\n"
                    f"Filename: {filename}\n\n"
                    f"```python\n{content}\n```"
                ),
            }
        ],
    )
    return message.content[0].text


def main():
    files = get_python_files()
    report_lines = ["# AI Code Review Report\n"]

    if not files:
        report_lines.append("No Python files found.")
    else:
        for filename in files:
            content = read_file(filename)
            print(f"Reviewing {filename}...")
            review = review_code(filename, content)
            report_lines.append(f"\n## {filename}\n\n{review}\n")

    with open("ai_review_report.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(report_lines))

    print("AI review complete. Report saved to ai_review_report.txt")


if __name__ == "__main__":
    main()
