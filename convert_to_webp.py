from PIL import Image
import os

def convert_to_webp(input_path, output_path, quality=80):
    """Конвертирует изображение в WebP"""
    try:
        img = Image.open(input_path)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img.save(output_path, 'WEBP', quality=quality, optimize=True)
        
        original_size = os.path.getsize(input_path) / 1024
        new_size = os.path.getsize(output_path) / 1024
        reduction = 100 - (new_size/original_size*100)
        
        print(f"✅ {os.path.basename(input_path)} → {os.path.basename(output_path)}")
        print(f"   {original_size:.1f}KB → {new_size:.1f}KB (сжато на {reduction:.1f}%)")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

# Конвертируем все JPG в WebP
images_dir = "images"
for filename in os.listdir(images_dir):
    if filename.endswith('.jpg'):
        input_path = os.path.join(images_dir, filename)
        output_path = os.path.join(images_dir, filename.replace('.jpg', '.webp'))
        convert_to_webp(input_path, output_path, quality=75)