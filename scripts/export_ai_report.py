"""Appendix C, "Report on the Use of AI": the exact queries typed into the AI tool and its complete text output, as LaTeX.

Usage:  python scripts/export_ai_report.py [--transcript PATH ...]

UPC rules: the end of the paper must state (1) the system used, (2) the exact wording of every query and (3) the complete output.
This script reads the Claude Code session transcript(s) (JSON lines, written by Claude Code under ~/.claude/projects/) and writes
overleaf/sections/C-ai-log.tex (every query in chronological order, each followed by everything the AI wrote back as text),
C-ai-instructions.tex (the standing project instructions CLAUDE.md, loaded into every session) and C-ai-meta.tex (dates, model).

What is included and what is not:
* Queries: every message typed by a team member, verbatim, including slash commands (/plan, skills) and pasted text.
  Excluded: /login and the output of shell commands the team ran themselves (not queries to the AI).
* Output: every text message the AI wrote, verbatim. Automatic notifications that a background task had finished are marked,
  because the AI's text after them continues the answer to the preceding query. Not reproduced: the AI's tool calls (file edits,
  shell commands, web searches) and their raw results; their product is the code, data and history of the GitHub repository.
* Redactions (privacy and security only, marked [REDACTED ...]): login details and a password for a university computing cluster,
  user@host account names, full host names of that cluster. Nothing else is changed.
"""
import argparse
import glob
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = sorted(glob.glob(str(Path.home() / ".claude" / "projects" / "-mnt-c-Users-frantuxed-Downloads-UPC" / "*.jsonl")))
SYS = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)

UNI = {"–": "--", "‑": "-", "±": "$\\pm$", "≈": "$\\approx$", "²": "$^2$", "σ": "$\\sigma$", "→": "$\\rightarrow$", "−": "$-$",
       "\u20d7": "", "³": "$^3$", "°": "$^\\circ$", "×": "$\\times$", "ω": "$\\omega$", "é": "\\'e", "·": "$\\cdot$",
       "χ": "$\\chi$", "₀": "$_0$", "ö": "\\\"o", "…": "\\ldots{}", "—": "---", "⁻": "$^-$", "§": "\\S{}", "∝": "$\\propto$",
       "ρ": "$\\rho$", "√": "$\\surd$", "∈": "$\\in$", "í": "\\'i", "∥": "$\\parallel$", "’": "'", "‘": "`", "ê": "\\^e",
       "Δ": "$\\Delta$", "⁴": "$^4$", "≥": "$\\geq$", "⅔": "$\\frac23$", "©": "\\copyright{}", "£": "\\pounds{}", "¡": "!`",
       "≤": "$\\leq$", "¹": "$^1$", "⁰": "$^0$", "⊥": "$\\perp$", "₁": "$_1$", "₂": "$_2$", "←": "$\\leftarrow$", "\u00a0": "~",
       "Ω": "$\\Omega$", "✗": "x", "𝐠": "$\\mathbf{g}$", "⁵": "$^5$", "µ": "$\\mu$", "μ": "$\\mu$", "“": "``", "”": "''",
       "ł": "\\l{}", "ą": "\\k{a}", "ę": "\\k{e}", "ó": "\\'o", "ś": "\\'s", "ć": "\\'c", "ń": "\\'n", "ż": "\\.z", "ź": "\\'z",
       "Ł": "\\L{}", "Ś": "\\'S", "Ż": "\\.Z", "π": "$\\pi$", "θ": "$\\theta$", "α": "$\\alpha$", "β": "$\\beta$", "τ": "$\\tau$",
       "μ": "$\\mu$", "≠": "$\\neq$", "∞": "$\\infty$", "✓": "ok", "⇒": "$\\Rightarrow$", "↔": "$\\leftrightarrow$", "≲": "$\\lesssim$",
       "≳": "$\\gtrsim$", "⟂": "$\\perp$", "∼": "$\\sim$", "•": "$\\bullet$", "ü": "\\\"u", "ä": "\\\"a", "è": "\\`e", "Å": "\\AA{}",
       "æ": "\\ae{}", "ø": "\\o{}"}
ASCII = {"\\": "\\textbackslash{}", "{": "\\{", "}": "\\}", "$": "\\$", "&": "\\&", "#": "\\#", "^": "\\^{}", "_": "\\_",
         "%": "\\%", "~": "\\textasciitilde{}", "<": "\\textless{}", ">": "\\textgreater{}", "|": "\\textbar{}", '"': "\\textquotedbl{}"}
BREAK_AFTER = set("/_.-=,:;)]}")


def tex_token(tok):
    """Escape one whitespace-free token; long tokens (paths, URLs, code) get break points."""
    out, run = [], 0
    for ch in tok:
        out.append(ASCII.get(ch) or UNI.get(ch) or (ch if ord(ch) < 128 else "?"))
        run += 1
        if len(tok) > 18 and (ch in BREAK_AFTER or run >= 14):
            out.append("\\allowbreak{}"); run = 0
    return "".join(out)


def tex(text):
    paras = re.split(r"\n\s*\n", text.strip())
    return "\n\n".join("\\newline\n".join(" ".join(tex_token(t) for t in line.split()) or "~" for line in p.split("\n")) for p in paras)


SECRETS = set()   # filled in main(): every string that followed a "passwd:" anywhere, removed from every message


def redact(text):
    for sec in SECRETS:
        text = text.replace(sec, "[REDACTED]")
    text = re.sub(r"(ssh\s+-J\s+)\S+.*", r"\1[REDACTED: cluster login details and password]", text)
    text = re.sub(r"(?i)\b(passw(or)?d|has[lł]o)\s*[:=]\s*\S+", r"\1: [REDACTED]", text)
    text = re.sub(r"[\w.+-]+@([\w-]+\.)*fuw\.edu\.pl", "[REDACTED user@host]", text)
    text = re.sub(r"\b[\w-]+(\.[\w-]+)*\.fuw\.edu\.pl\b", "[REDACTED host]", text)
    return text


def turns(paths):
    for f in paths:
        for line in open(f, errors="ignore"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("isSidechain") or d.get("isMeta") or d.get("isCompactSummary") or d.get("type") not in ("user", "assistant"):
                continue
            m = d.get("message") or {}
            c = m.get("content")
            parts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
            txt = "\n\n".join(p for p in (SYS.sub("", p).strip() for p in parts) if p)
            if txt:
                yield d["type"], d.get("timestamp", ""), m.get("model"), txt


def classify(txt):
    """('query', text) | ('notify', None) | ('skip', None) for a user-side message."""
    if "<task-notification>" in txt:
        return "notify", None
    if re.search(r"<(local-command-stdout|bash-stdout|bash-stderr|bash-input)>", txt):
        return "skip", None
    cmd = re.search(r"<command-name>(.*?)</command-name>", txt, re.S)
    if cmd:
        name = cmd.group(1).strip()
        if name in ("/login", "/logout", "/model", "/clear", "/config", "/status", "/cost"):
            return "skip", None
        args = re.search(r"<command-args>(.*?)</command-args>", txt, re.S)
        return "query", (name + (" " + args.group(1).strip() if args and args.group(1).strip() else ""))
    if txt.startswith("Base directory for this skill:"):        # expanded skill text inserted by the tool, not typed
        return "skip", None
    txt = re.sub(r"</?pasted_content[^>]*>", "\n[pasted text]\n", txt).strip()
    return "query", txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", nargs="*", default=DEFAULT)
    a = ap.parse_args()
    for _, _, _, txt in turns(a.transcript):
        SECRETS.update(m.group(2) for m in re.finditer(r"(?i)\b(passw(?:or)?d|has[lł]o)\s*[:=]\s*(\S+)", txt) if len(m.group(2)) >= 4)
    L, nq, models, first, last = [], 0, set(), None, None
    in_output = False
    for role, ts, model, txt in turns(a.transcript):
        when = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%d %b %Y, %H:%M UTC") if ts else ""
        if role == "user":
            kind, q = classify(txt)
            if kind == "skip":
                continue
            if kind == "notify":
                L.append("\\aiNote{automatic notification to the AI: a background computation finished}")
                continue
            nq += 1; in_output = False
            first = first or when; last = when
            L.append(f"\\aiQuery{{{nq}}}{{{when}}}\n{tex(redact(q))}")
        else:
            if model and not model.startswith("<"):
                models.add(model)
            if not in_output:
                L.append("\\aiOutput"); in_output = True
            L.append(tex(redact(txt)))
    tag = "% AUTO-GENERATED by scripts/export_ai_report.py from the Claude Code session transcript -- do not edit by hand"
    sec = ROOT / "overleaf" / "sections"
    (sec / "C-ai-meta.tex").write_text(tag + "\n" + f"\\newcommand{{\\aiNQueries}}{{{nq}}}\\newcommand{{\\aiFirst}}{{{first}}}"
                                       f"\\newcommand{{\\aiLast}}{{{last}}}\\newcommand{{\\aiModels}}{{{', '.join(sorted(models))}}}\n")
    # the standing project instructions (CLAUDE.md) are loaded into every session, so they are input to the AI as well
    (sec / "C-ai-instructions.tex").write_text(tag + "\n\\begingroup\\aiLogStyle\n" + tex(redact((ROOT / "CLAUDE.md").read_text()))
                                               + "\n\\endgroup\n")
    out = sec / "C-ai-log.tex"
    out.write_text(tag + "\n\\begingroup\\aiLogStyle\n" + "\n\n".join(L) + "\n\\endgroup\n")
    print(f"wrote {out}: {nq} queries, models {sorted(models)}, {first} -- {last}")


if __name__ == "__main__":
    main()
