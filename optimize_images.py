"""
Скрипт для оптимизации изображений сайта MEMORY
Сжимает изображения до оптимального размера без потери качества
"""

from PIL import Image
import os

def optimize_image(input_path, output_path, quality=80, max_width=1200):
    """
    Оптимизирует изображение
    
    Args:
        input_path: Путь к исходному изображению
        output_path: Путь для сохранения оптимизированного изображения
        quality: Качество JPEG (1-100), рекомендуется 75-85
        max_width: Максимальная ширина в пикселях
    """
    try:
        img = Image.open(input_path)
        
        # Изменяем размер если слишком большое
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)
            print(f"  Изменен размер: {img.width}x{img.height}px")
        
        # Конвертируем в RGB если нужно
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Сохраняем с оптимизацией
        img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
        
        # Показываем результат
        original_size = os.path.getsize(input_path) / 1024
        new_size = os.path.getsize(output_path) / 1024
        reduction = 100 - (new_size/original_size*100)
        
        print(f"✅ {os.path.basename(input_path)}")
        print(f"   {original_size:.1f}KB → {new_size:.1f}KB (сжато на {reduction:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обработке {input_path}: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Оптимизация изображений для сайта MEMORY\n")
    
    images_dir = "images"
    
    if not os.path.exists(images_dir):
        print(f"❌ Папка {images_dir} не найдена!")
        print("   Запусти скрипт из папки clothing-website")
        return
    
    # Настройки оптимизации
    settings = {
        'last-memory-tshirt': {'quality': 80, 'max_width': 1200},  # Фото товара
        'кот.jpg': {'quality': 75, 'max_width': 1920},  # Фон героя
        'logo': {'quality': 85, 'max_width': 500},  # Логотип
        'background': {'quality': 70, 'max_width': 1920}  # Фон
    }
    
    optimized_count = 0
    total_original = 0
    total_optimized = 0
    
    for filename in os.listdir(images_dir):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        
        input_path = os.path.join(images_dir, filename)
        
        # Определяем настройки для файла
        quality = 80
        max_width = 1200
        
        for key, config in settings.items():
            if key in filename:
                quality = config['quality']
                max_width = config['max_width']
                break
        
        # Создаем имя для оптимизированного файла
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(images_dir, f"{name}_optimized{ext}")
        
        print(f"\n📸 Обрабатываю: {filename}")
        print(f"   Качество: {quality}%, Макс. ширина: {max_width}px")
        
        if optimize_image(input_path, output_path, quality, max_width):
            optimized_count += 1
            total_original += os.path.getsize(input_path) / 1024
            total_optimized += os.path.getsize(output_path) / 1024
    
    # Итоги
    print("\n" + "="*50)
    print(f"✅ Оптимизировано файлов: {optimized_count}")
    print(f"📊 Общий размер ДО: {total_original:.1f} KB")
    print(f"📊 Общий размер ПОСЛЕ: {total_optimized:.1f} KB")
    print(f"💾 Сэкономлено: {total_original - total_optimized:.1f} KB ({100 - (total_optimized/total_original*100):.1f}%)")
    print("="*50)
    
    print("\n📝 Следующие шаги:")
    print("1. Проверь оптимизированные изображения (_optimized)")
    print("2. Если качество устраивает, замени оригиналы:")
    print("   - Удали старые файлы")
    print("   - Переименуй _optimized файлы (убери _optimized)")
    print("3. Загрузи на Vercel")
    print("\n🎉 Готово!")

if __name__ == "__main__":
    main()
