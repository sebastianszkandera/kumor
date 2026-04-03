# Worth It? - Mobile App

A mobile-friendly app to calculate if an item is worth working for based on your hourly rate.

## Features

✨ **New Features:**
- 📱 **Mobile-Optimized UI** - Works seamlessly on iOS and Android
- 💾 **Item History** - Track all items you've calculated with automatic saving
- 📸 **Photo Support** - Add photos of items you're considering
- 💭 **Opinion Tracking** - Save your thoughts on why you want items
- 📊 **Data Persistence** - All data saved in `worth_it_data.json`
- 🎯 **Quick Calculator** - Tab-based interface for easy navigation

## Installation

### For Desktop Testing:
```bash
pip install -r requirements.txt
python project3.py
```

### For Android:
1. Install Kivy on your machine
2. Use Buildozer to create an APK:
```bash
pip install buildozer
buildozer android debug
```

### For iOS:
1. Use Toolchain for Kivy
2. Follow [Kivy iOS Guide](https://kivy.org/doc/stable/guide/packaging-ios.html)

## Usage

1. **Calculator Tab**: 
   - Enter your hourly rate
   - Add item name and price
   - Write your opinion
   - Select a photo (optional)
   - Click "Calculate Worth"

2. **History Tab**:
   - View all your saved items
   - See calculation results
   - Clear history when needed

## Data Storage
Data is automatically saved to `worth_it_data.json` in the same directory.

## Mobile Build Instructions

### Android (using Buildozer):
```bash
buildozer android debug
```

### iOS (using Toolchain):
```bash
toolchain create WorthIt . --requirements=python3,kivy
```
