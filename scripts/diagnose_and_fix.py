#!/usr/bin/env python3
"""
Simple diagnoser & self-healer for simulate_app.py

Behavior:
- Runs the app once to collect logs (but run_output.log is already present from test step)
- Attempts lightweight fixes (sleep + retry up to N times)
- Writes 'HEALED' to heal_status.txt if remediation succeeds, otherwise 'UNHEALED'
- Writes diagnostics to diagnostics.log
"""

import subprocess, time, sys, os

RUN_CMD = ["python", "simulate_app.py"]
MAX_RETRIES = 2              # how many retry attempts (beyond initial failure)
RETRY_WAIT = 3               # seconds between retries
DIAG_FILE = "diagnostics.log"
HEAL_FILE = "heal_status.txt"

def run_and_capture(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, out

def append_log(msg):
    with open(DIAG_FILE, "a") as f:
        f.write(msg + "\n")

def main():
    # Start fresh
    if os.path.exists(DIAG_FILE):
        os.remove(DIAG_FILE)
    if os.path.exists(HEAL_FILE):
        os.remove(HEAL_FILE)

    append_log("=== Self-Heal diagnostics started ===")
    append_log(f"Running initial command: {' '.join(RUN_CMD)}")
    rc, out = run_and_capture(RUN_CMD)
    append_log(f"Initial returncode: {rc}")
    append_log("Initial output:\n" + out)

    if rc == 0:
        append_log("Initial run succeeded unexpectedly (test job indicated failure). Marking as HEALED.")
        with open(HEAL_FILE, "w") as f:
            f.write("HEALED")
        return 0

    # Lightweight remediation attempts
    for attempt in range(1, MAX_RETRIES + 1):
        append_log(f"Attempt {attempt}/{MAX_RETRIES} remediation: wait {RETRY_WAIT}s then retry")
        time.sleep(RETRY_WAIT)
        rc2, out2 = run_and_capture(RUN_CMD)
        append_log(f"Retry returncode: {rc2}")
        append_log("Retry output:\n" + out2)
        if rc2 == 0:
            append_log("Remediation succeeded on retry.")
            with open(HEAL_FILE, "w") as f:
                f.write("HEALED")
            return 0

    # If here, remediation failed
    append_log("All remediation attempts failed. Producing richer diagnostics...")

    # Add system information to aid triage
    try:
        uname = subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout.strip()
        append_log("System info: " + uname)
    except Exception as e:
        append_log("Could not run uname: " + str(e))

    # Copy last outputs into diagnostic log (if run_output.log exists)
    if os.path.exists("run_output.log"):
        append_log("----- begin run_output.log -----")
        append_log(open("run_output.log").read())
        append_log("----- end run_output.log -----")

    append_log("Marking as UNHEALED")
    with open(HEAL_FILE, "w") as f:
        f.write("UNHEALED")
    return 2

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
