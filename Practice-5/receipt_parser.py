import os
import re
import json

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "raw.txt")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()
lines = text.splitlines()
# 1. All prices
price_pattern = r"\b\d{1,3}(?: \d{3})*,\d{2}\b"
prices = [float(p.replace(" ", "").replace(",", ".")) for p in re.findall(price_pattern, text)]

# 2. Data and time
dt_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
datetime_str = f"{dt_match.group(1)} {dt_match.group(2)}" if dt_match else None

# 3. Sposob Oplaty
payment_method = None
for i, line in enumerate(lines):
    if "Банковская карта" in line or "Наличными" in line:
        payment_method = line.replace(":", "").strip()
        break

# 4. Total amount
total_amount = None
for i, line in enumerate(lines):
    if "ИТОГО" in line:
        for j in range(i + 1, min(i + 5, len(lines))):
            if re.fullmatch(price_pattern, lines[j].strip()):
                total_amount = float(lines[j].replace(" ", "").replace(",", "."))
                break

# 5. Tovars
items = []
i = 0
while i < len(lines):
    if re.match(r"^\d+\.$", lines[i].strip()):
        item_no = int(lines[i].strip()[:-1])
        i += 1

        name_parts = []
        while i < len(lines) and not re.match(r"^\d+,\d{3}\s*x\s*[\d ]+,\d{2}$", lines[i].strip()):
            if lines[i].strip() and lines[i].strip() != "Стоимость":
                name_parts.append(lines[i].strip())
            i += 1

        qty = unit_price = line_total = None

        if i < len(lines):
            m = re.match(r"^(\d+,\d{3})\s*x\s*([\d ]+,\d{2})$", lines[i].strip())
            if m:
                qty = float(m.group(1).replace(",", "."))
                unit_price = float(m.group(2).replace(" ", "").replace(",", "."))
                i += 1

        while i < len(lines):
            if re.fullmatch(price_pattern, lines[i].strip()):
                line_total = float(lines[i].replace(" ", "").replace(",", "."))
                break
            if re.match(r"^\d+\.$", lines[i].strip()):
                i -= 1
                break
            i += 1

        items.append({
            "item_no": item_no,
            "name": " ".join(name_parts),
            "quantity": qty,
            "unit_price": unit_price,
            "line_total": line_total
        })
    i += 1

# 6. vivod
result = {
    "datetime": datetime_str,
    "payment_method": payment_method,
    "total_amount": total_amount,
    "all_prices": prices,
    "items": items
}
print(json.dumps(result, ensure_ascii=False, indent=2))