#!/usr/bin/env python3
"""
Quick demo of the Mozart Dice Waltz Generator
"""

def simple_demo():
    """Run a simple demonstration without any dependencies"""
    print("🎼 Mozart's Musical Dice Game - Simple Demo 🎼")
    print("=" * 50)
    print()
    print("This is how Mozart's dice game works:")
    print()

    import random

    # Simplified table (just first few entries)
    sample_table = {
        2: [96, 22, 101, 14],
        3: [32, 6, 128, 63],
        4: [69, 95, 158, 13],
        5: [40, 17, 113, 85],
        6: [148, 74, 163, 45],
        7: [104, 157, 27, 167],
        8: [152, 60, 171, 53],
        9: [119, 84, 114, 50],
        10: [98, 142, 42, 156],
        11: [3, 87, 165, 61],
        12: [54, 130, 10, 103]
    }

    print("Rolling dice for first 4 measures:")
    print("Column:  A    B    C    D")
    print("-" * 25)

    measures = []
    for col in range(4):
        # Roll two dice
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2

        # Look up measure
        measure = sample_table[total][col]
        measures.append(measure)

        col_letter = chr(65 + col)
        print(f"Col {col_letter}:   {die1}+{die2}={total:2d} → Measure {measure:3d}")

    print()
    print(f"🎵 Your waltz begins with measures: {measures}")
    print()
    print("In the full version, this creates a complete 16-measure waltz!")
    print("Mozart provided 176 different musical measures to choose from.")
    print(f"Total possible waltzes: 11^16 = {11**16:,}")
    print()
    print("🚀 Try the full generator:")
    print("   python mozart_dice_waltz.py")
    print("   python mozart_dice_advanced.py  (with musical output)")

if __name__ == "__main__":
    simple_demo()