import os
import subprocess

from tqdm import tqdm


for root, _, files in os.walk("images"):
    new_dir = root.replace("images", "pngs")
    os.makedirs(new_dir, exist_ok=True)
    print(root)
    for filename in tqdm(files):
        if filename.endswith(".svg"):
            new_filename = filename.replace(".svg", ".png")
            subprocess.run(['/Applications/Inkscape.app/Contents/MacOS/inkscape', f'--export-filename={os.path.join(new_dir, new_filename)}', os.path.join(root, filename)])
