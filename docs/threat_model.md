# Threat Model: Password Security

## 1. Attack Vectors Simulated
- **Brute Force (Offline)**: Attacker has obtained the hash and uses high-end GPUs (e.g., NVIDIA RTX 4090 clusters) to guess trillions of combinations.
- **Dictionary Attack**: Attacker uses a pre-compiled list of common passwords and their variations.
- **Credential Stuffing**: Reuse of passwords from known data breaches.
- **Rule-Based Cracking**: Applying common mutations (capitalization, adding years like `2024`, special chars at the end).

## 2. Risk Classification
| Score | Label | Description |
|---|---|---|
| 0-20 | Critical | Instantly crackable by any basic script. |
| 21-40 | Weak | Vulnerable to basic dictionary/pattern attacks. |
| 41-60 | Moderate | Safe from casual attacks, but fails against dedicated GPU clusters. |
| 61-80 | Strong | Resistant to most common attack vectors; follows basic NIST guidelines. |
| 81-100 | Enterprise | High entropy, complex structure, resistant to supercomputing brute force. |

## 3. Mitigation Strategies (Advice Engine)
The platform suggests:
- **Increasing Length**: The single most effective way to increase entropy.
- **Mixing Character Sets**: Increasing the search space for attackers.
- **Avoiding Patterns**: Breaking the "rules" that cracking tools like *Hashcat* or *John the Ripper* use.
- **Passphrases**: Recommending multiple random words (e.g., `CorrectHorseBatteryStaple`) which are easier to remember but harder to crack.
