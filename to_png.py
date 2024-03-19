import cairosvg
import os

for root, _, files in os.walk("images"):
    new_dir = root.replace("images", "pngs")
    os.makedirs(new_dir, exist_ok=True)
    for filename in files:
        if filename.endswith(".svg"):
            new_filename = filename.replace(".svg", ".png")
            cairosvg.svg2png(
                url=os.path.join(root, filename),
                write_to=os.path.join(new_dir, new_filename),
            )
