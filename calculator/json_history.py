import json
from pathlib import Path


HISTORY_FILE = Path(__file__).resolve().parent.parent / "calculation_history.json"


def read_calculation_history(file_path: Path | str | None = None) -> list[dict]:
    """Return saved records, treating a missing or empty file as an empty history."""
    path = Path(file_path) if file_path is not None else HISTORY_FILE
    if not path.exists():
        return []

    contents = path.read_text(encoding="utf-8")
    if not contents.strip():
        return []

    try:
        history = json.loads(contents)
    except json.JSONDecodeError as exc:
        raise ValueError(f"History file contains invalid JSON: {path}") from exc

    if not isinstance(history, list):
        raise ValueError(f"History file must contain a JSON list: {path}")

    return history


def save_calculation_record(
    record: dict, file_path: Path | str | None = None
) -> None:
    """Append one calculation record while preserving existing history."""
    if not isinstance(record, dict):
        raise TypeError("A calculation history record must be a dictionary.")

    path = Path(file_path) if file_path is not None else HISTORY_FILE
    history = read_calculation_history(path)
    history.append(record)

    path.write_text(
        json.dumps(history, indent=4, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
