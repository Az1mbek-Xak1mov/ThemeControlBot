from pathlib import Path
import datetime

HISTORY_DIR = Path("chat_history")
HISTORY_DIR.mkdir(exist_ok=True)

def _history_file_for(chat_id: int) -> Path:
    return HISTORY_DIR / f"{chat_id}.txt"

def append_message_to_file(chat_id: int, text: str) -> None:
    p = _history_file_for(chat_id)
    line = f"{datetime.datetime.utcnow().isoformat()}|{text.replace(chr(10), ' ')}\n"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(line)

def get_last_n_messages_from_file(chat_id: int, n: int = 3) -> list[str]:
    p = _history_file_for(chat_id)
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()
    messages = []
    for ln in lines:
        ln = ln.rstrip("\n")
        if "|" in ln:
            _, msg = ln.split("|", 1)
        else:
            msg = ln
        messages.append(msg)
    last_n = messages[-n:]
    return last_n  # already oldest->newest

def delete_history_file(chat_id: int) -> bool:
    p = _history_file_for(chat_id)
    try:
        p.unlink()
        return True
    except FileNotFoundError:
        return False