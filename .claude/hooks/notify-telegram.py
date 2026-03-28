#!/usr/bin/env python3
"""
Claude Code → Telegram Notification Hook
Feuert bei: Notification (Permission-Request u.a.), Stop (Task fertig)
"""
import json
import sys
import urllib.request
import urllib.parse

def _load_env(path="/root/.claude/hooks/.env"):
    env = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env

_env = _load_env()
TELEGRAM_TOKEN = _env.get("TELEGRAM_TOKEN", "")
CHAT_ID = _env.get("CHAT_ID", "")

ICONS = {
    "Notification": "🔔",
    "Stop": "✅",
}

def send(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }).encode()
    req = urllib.request.Request(url, data=data)
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Telegram send failed: {e}", file=sys.stderr)

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    event = payload.get("hook_event_name", "")
    message = payload.get("message", "").strip()
    cwd = payload.get("cwd", "")

    icon = ICONS.get(event, "🤖")

    if event == "Stop":
        # Stop-Event hat keine message — generische Meldung
        if not message:
            message = "Task abgeschlossen."
    elif not message:
        sys.exit(0)

    # Kürze langen Message-Text
    if len(message) > 300:
        message = message[:297] + "..."

    # Arbeitsverzeichnis nur wenn relevant (nicht /root)
    context = f"\n<code>{cwd}</code>" if cwd and cwd != "/root" else ""

    text = f"{icon} <b>Claude Code</b>{context}\n\n{message}"
    send(text)

if __name__ == "__main__":
    main()
