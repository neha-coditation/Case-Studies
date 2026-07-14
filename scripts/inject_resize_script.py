import os
from bs4 import BeautifulSoup

RESIZE_SCRIPT_ID = "iframe-resize-script"

RESIZE_SCRIPT = f"""
<script id="{RESIZE_SCRIPT_ID}">
function sendHeightToParent() {{
  const height = document.documentElement.scrollHeight;
  window.parent.postMessage({{ type: 'resize-iframe', height: height }}, '*');
}}
window.addEventListener('load', sendHeightToParent);
window.addEventListener('resize', sendHeightToParent);
new ResizeObserver(sendHeightToParent).observe(document.body);
setTimeout(sendHeightToParent, 500);
setTimeout(sendHeightToParent, 1500);
</script>
"""

def inject_into_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "lxml")

    # Skip if already injected
    if soup.find("script", {"id": RESIZE_SCRIPT_ID}):
        print(f"Skipped (already has script): {filepath}")
        return False

    if soup.body is None:
        print(f"Skipped (no <body> found): {filepath}")
        return False

    script_soup = BeautifulSoup(RESIZE_SCRIPT, "lxml")
    soup.body.append(script_soup)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"Injected: {filepath}")
    return True


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Skip index.html unless you also want it there
    exclude = {"index.html"}

    count = 0
    for fname in os.listdir(repo_root):
        if fname.endswith(".html") and fname not in exclude:
            filepath = os.path.join(repo_root, fname)
            if inject_into_file(filepath):
                count += 1

    print(f"\nDone. Injected into {count} file(s).")


if __name__ == "__main__":
    main()
