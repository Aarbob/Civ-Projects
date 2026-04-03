# 🎼 Mozart's Musical Dice Game - Waltz Generator

An interactive implementation of Wolfgang Amadeus Mozart's famous "Musikalisches Würfelspiel" (K.516f), where you can generate infinite unique waltzes by simply rolling dice!

## 🎯 What is This?

In 1787, Mozart created a ingenious system that lets anyone compose waltzes without knowing music theory. You just roll two dice 16 times, look up the results in his special tables, and play the corresponding pre-composed musical measures. Each game creates a completely unique waltz!

## 🎲 How It Works

1. **Roll dice 8 times** for the first half of the waltz (measures 1-8)
2. **Roll dice 8 more times** for the second half (measures 9-16)  
3. **Look up each result** in Mozart's number tables (Zahlentafel)
4. **Play the measures** in order - you've composed a waltz!

With 11 possible dice combinations (2-12) and 16 positions, there are **11^16 = 45,949,729,863,572,161** possible waltzes!

## 🚀 Quick Start

### Simple Demo (No Dependencies)
```bash
python demo.py
```

### Basic Waltz Generator
```bash
python mozart_dice_waltz.py
```

### Advanced Version with Sheet Music
```bash
# First install dependencies
pip install -r requirements.txt

# Then run the advanced generator
python mozart_dice_advanced.py
```

## 📁 Files Included

- **`demo.py`** - Quick demonstration of how the dice game works
- **`mozart_dice_waltz.py`** - Full implementation with dice rolling and measure selection
- **`mozart_dice_advanced.py`** - Advanced version that generates actual sheet music files
- **`requirements.txt`** - Python dependencies for musical features
- **`README.md`** - This file

## 🎵 Generated Output

The generators create several types of output:

### Basic Version
- **Console output** showing dice rolls and selected measures
- **ABC notation file** (`.abc`) - text-based music format
- **Composition log** (`.json`) - complete record of the generation process

### Advanced Version  
- **MIDI file** (`.mid`) - playable in any music software
- **MusicXML file** (`.musicxml`) - open in MuseScore, Finale, Sibelius, etc.
- **ABC notation file** (`.abc`) - text format for music
- **Sequence file** (`.txt`) - human-readable measure list

## 🔧 Installation & Setup

1. **Clone or download** this project
2. **For basic features:** No installation needed - just run `python demo.py`
3. **For sheet music generation:** 
   ```bash
   pip install music21
   ```

## 🎨 Example Output

```
🎲 Generating Mozart Waltz using dice rolls...

First Half (Measures 1-8):
Column:   A    B    C    D    E    F    G    H
--------------------------------------------------
Roll A:    7 → Measure 104
Roll B:   11 → Measure  87
Roll C:    5 → Measure 113
Roll D:    9 → Measure  50
Roll E:    6 → Measure  80
Roll F:    8 → Measure 133
Roll G:   10 → Measure  62
Roll H:    4 → Measure  24

🎵 Generated Waltz Summary:
   Complete sequence: [104, 87, 113, 50, 80, 133, 62, 24, ...]
```

## 🎯 Historical Background

Mozart's Musikalisches Würfelspiel represents an early example of algorithmic composition. The system demonstrates how mathematical principles can be applied to create art, predating modern computational music by over 200 years.

The original consists of:
- **Two number tables** (Zahlentafel) mapping dice rolls to measure numbers
- **176 pre-composed measures** of waltz music in 3/4 time  
- **Simple rules** for combining them into complete pieces

## 🛠 Extending the Project

Want to enhance this further? Try:

- **Add Mozart's original measures** - transcribe the actual 176 measures from the historical manuscript
- **Create variations** - implement minuets, country dances, or other dice games
- **Add playback** - integrate real-time MIDI playback
- **Web interface** - create a browser-based version with audio
- **Analysis tools** - study the mathematical properties of the generated music

## 📚 References

- Mozart, W.A. "Musikalisches Würfelspiel" K.516f (c.1787)
- Original manuscript available in various music libraries
- Modern editions published by several music publishers

## 🎼 Usage Tips

1. **Listen to your waltzes** - open the `.mid` files in any music player
2. **Edit the sheet music** - open `.musicxml` files in notation software  
3. **Share your compositions** - each waltz is unique and yours to keep!
4. **Try multiple generations** - every run creates something completely different

---

*🎉 Happy composing! You're now part of a tradition that spans over 230 years of algorithmic music creation.*# Civ-Projects
