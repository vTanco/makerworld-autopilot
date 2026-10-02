"""
High-converting Markdown templates for MakerWorld descriptions.
Optimized for search rankings, user retention, and maximizing Boost token conversions.
"""

from typing import Dict, Any

MAKERWORLD_DESCRIPTION_TEMPLATE = """<h2>{title}</h2>
<p>{description_highlight}</p>

<h3>📐 Specifications</h3>
<ul>
<li><strong>Dimensions:</strong> {dimensions}</li>
<li><strong>Weight:</strong> ~{weight}g (PLA)</li>
<li><strong>Parts:</strong> 1 piece, no assembly</li>
<li><strong>Supports:</strong> None required</li>
</ul>

<h3>⚙️ Print Settings</h3>
<ul>
<li><strong>Printer:</strong> Bambu Lab A1 / A1 mini / P1S / X1C</li>
<li><strong>Material:</strong> PLA, PLA+, PETG</li>
<li><strong>Layer Height:</strong> {layer_height}mm</li>
<li><strong>Infill:</strong> {infill}</li>
<li><strong>Supports:</strong> None needed ✨</li>
<li><strong>Build Plate:</strong> Textured PEI recommended</li>
<li><strong>Print Time:</strong> ~{print_time}</li>
</ul>

<h3>📦 What's Included</h3>
<ul>
<li>✅ Optimized STL file</li>
<li>✅ Bambu Studio 3MF with pre-configured print profile</li>
<li>✅ Ready to print — just hit Print!</li>
<li>✅ Real photos of the printed model</li>
</ul>

<h3>🛠️ How to Print</h3>
<p>1. <strong>Download</strong> the .3mf and open in Bambu Studio<br>
2. <strong>Slice</strong> — settings are pre-configured<br>
3. <strong>Print</strong> — no supports needed<br>
4. <strong>Remove</strong> from build plate<br>
{assembly_steps}</p>

<h3>💡 Pro Tips</h3>
<p>• Textured PEI plate at 60°C for best adhesion<br>
• For PETG: increase bed temp to 75°C<br>
• {material_tip}</p>

<h3>🚀 Like & Boost!</h3>
<p>If this model was useful, please give it a <strong>Like</strong> and a <strong>🚀 Boost</strong>! It helps independent creators keep sharing free designs. Share your makes in the comments!</p>

<hr>

<h3>🇪🇸 Español</h3>
<p>{description_highlight_es}</p>

<h3>📐 Especificaciones</h3>
<ul>
<li><strong>Dimensiones:</strong> {dimensions}</li>
<li><strong>Peso:</strong> ~{weight}g (PLA)</li>
<li><strong>Piezas:</strong> 1 pieza, sin ensamblaje</li>
<li><strong>Soportes:</strong> No necesarios</li>
</ul>

<h3>🛠️ Cómo imprimir</h3>
<p>1. <strong>Descarga</strong> el archivo .3mf y ábrelo en Bambu Studio<br>
2. <strong>Slice</strong> — la configuración ya viene incluida<br>
3. <strong>Imprime</strong> — sin soportes<br>
4. <strong>Retira</strong> de la cama de impresión</p>

<h3>🚀 ¡Apoya a la comunidad!</h3>
<p>Si te ha resultado útil, dale <strong>Like</strong> y <strong>🚀 Boost</strong>. ¡Comparte fotos de tus impresiones en los comentarios!</p>
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
