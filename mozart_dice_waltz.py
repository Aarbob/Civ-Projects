#!/usr/bin/env python3
"""
Mozart's Musical Dice Game - Waltz Generator
Based on Mozart's Musikalisches Würfelspiel K.516f

This program generates unique waltzes by rolling dice and looking up
pre-composed musical measures according to Mozart's original tables.
"""

import random
import json
from typing import List, Tuple

class MozartDiceWaltz:
    def __init__(self):
        # Number tables (Zahlentafel) - maps dice roll sums to measure numbers
        # First half of waltz (measures 1-8)
        self.first_half_table = {
            2:  [96, 22, 101, 14, 119, 44, 49, 2],
            3:  [32, 6, 128, 63, 146, 46, 134, 81],
            4:  [69, 95, 158, 13, 153, 55, 110, 24],
            5:  [40, 17, 113, 85, 161, 2, 159, 100],
            6:  [148, 74, 163, 45, 80, 97, 36, 107],
            7:  [104, 157, 27, 167, 154, 68, 118, 91],
            8:  [152, 60, 171, 53, 99, 133, 21, 127],
            9:  [119, 84, 114, 50, 140, 86, 169, 94],
            10: [98, 142, 42, 156, 75, 129, 62, 123],
            11: [3, 87, 165, 61, 135, 47, 147, 33],
            12: [54, 130, 10, 103, 28, 37, 106, 5]
        }

        # Second half of waltz (measures 9-16)
        self.second_half_table = {
            2:  [70, 121, 26, 9, 112, 49, 109, 14],
            3:  [117, 39, 126, 56, 174, 18, 116, 83],
            4:  [66, 139, 15, 132, 73, 58, 145, 79],
            5:  [90, 176, 7, 34, 67, 160, 52, 170],
            6:  [25, 143, 64, 125, 76, 136, 1, 93],
            7:  [138, 71, 150, 29, 101, 162, 23, 151],
            8:  [16, 155, 57, 175, 43, 168, 89, 172],
            9:  [120, 88, 48, 166, 51, 115, 72, 111],
            10: [65, 77, 19, 82, 137, 38, 149, 8],
            11: [102, 4, 31, 164, 144, 59, 173, 78],
            12: [35, 20, 108, 92, 12, 124, 44, 131]
        }

        # This would contain the actual musical measures in a real implementation
        # For now, we'll use placeholder notation
        self.measures = {}
        self._initialize_measures()

    def _initialize_measures(self):
        """Initialize musical measures - in a full implementation,
        these would contain actual musical notation data"""
        for i in range(1, 177):  # Measures 1-176
            # Placeholder - in reality these would be musical notation
            self.measures[i] = f"Measure_{i:03d}"

    def roll_dice(self) -> int:
        """Roll two dice and return the sum"""
        return random.randint(1, 6) + random.randint(1, 6)

    def generate_waltz(self) -> Tuple[List[int], List[int], List[str]]:
        """Generate a complete waltz by rolling dice and looking up measures"""
        print("🎲 Generating Mozart Waltz using dice rolls...\n")

        # Generate first half (8 measures)
        first_half_rolls = []
        first_half_measures = []

        print("First Half (Measures 1-8):")
        print("Column:   A    B    C    D    E    F    G    H")
        print("-" * 50)

        for column_idx in range(8):
            roll = self.roll_dice()
            measure_num = self.first_half_table[roll][column_idx]
            first_half_rolls.append(roll)
            first_half_measures.append(measure_num)
            column_letter = chr(65 + column_idx)  # A-H
            print(f"Roll {column_letter}:    {roll:2d} → Measure {measure_num:3d}")

        print()

        # Generate second half (8 measures)
        second_half_rolls = []
        second_half_measures = []

        print("Second Half (Measures 9-16):")
        print("Column:   A    B    C    D    E    F    G    H")
        print("-" * 50)

        for column_idx in range(8):
            roll = self.roll_dice()
            measure_num = self.second_half_table[roll][column_idx]
            second_half_rolls.append(roll)
            second_half_measures.append(measure_num)
            column_letter = chr(65 + column_idx)  # A-H
            print(f"Roll {column_letter}:    {roll:2d} → Measure {measure_num:3d}")

        # Combine both halves
        all_measures = first_half_measures + second_half_measures

        # Generate the sequence of musical measures
        musical_sequence = [self.measures[measure] for measure in all_measures]

        return first_half_measures, second_half_measures, musical_sequence

    def export_to_abc_notation(self, measures: List[int], filename: str):
        """Export the waltz to ABC notation format (simplified)"""
        with open(filename, 'w') as f:
            f.write("X:1\n")
            f.write("T:Mozart Dice Waltz\n")
            f.write("C:W.A. Mozart (Generated)\n")
            f.write("M:3/4\n")
            f.write("L:1/8\n")
            f.write("K:C\n")
            f.write("\n")

            # Write measure sequence as comments
            f.write("% Generated measure sequence:\n")
            for i, measure in enumerate(measures, 1):
                f.write(f"% {i:2d}: Measure {measure:3d}\n")

            f.write("\n")
            f.write("% Musical notation would go here\n")
            f.write("% Each measure from Mozart's original table\n")

        print(f"📝 Waltz exported to {filename}")

    def save_composition_log(self, first_half: List[int], second_half: List[int], filename: str):
        """Save the composition details to a JSON file"""
        composition_data = {
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "first_half_measures": first_half,
            "second_half_measures": second_half,
            "total_measures": len(first_half) + len(second_half),
            "measure_sequence": first_half + second_half
        }

        with open(filename, 'w') as f:
            json.dump(composition_data, f, indent=2)

        print(f"💾 Composition log saved to {filename}")

def main():
    """Main function to generate a waltz"""
    print("🎼 Mozart's Musical Dice Game - Waltz Generator 🎼")
    print("=" * 55)
    print()

    generator = MozartDiceWaltz()

    # Generate waltz
    first_half, second_half, musical_sequence = generator.generate_waltz()

    print(f"\n🎵 Generated Waltz Summary:")
    print(f"   First Half:  {first_half}")
    print(f"   Second Half: {second_half}")
    print(f"   Complete sequence: {first_half + second_half}")

    # Export files
    timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
    abc_filename = f"waltz_{timestamp}.abc"
    log_filename = f"composition_{timestamp}.json"

    generator.export_to_abc_notation(first_half + second_half, abc_filename)
    generator.save_composition_log(first_half, second_half, log_filename)

    print(f"\n✨ Your unique Mozart waltz has been generated!")
    print(f"   Total possible combinations: 11^16 = {11**16:,}")
    print(f"   Your waltz is one of these unique possibilities! 🎊")

if __name__ == "__main__":
    main()