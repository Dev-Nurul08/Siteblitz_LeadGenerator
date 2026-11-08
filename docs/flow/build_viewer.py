"""
Build docs/flow/index.html from siteblitz-flow.mmd + viewer.template.html.

Why a build step: browsers block fetch() of local files opened via file://, so the viewer
embeds the diagram source. Edit the .mmd, then run:  python docs/flow/build_viewer.py
"""

from pathlib import Path

HERE = Path(__file__).parent

# Same palette as docs/spec/ui-redesign.md (rows "colour tokens") — keep the two in sync.
PALETTE = {
    "__BG__": "#f4f4f1",
    "__SURFACE__": "#ffffff",
    "__BORDER__": "#dededa",
    "__TEXT__": "#17181a",
    "__TEXT2__": "#45474b",
    "__ACCENT__": "#1a4be0",
    "__HOT__": "#b8360f",
    "__LEAD__": "#e1f3e7",
    "__WARM__": "#fdeedd",
    "__NOTLEAD__": "#fce6e9",
    "__REVIEW__": "#fbf0d2",
    "__BAD__": "#b42318",
    "__NEUTRAL__": "#efefeb",
    "__FONT__": "'IBM Plex Sans', 'Segoe UI', system-ui, sans-serif",
}


def main() -> None:
    html = (HERE / "viewer.template.html").read_text(encoding="utf-8")
    mmd = (HERE / "siteblitz-flow.mmd").read_text(encoding="utf-8")
    if "</script" in mmd.lower():
        raise SystemExit("siteblitz-flow.mmd must not contain '</script'")
    for key, value in PALETTE.items():
        html = html.replace(key, value)
    html = html.replace("__MMD__", mmd)
    (HERE / "index.html").write_text(html, encoding="utf-8")
    print(f"wrote {HERE / 'index.html'}")


if __name__ == "__main__":
    main()
