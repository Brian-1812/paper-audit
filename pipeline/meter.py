"""Read the account's usage windows from one tiny Haiku call (the rate_limit_event of stream-json output).

Usage: python3 -I pipeline/meter.py      -> prints {"five_hour": 0.77, "seven_day": 0.93}
The meter reads the whole account, so other sessions of the same account move it too.
With an API key there is no such event, and read() returns None values (the guards then never pause).
"""
import json, subprocess, sys


def read():
    p = subprocess.run(["claude", "-p", "--model", "haiku", "--safe-mode", "--strict-mcp-config", "--no-session-persistence",
                        "--tools", "", "--output-format", "stream-json", "--verbose"],
                       input="Reply OK.", capture_output=True, text=True, timeout=180)
    for line in p.stdout.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") == "rate_limit_event":
            w = d["rate_limit_info"].get("unifiedWindows", {})
            m = {k: w.get(k, {}).get("utilization") for k in ("five_hour", "seven_day")}
            m.update({k + "_resets": w.get(k, {}).get("resetsAt") for k in ("five_hour", "seven_day")})
            return m
    return {"five_hour": None, "seven_day": None, "five_hour_resets": None, "seven_day_resets": None}


if __name__ == "__main__":
    print(json.dumps(read()))
