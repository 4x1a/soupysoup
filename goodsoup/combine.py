from fpdf import FPDF

# Create a new PDF
pdf = FPDF()
pdf.add_page()

# Use a Unicode-compatible font (required for emoji, accented characters, etc.)
pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
pdf.set_font("DejaVu", size=10)

# Read the text file
with open("combined.txt", "r", encoding="utf-8") as file:
    for line in file:
        pdf.multi_cell(190, 6, line.strip())

# Save the PDF
pdf.output("output.pdf")
print("✅ PDF saved as output.pdf")
