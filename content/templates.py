"""
High-converting Markdown templates for MakerWorld descriptions.
Optimized for search rankings, user retention, and maximizing Boost token conversions.
"""

from typing import Dict, Any

MAKERWORLD_DESCRIPTION_TEMPLATE = """# {title}

{description_highlight}

---

## 📐 Technical Specifications
| Parameter | Value |
|---|---|
| Dimensions | {dimensions} |
| Estimated Weight | {weight}g (PLA) |
| Number of Parts | 1 (single piece) |
| Tolerances | ±0.2mm |
| Support Required | No |

## ⚙️ Recommended Print Settings
| Setting | Value |
|---|---|
| Printer | Bambu Lab A1 / A1 mini / P1S / X1C |
| Material | PLA, PLA+, Matte PLA, PETG |
| Layer Height | {layer_height}mm |
| Wall Loops | 3-4 |
| Infill | {infill} |
| Supports | None required |
| Build Plate | Textured PEI (recommended) |
| Estimated Time | {print_time} |

## 📦 What's Included
- ✅ Optimized STL file
- ✅ Bambu Studio 3MF project with pre-configured print profile
- ✅ Slice settings pre-loaded (just hit Print!)
- ✅ Real photos of printed model

## 🛠️ Print & Assembly Guide
1. **Download** the .3mf file and open in Bambu Studio
2. **Slice** — all settings are pre-configured for optimal results
3. **Print** — no supports, no brim needed
4. **Remove** from build plate and inspect
{assembly_steps}

## 💡 Pro Tips
- Use textured PEI plate at 60°C for best adhesion
- For PETG, increase bed temp to 75°C
- Standard speed recommended for first layer
- {material_tip}

## 🔗 More from this Creator
Check out my other functional prints for desk organization, 3D printer upgrades, and workshop tools!

## 🚀 Support the Community!
If you found this model useful, please **Like** and **🚀 Boost**!
Boost tokens help independent creators release more high-quality prints.
Share photos of your makes in the comments! Happy printing!
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
