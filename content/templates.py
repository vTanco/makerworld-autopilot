"""
High-converting Markdown templates for MakerWorld descriptions.
Optimized for search rankings, user retention, and maximizing Boost token conversions.
"""

from typing import Dict, Any

MAKERWORLD_DESCRIPTION_TEMPLATE = """# {title}

{description_highlight}

---

### ✨ Features
- **Zero-Support Printing:** Engineered from the ground up to print cleanly without any supports or brim.
- **Dimensional Accuracy:** Tuned tolerances for seamless fit and finish.
- **Fast & Efficient:** Optimized geometry minimizes travel moves and filament waste.
- **Dimensions:** `{dimensions}`

---

### ⚙️ Recommended Print Settings
| Parameter | Value |
|---|---|
| **Printer** | Bambu Lab A1 / A1 mini / P1P / P1S / X1C |
| **Material** | PLA, PLA+, Matte PLA, or PETG |
| **Layer Height** | `{layer_height}` mm |
| **Wall Loops** | 3 - 4 walls |
| **Infill** | `{infill}` |
| **Supports** | **None required** |
| **Build Plate** | Textured PEI plate recommended |

---

### 🚀 Community & Boosts
If you found this model useful, please consider giving it a **Like** and dropping a **🚀 Boost**! Boost tokens help independent creators continue releasing high-quality functional prints for free.

Feel free to post photos of your makes in the comments section! Happy printing!
"""

REDDIT_POST_TEMPLATE = """[Free STL] Designed a {title} for my desk setup!

Hey everyone! I designed this {title} to solve my desk clutter issues. 
Key highlights:
- 100% support-free print
- Print time is around {print_time}
- Compatible with standard Bambu Lab and Prusa profiles

I've shared the 3MF print profile and STL on MakerWorld for free:
👉 Download: {makerworld_url}

Would love feedback or suggestions on variations to add!
"""

PINTEREST_PIN_TEMPLATE = """Title: Free 3D Print File: {title}
Description: Download this free 3D printable {title}. Support-free design, perfect for home and desk organization. Get the STL & 3MF file on MakerWorld!
Link: {makerworld_url}
"""
