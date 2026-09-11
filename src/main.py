import json
import os
import re

 # HELPER FUNCTIONS

def mask_credit_card(card_str):
   
    # this one Masks a 16-digit credit card string then it hides sensitive digits.
    
    digits = [char for char in card_str if char.isdigit()]
    if len(digits) != 16:
        return card_str

    last_4 = "".join(digits[-4:])

    if "-" in card_str:
        return f"****-****-****-{last_4}"
    elif " " in card_str:
        return f"**** **** **** {last_4}"
    else:
        return f"************{last_4}"

def check_security_threats(text):
     # This one Scans text for malicious patterns and reports when some are detected
    
    threat_patterns = {
        "XSS Injection Attempt": r"<script.*?>.*?</script>|javascript:|onerror=",
        "SQL Injection Attempt": r"\b(DROP|DELETE|UPDATE|INSERT|SELECT)\s+(TABLE|FROM|INTO)\b|(?<!-)--(?!-)|';",
        "Prompt Injection Attempt": r"(?i)(ignore\s+all\s+previous\s+instructions|system\s+prompt|disregard\s+prior)",
    }

    detected_threats = {}

    for threat_type, pattern in threat_patterns.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            detected_threats[threat_type] = len(matches)

    return detected_threats

# MAIN SCRIPT 😁
file_path = "input/raw-text.txt"
output_dir = "output"
output_file = os.path.join(output_dir, "sample-output.json")

# Verify that the required input file exists before running extraction

if not os.path.exists(file_path):
    print(
        f"Error: Could not find '{file_path}'. Please check your folder structure again."
    )
else:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Data container for JSON output
    output_data = {}

    #  Security Threat Scan
    threats = check_security_threats(raw_text)
    output_data["security_scan"] = {
        "threats_detected": len(threats) > 0,
        "details": threats if threats else "No threats detected.",
    }

    if threats:
        print("⚠️ ⚠️ ⚠️ Some Malicious Content was Detected:")
        for threat_type, count in threats.items():
            print(f"   Flagged: {threat_type} ({count} occurrence(s))")
    else:
        print(" ✅  No malicious injection patterns were detected.")

    #  Emails
    general_pattern = r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
    extracted_emails = re.findall(general_pattern, raw_text)
    classified_emails = []

    print(f"\n Extracted exactly {len(extracted_emails)} valid emails(📩) ")
    for email in extracted_emails:
        domain = email.split("@")[-1].lower()
        if domain == "alumni.alueducation.com":
            category = "ALU Alumni               ✅ "
        elif domain == "si.alueducation.com":
            category = "ALU SI                   ✅ "
        elif domain == "alueducation.com":
            category = "ALU Staff                ✅ "
        else:
            category = "External(Not acceptable) ❌ "

        classified_emails.append({"email": email, "category": category})
        print(f"[{category:<22}] {email}")

    output_data["emails"] = classified_emails

    #  Credit Cards
    card_pattern = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"
    extracted_cards = re.findall(card_pattern, raw_text)
    masked_cards = [mask_credit_card(card) for card in extracted_cards]

    print(f"\n Extracted exactly {len(extracted_cards)} card-like numbers( 💳 ) ")
    for masked in masked_cards:
        print(f"Masked: {masked}")

    output_data["credit_cards"] = masked_cards

    #  Phone Numbers
    phone_pattern = r"(?:\+250\s?|0)7[2389]\d{1}[-\s]?\d{3}[-\s]?\d{3}\b"
    extracted_phones = re.findall(phone_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_phones)} phone numbers( ☎️ ) ")
    for phone in extracted_phones:
        print(f"[ Phone Number          ] {phone}")

    output_data["phone_numbers"] = extracted_phones

    #  Currency Amounts
    currency_pattern = (
        r"(?:\b(?:USD|RWF|EUR|Frw)\s?|[\$€£])\d+(?:,\d{3})*(?:\.\d{2})?\b"
    )
    extracted_currencies = re.findall(currency_pattern, raw_text)
    print(        f"\n Extracted exactly {len(extracted_currencies)} currency amounts( 💰 ) " )
    for amount in extracted_currencies:
        print(f"[Currency Amount     ] {amount}")

    output_data["currency_amounts"] = extracted_currencies

    #  Time Formats
    time_pattern = r"\b(?:1[0-2]|0?[1-9]):[0-5]\d\s?(?:AM|PM|am|pm)\b|\b(?:[01]?\d|2[0-3]):[0-5]\d\b"
    extracted_times = re.findall(time_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_times)} time formats( ⏰ ) ")
    for time_str in extracted_times:
        print(f"[Time Format           ] {time_str}")

    output_data["time_formats"] = extracted_times

    # Hashtags
    hashtag_pattern = r"#\w+"
    extracted_hashtags = re.findall(hashtag_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_hashtags)} hashtags( #️⃣ ) ")
    for tag in extracted_hashtags:
        print(f"[Hashtag              ] {tag}")

    output_data["hashtags"] = extracted_hashtags

    #  Save Structured Results to JSON
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as json_out:
        json.dump(output_data, json_out, indent=4)

    print(f"\n Results successfully saved( 💾 ) to '{output_file}'.")