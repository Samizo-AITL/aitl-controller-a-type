from PIL import Image
import os

# 変換したい PNG ファイル名（あなたの画像名に合わせてください）
png_file = "data/aitl_full_demo_ideal.png"

# 出力PDF名
pdf_file = png_file.replace(".png", ".pdf")

# PNG を開く
image = Image.open(png_file)

# PDF として保存
image.save(pdf_file, "PDF", resolution=150.0)

print("Converted to PDF:", pdf_file)
