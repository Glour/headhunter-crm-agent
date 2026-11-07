import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_environment_files_preserve_explicit_overrides_with_bash(tmp_path):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    for name in ("load_project_env.sh", "hh_telegram_env.sh"):
        shutil.copy(ROOT / "scripts" / name, scripts / name)
    (tmp_path / ".env").write_text(
        "HH_CHAT_REPLY_SEND=1\nHH_CRM_DB_PATH=from-project\n", encoding="utf-8"
    )
    secrets = tmp_path / "secrets.env"
    secrets.write_text(
        "HH_CHAT_REPLY_SEND=1\nHH_CRM_DB_PATH=from-secrets\nHH_TELEGRAM_LIMIT=25\n",
        encoding="utf-8",
    )
    env = {
        "PATH": os.environ["PATH"],
        "HH_CRM_DB_PATH": "",
        "HH_CHAT_REPLY_SEND": "0",
        "HH_TELEGRAM_SECRETS_FILE": str(secrets),
    }
    result = subprocess.run(
        [
            "bash",
            "-c",
            'source "$1"; printf "%s\\n" "$HH_CHAT_REPLY_SEND" "${HH_CRM_DB_PATH-unset}" "$HH_TELEGRAM_LIMIT"',
            "bash",
            str(scripts / "hh_telegram_env.sh"),
        ],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    # Empty DB override is preserved while sourcing, then the documented default applies.
    assert result.stdout.splitlines() == ["0", "./data/hh_crm.sqlite3", "25"]
