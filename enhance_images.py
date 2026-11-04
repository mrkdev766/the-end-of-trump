#!/usr/bin/env python3
"""
enhance_images.py
Intelligently crops and enhances all 47 original images for 1080p documentary:
- Exact 16:9 aspect ratio cropping (no stretching or squashing)
- 35/65 top-bias crop for portrait / character photos to keep heads in frame
- High-fidelity Lanczos 2560x1440 upscaling
- Unsharp mask sharpening and contrast/vibrancy grading
"""

import os, glob
from PIL import Image, ImageEnhance, ImageFilter

SRC_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc/assets/images"
DST_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc/assets/images_enhanced"
os.makedirs(DST_DIR, exist_ok=True)

TARGET_AR = 16.0 / 9.0
OUT_W, OUT_H = 2560, 1440

def enhance_image(src_path, dst_path):
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    ar = w / h
    
    # 1. Exact 16:9 Crop without stretching
    if abs(ar - TARGET_AR) > 0.01:
        if ar > TARGET_AR:
            # Too wide: crop width centered
            target_w = int(h * TARGET_AR)
            left = (w - target_w) // 2
            im_cropped = im.crop((left, 0, left + target_w, h))
        else:
            # Too tall: crop height with 35% top bias to keep heads/faces in frame
            target_h = int(w / TARGET_AR)
            diff = h - target_h
            top = int(diff * 0.35)
            im_cropped = im.crop((0, top, w, top + target_h))
    else:
        im_cropped = im
        
    # 2. High-quality 2K/1440p Lanczos Upscaling
    im_upscaled = im_cropped.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS)
    
    # 3. Unsharp Mask Sharpening
    im_sharp = im_upscaled.filter(ImageFilter.UnsharpMask(radius=2.2, percent=145, threshold=2))
    
    # 4. Cinematic Contrast & Saturation Boost
    im_contrast = ImageEnhance.Contrast(im_sharp).enhance(1.06)
    im_final = ImageEnhance.Color(im_contrast).enhance(1.04)
    
    # 5. Save with maximum JPEG quality
    im_final.save(dst_path, "JPEG", quality=95, subsampling=0)

def main():
    imgs = sorted(glob.glob(os.path.join(SRC_DIR, "*.jpg")))
    print(f"=== Enhancing and 16:9 Cropping {len(imgs)} Images ===")
    for idx, img in enumerate(imgs, 1):
        filename = os.path.basename(img)
        dst_path = os.path.join(DST_DIR, filename)
        enhance_image(img, dst_path)
        print(f"[{idx}/{len(imgs)}] Enhanced: {filename} -> 2560x1440 16:9")
        
    print("\n✅ All images successfully enhanced, sharpened, and cropped to 16:9!")

if __name__ == "__main__":
    main()
