# 🔐 Multi-Algorithmic Password Strength Analyzer

A robust and extensible tool to evaluate password strength using multiple attack models. This analyzer estimates how long it would take to crack a password using various real-world methods like brute-force, dictionary attacks, and rule-based pattern analysis.

---

## 🚀 Features

- 🔢 Entropy-based strength evaluation
- 📖 Dictionary attack simulation
- ⚙️ Rule-based pattern matching (e.g., substitutions like `@` for `a`)
- 🔐 Brute-force time estimation
- 🌗 Dark mode enabled frontend UI
- 💡 Real-time strength feedback
- 📊 Summary of estimated crack times across algorithms
- 🧰 **Secret Vault with file upload & destruction mechanism**
- ❌ Marks as "immune" if crack time exceeds 100 years

---

## 🔒 Secret Vault Feature

This project includes a hidden **Secure Vault** feature:

- 🗝️ When a **pre-defined "special password"** is entered, a hidden vault UI is revealed.
- 📤 You can **upload sensitive files** to this vault.
- 🔁 To **view or download files**, you must re-enter the exact same password.
- ❌ If the password is incorrect during re-entry:
  - **All files in the vault are deleted permanently** for security.

> This ensures an extra layer of confidentiality and adds a destruct-on-wrong-password security mechanism.

---

## 🛠️ Tech Stack

| Layer         | Technology              |
|---------------|--------------------------|
| Backend       | Java                     |
| Frontend      | HTML, CSS, JavaScript    |
| Attack Models | Brute-force, Dictionary, Rule-based, Pattern Matching |
| Vault System  | Local File Handling (Java), Hidden UI Logic (JavaScript) |

---

## 🧪 Example Output

```json
{
  "password": "Str0ng@Passw0rd",
  "entropy": 56.7,
  "brute_force": "145 years",
  "dictionary_attack": "Immune",
  "rule_based": "2 hours",
  "pattern_matching": "Immune",
  "verdict": "Very Strong"
}
