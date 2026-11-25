import os
from PIL import Image, ImageDraw, ImageFont

def generate_assets(output_dir="packaging/msix_build/Assets"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Base source
    src_path = "icon-512.png"
    if not os.path.exists(src_path):
        src_path = "logo.png"
    
    base_img = Image.open(src_path).convert("RGBA")
    
    # Specs: (filename, width, height, is_wide, is_splash)
    specs = [
        ("StoreLogo.png", 50, 50, False, False),
        ("StoreLogo.scale-100.png", 50, 50, False, False),
        ("StoreLogo.scale-125.png", 63, 63, False, False),
        ("StoreLogo.scale-150.png", 75, 75, False, False),
        ("StoreLogo.scale-200.png", 100, 100, False, False),
        ("StoreLogo.scale-400.png", 200, 200, False, False),

        ("Square44x44Logo.png", 44, 44, False, False),
        ("Square44x44Logo.scale-100.png", 44, 44, False, False),
        ("Square44x44Logo.scale-125.png", 55, 55, False, False),
        ("Square44x44Logo.scale-150.png", 66, 66, False, False),
        ("Square44x44Logo.scale-200.png", 88, 88, False, False),
        ("Square44x44Logo.scale-400.png", 176, 176, False, False),
        ("Square44x44Logo.targetsize-16.png", 16, 16, False, False),
        ("Square44x44Logo.targetsize-24.png", 24, 24, False, False),
        ("Square44x44Logo.targetsize-32.png", 32, 32, False, False),
        ("Square44x44Logo.targetsize-48.png", 48, 48, False, False),
        ("Square44x44Logo.targetsize-256.png", 256, 256, False, False),

        ("Square150x150Logo.png", 150, 150, False, False),
        ("Square150x150Logo.scale-100.png", 150, 150, False, False),
        ("Square150x150Logo.scale-125.png", 188, 188, False, False),
        ("Square150x150Logo.scale-150.png", 225, 225, False, False),
        ("Square150x150Logo.scale-200.png", 300, 300, False, False),
        ("Square150x150Logo.scale-400.png", 600, 600, False, False),

        ("Wide310x150Logo.png", 310, 150, True, False),
        ("Wide310x150Logo.scale-100.png", 310, 150, True, False),
        ("Wide310x150Logo.scale-125.png", 388, 188, True, False),
        ("Wide310x150Logo.scale-150.png", 465, 225, True, False),
        ("Wide310x150Logo.scale-200.png", 620, 300, True, False),
        ("Wide310x150Logo.scale-400.png", 1240, 600, True, False),

        ("SplashScreen.png", 620, 300, False, True),
        ("SplashScreen.scale-100.png", 620, 300, False, True),
        ("SplashScreen.scale-125.png", 775, 375, False, True),
        ("SplashScreen.scale-150.png", 930, 450, False, True),
        ("SplashScreen.scale-200.png", 1240, 600, False, True),
        ("SplashScreen.scale-400.png", 2480, 1200, False, True),
    ]

    bg_color = (13, 17, 23, 255) # #0D1117 deep obsidian navy

    for filename, w, h, is_wide, is_splash in specs:
        target = Image.new("RGBA", (w, h), bg_color)
        
        # Determine icon size to place inside
        if is_wide:
            icon_dim = int(h * 0.8)
            resized_icon = base_img.resize((icon_dim, icon_dim), Image.LANCZOS)
            offset_x = (w - icon_dim) // 2
            offset_y = (h - icon_dim) // 2
            target.paste(resized_icon, (offset_x, offset_y), resized_icon)
        elif is_splash:
            icon_dim = int(min(w, h) * 0.6)
            resized_icon = base_img.resize((icon_dim, icon_dim), Image.LANCZOS)
            offset_x = (w - icon_dim) // 2
            offset_y = (h - icon_dim) // 2
            target.paste(resized_icon, (offset_x, offset_y), resized_icon)
        else:
            # Square icon: take up ~85% of square
            icon_dim = max(1, int(w * 0.85))
            resized_icon = base_img.resize((icon_dim, icon_dim), Image.LANCZOS)
            offset_x = (w - icon_dim) // 2
            offset_y = (h - icon_dim) // 2
            target.paste(resized_icon, (offset_x, offset_y), resized_icon)
            
        out_file = os.path.join(output_dir, filename)
        target.save(out_file, "PNG")
        print(f"Generated {out_file} ({w}x{h})")

    # Also generate .ico file for Win32 application icon
    ico_img = base_img.resize((256, 256), Image.LANCZOS)
    ico_path = os.path.join(output_dir, "app_icon.ico")
    ico_img.save(ico_path, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"Generated {ico_path}")

if __name__ == "__main__":
    generate_assets()

