import os
import re


def mask_credit_card(card_str):
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


file_path = "input/raw-text.txt"

if not os.path.exists(file_path):
    print(
        f"Error: Could not find '{file_path}'. Please check your folder structure again."
    )
else:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 📩 Emails
    general_pattern = r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
    extracted_emails = re.findall(general_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_emails)} valid email(s) ")
    for email in extracted_emails:
        domain = email.split("@")[-1].lower()
        if domain == "alumni.alueducation.com":
            category = "ALU Alumni"
        elif domain == "si.alueducation.com":
            category = "ALU SI"
        elif domain == "alueducation.com":
            category = "ALU Staff"
        else:
            category = "External(Not acceptable)"
        print(f"[{category:<22}] {email}")

    # 💳 Credit Cards
    card_pattern = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"
    extracted_cards = re.findall(card_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_cards)} card-like number(s) ")
    for raw_card in extracted_cards:
        masked = mask_credit_card(raw_card)
        print(f"Masked: {masked}")

    # ☎️ Phone Numbers (Rwandan + International formats)
    phone_pattern = r"(?:\+250\s?|0)7[8389]\d{1}[-\s]?\d{3}[-\s]?\d{3}\b"
    extracted_phones = re.findall(phone_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_phones)} phone number(s) ")
    for phone in extracted_phones:
        print(f"[Phone Number          ]                 {phone}")

    # 💰 Currency Amounts (Matches $, USD, RWF, EUR with numbers)
    currency_pattern = r"(?:(?<=\s)|(?<=^)|(?<=\())[\$€£]?\s?\d+(?:,\d{3})*(?:\.\d{2})?\b|\b(?:USD|RWF|EUR|Frw)\s?\d+(?:,\d{3})*(?:\.\d{2})?\b"
    extracted_currencies = re.findall(currency_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_currencies)}             currency amount(s) ")
    for amount in extracted_currencies:
        print(f"[Currency Amount       ]                 {amount}")

    # ⏰ Time Formats (Matches 12-hour and  24-hour )
    time_pattern = r"\b(?:1[0-2]|0?[1-9]):[0-5]\d\s?(?:AM|PM|am|pm)\b|\b(?:[01]?\d|2[0-3]):[0-5]\d\b"
    extracted_times = re.findall(time_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_times)} time format(s) ")
    for time_str in extracted_times:
        print(f"[Time Format           ]                 {time_str}")

    # #️⃣ Hashtags (Matches #word style tags)
    hashtag_pattern = r"#\w+"
    extracted_hashtags = re.findall(hashtag_pattern, raw_text)
    print(f"\n Extracted exactly {len(extracted_hashtags)} hashtag(s) ")
    for tag in extracted_hashtags:
        print(f"[Hashtag               ]                 {tag}")
