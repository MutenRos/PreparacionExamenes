import json, os

ingles_dir = r"C:\Users\freak\Preparacion Examenes\Ingles"
with open(os.path.join(ingles_dir, "_extracted.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# Show first PDF content for analysis
for k, v in list(data.items())[:3]:
    print(f"\n{'='*60}")
    print(f"FILE: {k}")
    print(f"{'='*60}")
    print(v[:2000])
