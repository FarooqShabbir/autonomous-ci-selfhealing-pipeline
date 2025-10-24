# simulate_app.py
import random, time, sys

print("Starting synthetic app build/test...")
time.sleep(2)
if random.random() < 0.4:
    print("❌ Simulated failure: transient network error")
    sys.exit(1)
else:
    print("✅ Simulated success")
    sys.exit(0)
