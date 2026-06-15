import contextlib
import base64
import io
import json
import os
import sys
import traceback
from pathlib import Path


def run_notebook(path):
    path = Path(path).resolve()
    notebook = json.loads(path.read_text(encoding="utf-8"))
    namespace = {"__name__": "__main__"}
    old_cwd = Path.cwd()
    os.chdir(path.parent)
    count = 0
    try:
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            count += 1
            cell["execution_count"] = count
            cell["outputs"] = []
            stdout = io.StringIO()
            display_outputs = []

            def display(*objects):
                for obj in objects:
                    if hasattr(obj, "to_html"):
                        html = obj.to_html()
                    elif hasattr(obj, "_repr_html_"):
                        html = obj._repr_html_()
                    else:
                        html = f"<pre>{obj}</pre>"
                    display_outputs.append({
                        "output_type": "display_data",
                        "metadata": {},
                        "data": {"text/html": html},
                    })

            namespace["display"] = display
            try:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stdout):
                    exec(compile("".join(cell["source"]), f"{path.name}:cell-{count}", "exec"), namespace)
                text = stdout.getvalue()
                if text:
                    cell["outputs"].append({"name": "stdout", "output_type": "stream", "text": text.splitlines(keepends=True)})
                cell["outputs"].extend(display_outputs)

                pyplot = namespace.get("plt")
                if pyplot is not None:
                    for number in pyplot.get_fignums():
                        figure = pyplot.figure(number)
                        buffer = io.BytesIO()
                        figure.savefig(buffer, format="png", dpi=120, bbox_inches="tight")
                        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
                        cell["outputs"].append({
                            "output_type": "display_data",
                            "metadata": {},
                            "data": {"image/png": encoded},
                        })
                    pyplot.close("all")
            except Exception as exc:
                cell["outputs"].append({
                    "output_type": "error",
                    "ename": type(exc).__name__,
                    "evalue": str(exc),
                    "traceback": traceback.format_exc().splitlines(),
                })
                with path.open("w", encoding="utf-8", newline="\n") as handle:
                    handle.write(json.dumps(notebook, ensure_ascii=False, indent=1))
                raise
    finally:
        os.chdir(old_cwd)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(notebook, ensure_ascii=False, indent=1))
    print(f"Executed {path.name}: {count} code cells")


if __name__ == "__main__":
    for notebook_path in sys.argv[1:]:
        run_notebook(notebook_path)
