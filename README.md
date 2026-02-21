## 📋 Краткая инструкция

### Использование
1. Положи ZIP-архивы с ресурспаками в папку `import`
2. Запусти скрипт:
```bash
python convert_models.py
```
3. Забирай готовые архивы с суффиксом `_converted` из папки `export`

## ⚙️ Функционал

- **Пакетная обработка** всех ZIP из папки `import`
- **Автопоиск** моделей по пути `assets/**/models/item/**`
- **Конвертация**:
  - `format_version: 1.9.0` → `1.21.11`
  - Старые повороты (`angle`/`axis`) → новый формат (`x`/`y`/`z`)
- **Безопасность**: оригиналы не меняются, временные файлы удаляются

## 📝 Пример

**Было:**
```json
"rotation": {"angle": 22.5, "axis": "x", "origin": [9.5, 7.1, 7]}
```

**Стало:**
```json
"rotation": {"x": 22.5, "y": 0, "z": 0, "origin": [9.5, 7.1, 7]}
```

---

# English version

## 📋 Quick Guide

### Setup
1. Save script as `convert_models.py`
2. Create folders next to it:
```
📁 import/    # put ZIPs here
📁 export/    # converted files go here
```

### Usage
1. Place ZIP resource packs in `import` folder
2. Run:
```bash
python convert_models.py
```
3. Get converted files with `_converted` suffix from `export`

## ⚙️ Features

- **Batch processing** all ZIPs from `import`
- **Auto-finds** models at `assets/**/models/item/**`
- **Converts**:
  - `format_version: 1.9.0` → `1.21.11`
  - Old rotations (`angle`/`axis`) → new format (`x`/`y`/`z`)
- **Safe**: originals unchanged, temp files auto-deleted

## 📝 Example

**Before:**
```json
"rotation": {"angle": 22.5, "axis": "x", "origin": [9.5, 7.1, 7]}
```

**After:**
```json
"rotation": {"x": 22.5, "y": 0, "z": 0, "origin": [9.5, 7.1, 7]}
```