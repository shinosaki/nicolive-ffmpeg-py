import re
import subprocess
from pathlib import Path

def extract_program_id(input: str) -> str | None:
    match = re.search(r'(lv\d+)', input)
    return match.group(1) if match is not None else None

def exec_ffmpeg(args: list[str], ffmpeg_path = 'ffmpeg', log_path: Path | None = None):
    command = [ffmpeg_path, *args]
    print(' '.join(command))

    if log_path is None:
        proc = subprocess.Popen(command)
    else:
        log_path.write_text(' '.join(command) + '\n', encoding='utf-8')
        with log_path.open('a') as f:
            proc = subprocess.Popen(command,
                stdout=f,
                stderr=subprocess.STDOUT,
            )

    return proc
