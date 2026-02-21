import os
import json
import zipfile
import shutil
import tempfile
from pathlib import Path
import glob

# Папки для работы
IMPORT_DIR = "import"
EXPORT_DIR = "export"
TEMP_PACK_DIR = "temp_pack"

# Создаем необходимые папки
os.makedirs(IMPORT_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

def convert_rotation(old_rotation):
    """
    Конвертирует старый формат поворота (с angle/axis) в новый (с x/y/z).
    Если поворот уже в новом формате, возвращает как есть.
    """
    if not isinstance(old_rotation, dict):
        return old_rotation
    
    # Если это уже новый формат (есть ключи x, y, z)
    if "x" in old_rotation or "y" in old_rotation or "z" in old_rotation:
        return old_rotation
    
    # Конвертируем из старого формата
    if "angle" in old_rotation and "axis" in old_rotation:
        angle = old_rotation["angle"]
        axis = old_rotation["axis"]
        origin = old_rotation.get("origin", [0, 0, 0])
        
        # Создаем новый формат поворота
        new_rotation = {"origin": origin}
        
        # Устанавливаем значение для соответствующей оси
        if axis == "x":
            new_rotation["x"] = angle
            new_rotation["y"] = 0
            new_rotation["z"] = 0
        elif axis == "y":
            new_rotation["x"] = 0
            new_rotation["y"] = angle
            new_rotation["z"] = 0
        elif axis == "z":
            new_rotation["x"] = 0
            new_rotation["y"] = 0
            new_rotation["z"] = angle
        
        return new_rotation
    
    return old_rotation

def convert_model(model_data):
    """
    Конвертирует модель в новый формат (1.21.11).
    """
    if not isinstance(model_data, dict):
        return model_data
    
    # Меняем format_version
    if "format_version" in model_data:
        model_data["format_version"] = "1.21.11"
    
    # Конвертируем rotations в элементах
    if "elements" in model_data and isinstance(model_data["elements"], list):
        for element in model_data["elements"]:
            if "rotation" in element:
                element["rotation"] = convert_rotation(element["rotation"])
    
    return model_data

def process_zip_file(zip_path):
    """
    Обрабатывает один ZIP-файл: распаковывает, конвертирует модели, создает новый ZIP.
    """
    print(f"Обработка: {zip_path.name}")
    
    # Создаем временную папку для этого архива
    with tempfile.TemporaryDirectory(dir=TEMP_PACK_DIR) as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        # Распаковываем архив
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir_path)
        
        # Ищем все JSON-файлы моделей по нужному пути
        model_files = []
        for root, dirs, files in os.walk(temp_dir_path):
            root_path = Path(root)
            # Проверяем, что путь содержит 'models/item'
            if 'models' in root_path.parts and 'item' in root_path.parts:
                for file in files:
                    if file.endswith('.json'):
                        model_files.append(Path(root) / file)
        
        if not model_files:
            print(f"  В архиве {zip_path.name} не найдено моделей предметов")
            return
        
        # Конвертируем каждую модель
        converted_count = 0
        for model_file in model_files:
            try:
                with open(model_file, 'r', encoding='utf-8') as f:
                    model_data = json.load(f)
                
                # Конвертируем модель
                converted_data = convert_model(model_data)
                
                # Сохраняем обратно
                with open(model_file, 'w', encoding='utf-8') as f:
                    json.dump(converted_data, f, indent=2, ensure_ascii=False)
                
                converted_count += 1
                print(f"  Конвертировано: {model_file.relative_to(temp_dir_path)}")
                
            except Exception as e:
                print(f"  Ошибка при конвертации {model_file}: {e}")
        
        # Создаем новый ZIP-файл
        output_filename = zip_path.stem + "_converted.zip"
        output_path = Path(EXPORT_DIR) / output_filename
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for file_path in temp_dir_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(temp_dir_path)
                    zip_ref.write(file_path, arcname)
        
        print(f"  Создан архив: {output_path}")
        print(f"  Всего конвертировано моделей: {converted_count}")
        print()

def main():
    # Очищаем/создаем папку для временных распаковок
    if os.path.exists(TEMP_PACK_DIR):
        shutil.rmtree(TEMP_PACK_DIR)
    os.makedirs(TEMP_PACK_DIR)
    
    # Ищем все ZIP-файлы в папке import
    zip_files = list(Path(IMPORT_DIR).glob("*.zip"))
    
    if not zip_files:
        print(f"В папке '{IMPORT_DIR}' не найдено ZIP-файлов.")
        print("Поместите туда архивы с ресурспаками для конвертации.")
        return
    
    print(f"Найдено ZIP-файлов: {len(zip_files)}")
    print()
    
    # Обрабатываем каждый ZIP-файл
    for zip_file in zip_files:
        process_zip_file(zip_file)
    
    # Очищаем временную папку
    shutil.rmtree(TEMP_PACK_DIR)
    
    print("Готово! Все файлы обработаны.")

if __name__ == "__main__":
    main()