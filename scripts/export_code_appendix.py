"""Write the code appendix of the paper: the simulation source without comments or docstrings, typeset with listings.

Usage:  PYTHONPATH=src .venv/bin/python scripts/export_code_appendix.py
Writes overleaf/code/<module>.py (stripped copies) and overleaf/sections/B-code.tex. The documented source stays in the repository;
the appendix shows only the code itself.
"""
import ast
import io
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "overleaf" / "code"
MODULES = [("Physical constants and the test case", "src/penalty/constants.py"),
           ("Aerodynamic coefficients", "src/penalty/coefficients.py"),
           ("Forces", "src/penalty/forces.py"),
           ("Equations of motion", "src/penalty/dynamics.py"),
           ("Reference integrator", "src/penalty/integrate.py"),
           ("Goal geometry and outcome", "src/penalty/outcome.py"),
           ("Least-squares inverse problem (Stages 1--3)", "src/penalty/inverse.py"),
           ("Linearised prediction", "src/penalty/predict.py"),
           ("Air and venue climate", "src/penalty/environment.py"),
           ("Vectorised integrator for sampling", "src/penalty/fastsim.py"),
           ("Bayesian model", "src/penalty/bayes.py"),
           ("Kick-mechanics spin prior", "src/penalty/kick.py"),
           ("Frame impacts", "src/penalty/collision.py"),
           ("Posterior sampling (Stages 4 and 6)", "scripts/run_stage4.py"),
           ("Probability of a goal (Stage 5)", "scripts/run_stage5.py"),
           ("Goal-probability map", "scripts/goal_probability_map.py"),
           ("Simulation-based coverage test", "scripts/validate_stage4_coverage.py")]


def docstring_lines(src):
    """Line numbers (1-based) covered by module, class and function docstrings."""
    lines = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                lines.update(range(first.lineno, first.end_lineno + 1))
    return lines


def strip(src):
    """Remove comments and docstrings, keep the layout of the code, collapse runs of blank lines."""
    drop = docstring_lines(src)
    comments = {}
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            comments[tok.start[0]] = tok.start[1]
    out = []
    for i, line in enumerate(src.splitlines(), 1):
        if i in drop:
            continue
        if i in comments:
            line = line[:comments[i]].rstrip()
            if not line.strip():
                continue
        out.append(line.rstrip())
    text, blank = [], 0
    for line in out:
        blank = blank + 1 if not line.strip() else 0
        if blank <= 1:
            text.append(line)
    while text and not text[0].strip():
        text.pop(0)
    return "\n".join(text).rstrip() + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tex = [r"\section{Simulation code}\label{app:code}",
           r"The complete simulation code in Python~3 (NumPy, SciPy, emcee), in the order in which the model is built.", ""]
    for title, path in MODULES:
        src = (ROOT / path).read_text()
        code = strip(src)
        compile(code, path, "exec")                     # the stripped code must still be valid Python
        name = Path(path).name
        (OUT / name).write_text(code)
        tex.append(rf"\subsection*{{{title}: \texttt{{{name.replace('_', chr(92) + '_')}}}}}")
        tex.append(rf"\lstinputlisting[style=sim]{{code/{name}}}")
        tex.append("")
    (ROOT / "overleaf" / "sections" / "B-code.tex").write_text("\n".join(tex))
    n = sum(len((OUT / Path(p).name).read_text().splitlines()) for _, p in MODULES)
    print(f"wrote {len(MODULES)} listings ({n} lines) to {OUT} and overleaf/sections/B-code.tex")


if __name__ == "__main__":
    main()
