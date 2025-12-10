import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json("debug_output.jsonl", lines=True)

# Convert timestamp strings to datetime objects
df["timestamp_local"] = pd.to_datetime(df["timestamp_local"])



plt.figure(figsize=(10,6))


df["percent_used"] = (df["used_disk_space"] / df["total_disk_space"]) * 100
plt.plot(df["timestamp_local"], df["percent_used"], label="Percent Used", color="blue")
plt.xlabel("Time")
plt.ylabel("Disk Space (Percent Used)")
plt.title("Disk Usage Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()