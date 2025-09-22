#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List, Iterable

ROOT = Path(__file__).resolve().parents[1]
APPS_DIR = ROOT / "apps"

REQUIRED_DIRS_BASE = [
    "domain",
    "application/services",
    "application/selectors",
    "infrastructure/repositories",
    "infrastructure/web",
]

MUST_LIVE_HERE = {
    "entities.py": "domain",
    "ports.py": "domain",
    "serializers.py": "infrastructure/web",
    "views.py": "infrastructure/web",
    "urls.py": "infrastructure/web",
    "pg_utils.py": "infrastructure/repositories",
    "tests.py": [".", "tests", "tests/unit", "tests/integration"],
    "apps.py": ".",
    "admin.py": ".",
    "models.py": ".",
}

ALLOWED_ROOT_FILES = {"apps.py", "admin.py", "models.py", "tests.py", "__init__.py"}

FORBID_PY_AT = {
    "application": "Usa application/services/ o application/selectors/ (no dejes .py sueltos en application/).",
    "infrastructure": "Usa infrastructure/repositories/ o infrastructure/web/ (no dejes .py sueltos en infrastructure/).",
}

def list_app_dirs(base: Path) -> List[Path]:
    if not base.exists():
        return []
    return [p for p in base.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))]

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)

def _normalize_allowed_dirs(v):
    return [v] if isinstance(v, str) else list(v)

def is_allowed_location(app: Path, file_path: Path, allowed_rel_dirs: Iterable[str]) -> bool:
    for rel_dir in allowed_rel_dirs:
        expected_dir = app if rel_dir == "." else (app / rel_dir)
        if file_path.parent.resolve() == expected_dir.resolve():
            return True
    return False

def main() -> int:
    errors: List[str] = []

    if not APPS_DIR.exists():
        errors.append(f"[E000] No existe el directorio base de apps: {rel(APPS_DIR)}")
    else:
        for app in list_app_dirs(APPS_DIR):
            app_rel = rel(app)

            for d in REQUIRED_DIRS_BASE:
                if not (app / d).exists():
                    errors.append(f"[E200] Falta directorio requerido '{d}' en {app_rel}/")

            for fname, allowed in MUST_LIVE_HERE.items():
                allowed_dirs = _normalize_allowed_dirs(allowed)
                for found in app.rglob(fname):
                    if not is_allowed_location(app, found, allowed_dirs):
                        allowed_str = ", ".join([("." if d == "." else d + "/") for d in allowed_dirs])
                        errors.append(f"[E310] '{fname}' en {rel(found.parent)}/; ubicaciones válidas: {allowed_str}")

            tests_dir = app / "tests"
            tests_py_locations = [
                app / "tests.py",
                tests_dir / "tests.py",
                tests_dir / "unit" / "tests.py",
                tests_dir / "integration" / "tests.py",
            ]
            has_tests_py = any(p.exists() for p in tests_py_locations)

            if tests_dir.exists():
                subdirs = [d.name for d in tests_dir.iterdir() if d.is_dir()]
                invalid_subdirs = [d for d in subdirs if d not in {"unit", "integration"}]
                if invalid_subdirs:
                    errors.append(f"[E212] {app_rel}/tests/ contiene carpetas no permitidas: {', '.join(invalid_subdirs)}. Usa solo unit/ e integration/.")

                if not has_tests_py and not {"unit", "integration"} & set(subdirs):
                    errors.append(f"[E213] {app_rel}/tests/ no tiene tests.py ni carpetas unit/ o integration/.")

                for py in tests_dir.glob("*.py"):
                    if py.name not in {"tests.py", "__init__.py"}:
                        errors.append(
                            f"[E325] {rel(py)} no permitido directamente en tests/. "
                            "Usa tests.py, __init__.py, o mueve a tests/unit/ o tests/integration/."
                        )

            for folder, hint in FORBID_PY_AT.items():
                parent = app / folder
                if parent.exists() and parent.is_dir():
                    for py in parent.glob("*.py"):
                        if py.name != "__init__.py":
                            errors.append(f"[E320] {rel(py)} no debe estar en '{folder}/'. {hint}")

            for py in app.glob("*.py"):
                if py.name not in ALLOWED_ROOT_FILES:
                    errors.append(f"[E330] Archivo no permitido en raíz de {app_rel}: {py.name}")

    if errors:
        print(" Estructura inválida / archivos fuera de lugar:")
        for e in errors:
            print(" -", e)
        print("\nReglas aplicadas:")
        print(" - Directorios base requeridos: " + ", ".join(REQUIRED_DIRS_BASE))
        print(" - Si existe tests/: solo carpetas unit/ e integration/ son válidas.")
        print(" - Si no hay tests.py: debe haber al menos una carpeta unit/ o integration/.")
        print(" - No .py sueltos en application/ o infrastructure/.")
        print(" - En raíz del app: solo " + ", ".join(sorted(ALLOWED_ROOT_FILES)))
        return 1

    print(" Estructura válida.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
