import fitz  # PyMuPDF
import os, json

ingles_dir = r"C:\Users\freak\Preparacion Examenes\Ingles"
output = {}

for fname in sorted(os.listdir(ingles_dir)):
    if fname.lower().endswith(".pdf"):
        path = os.path.join(ingles_dir, fname)
        try:
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            output[fname] = text.strip()
        except Exception as e:
            output[fname] = f"ERROR: {e}"

# Write to JSON for analysis
out_path = os.path.join(ingles_dir, "_extracted.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(output)} PDFs")
for k, v in output.items():
    print(f"  {k}: {len(v)} chars")
