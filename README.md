# 🕵️‍♀️ ALU Regex Data Extraction — Data Detective

---

## Overview
A secure Python regex-based program that I  designed to:
1.Process raw unstructured data and extract 6 specific types of structured data from raw text.
2.Validate input to ensure it is well-formed and does not contain unsafe or malicious content.
3.Handle realistic variations of data formats as they appear in the real world.

---

## How to Run
Run the main script from the root directory of the project using the terminal:

```bash
python3 src/main.py
```


## Data types Extracted
1.📩 Emails
2.💳 Credit Cards
3.☎️ Phone Numbers
4.💰 Currency amounts
5.⏰ Time Formats
6.#️⃣ Hashtags

## ALU email Classification
🎓 ALU Alumni: Matches emails ending in @alumni.alueducation.com.
💡 ALU SI: Matches emails ending in @si.alueducation.com.
🏫 ALU Staff: Matches emails ending in @alueducation.com.
🌐 External(Not acceptable): Any email that does not belong to the classifications above.

## Security considerations

🔒 Credit Card Redaction: Redacts all but the last 4 digits (e.g., `****-****-****-9424`) using `mask_credit_card()` to meet PCI-DSS compliance.

🛡️ Threat Detection Scanner: Pre-scans raw text to flag XSS, SQL injection, and LLM prompt injection payloads before extraction.

🎯 Decorative Dash False-Positive Fix: Uses negative lookarounds `(?<!-)--(?!-)` so SQL comment filters ignore decorative section divider lines.

🛑 No Plaintext Logging: Prevents sensitive unmasked financial data or malicious payloads from ever being logged or displayed in plain text.

## Known Limitations
📱 Regional Phone Bounds: The phone number regex is tailored specifically to Rwandan mobile formats (+250 / 07X) and will not capture generic international numbers.

💱 Symbol Position: The currency extractor expects prefixes (e.g $50 or RWF 100) and does not capture suffixed formats (e.g 50$ or 100 RWF).
