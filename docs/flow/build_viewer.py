"""
Build docs/flow/index.html from siteblitz-flow.mmd + viewer.template.html.

Why a build step: browsers block fetch() of local files opened via file://, so the viewer
embeds the diagram source. Edit the .mmd, then run:  python docs/flow/build_viewer.py
"""

from pathlib import Path

HERE = Path(__file__).parent

# Same palette as docs/spec/ui-redesign.md v2 rows 2–7 — keep the two in sync.
PALETTE = {
    "__BG__": "#18191b",
    "__SURFACE__": "#222427",
    "__BORDER__": "#34373b",
    "__TEXT__": "#eff0f1",
    "__TEXT2__": "#c4c6ca",
    "__ACCENT__": "#ff4a1f",
    "__HOT__": "#ff4a1f",
    "__LEAD__": "#183324",
    "__WARM__": "#3a2719",
    "__NOTLEAD__": "#2e3034",
    "__REVIEW__": "#352b10",
    "__BAD__": "#ff8a9b",
    "__NEUTRAL__": "#2a2c30",
    "__FONT__": "'Mona Sans', 'Segoe UI', system-ui, sans-serif",
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
