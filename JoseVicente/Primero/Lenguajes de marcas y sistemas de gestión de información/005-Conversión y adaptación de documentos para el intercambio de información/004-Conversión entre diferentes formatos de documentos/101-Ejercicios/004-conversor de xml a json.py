import json
import xmltodict

# Input / output filenames (change as needed)
INPUT_XML = "persona.xml"
OUTPUT_JSON = "persona2.json"

# Elements that should always be treated as arrays (lists)
# Add tag names here if necessary: "item", "book", "producto", etc.
FORCE_LIST_TAGS = ("item", "book")

def xml_to_json(input_xml: str, output_json: str) -> None:
    # 1. Read XML file
    with open(input_xml, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # 2. Parse XML to Python dict
    #    force_list: ensures certain tags are *always* lists
    data = xmltodict.parse(xml_content, force_list=FORCE_LIST_TAGS)

    # 3. Save as pretty-printed JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved JSON to: {output_json}")

if __name__ == "__main__":
    xml_to_json(INPUT_XML, OUTPUT_JSON)

