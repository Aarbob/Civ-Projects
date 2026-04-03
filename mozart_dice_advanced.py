#!/usr/bin/env python3
"""
Advanced Mozart Dice Waltz Generator with Real Musical Output
Requires: pip install music21
"""

import random
from typing import List, Dict, Tuple
try:
    from music21 import stream, note, meter, key, tempo, bar, duration
    MUSIC21_AVAILABLE = True
except ImportError:
    MUSIC21_AVAILABLE = False
    print("⚠️  music21 not installed. Run: pip install music21")

class AdvancedMozartDiceWaltz:
    def __init__(self):
        # Same number tables as before
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

        # Sample musical measures (simplified for demonstration)
        self.musical_measures = self._create_sample_measures()

    def _create_sample_measures(self) -> Dict[int, List[str]]:
        """Create sample musical measures. In a full implementation,
        these would be Mozart's actual 176 pre-composed measures."""

        # Simple waltz patterns in 3/4 time
        waltz_patterns = [
            ["C4", "E4", "G4"],      # I chord
            ["F4", "A4", "C5"],      # IV chord
            ["G4", "B4", "D5"],      # V chord
            ["C4", "G4", "E4"],      # I chord variation
            ["D4", "F4", "A4"],      # ii chord
            ["E4", "G4", "C5"],      # vi chord
            ["F4", "C4", "A4"],      # IV chord variation
            ["G4", "D4", "B4"],      # V chord variation
            ["A4", "C5", "E5"],      # vi chord high
            ["B4", "D5", "F5"],      # vii chord
        ]

        measures = {}
        for i in range(1, 177):
            # Cycle through patterns with variations
            pattern_idx = i % len(waltz_patterns)
            base_pattern = waltz_patterns[pattern_idx]

            # Add some random variations
            if random.random() < 0.3:  # 30% chance of variation
                # Transpose up or down occasionally
                variation = random.choice([-1, 1])
                measures[i] = [self._transpose_note(note, variation) for note in base_pattern]
            else:
                measures[i] = base_pattern.copy()

        return measures

    def _transpose_note(self, note_str: str, semitones: int) -> str:
        """Simple note transposition"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note_name = note_str[:-1]
        octave = int(note_str[-1])

        note_idx = notes.index(note_name) if note_name in notes else 0
        new_idx = (note_idx + semitones) % 12

        # Handle octave changes
        if note_idx + semitones >= 12:
            octave += 1
        elif note_idx + semitones < 0:
            octave -= 1

        return f"{notes[new_idx]}{octave}"

    def generate_waltz_with_music(self) -> Tuple[List[int], stream.Stream if MUSIC21_AVAILABLE else None]:
        """Generate waltz and create actual musical score"""
        print("🎲 Generating Mozart Waltz with musical notation...\n")

        # Roll dice for both halves
        all_measures = []
        all_rolls = []

        print("Dice Rolls and Measure Selection:")
        print("=" * 40)

        # First half
        print("First Half:")
        for i in range(8):
            roll = random.randint(1, 6) + random.randint(1, 6)
            measure_num = self.first_half_table[roll][i]
            all_measures.append(measure_num)
            all_rolls.append(roll)
            print(f"  {chr(65+i)}: Roll {roll:2d} → Measure {measure_num:3d}")

        print("\nSecond Half:")
        for i in range(8):
            roll = random.randint(1, 6) + random.randint(1, 6)
            measure_num = self.second_half_table[roll][i]
            all_measures.append(measure_num)
            all_rolls.append(roll)
            print(f"  {chr(65+i)}: Roll {roll:2d} → Measure {measure_num:3d}")

        # Create musical score if music21 is available
        if MUSIC21_AVAILABLE:
            score = self._create_musical_score(all_measures)
        else:
            score = None

        return all_measures, score

    def _create_musical_score(self, measures: List[int]) -> stream.Stream:
        """Create a music21 Score object from the generated measures"""
        if not MUSIC21_AVAILABLE:
            return None

        # Create the score
        waltz = stream.Stream()

        # Add metadata
        waltz.append(key.KeySignature(0))  # C major
        waltz.append(meter.TimeSignature('3/4'))
        waltz.append(tempo.TempoIndication(number=120))

        # Add measures
        for i, measure_num in enumerate(measures):
            measure = stream.Measure(number=i+1)

            # Get the notes for this measure
            notes_in_measure = self.musical_measures[measure_num]

            # Add notes with quarter note duration (3 per measure in 3/4 time)
            for note_str in notes_in_measure:
                n = note.Note(note_str, quarterLength=1.0)
                measure.append(n)

            waltz.append(measure)

        return waltz

    def save_musical_files(self, score: stream.Stream, measures: List[int], base_filename: str):
        """Save the waltz in various formats"""
        if not MUSIC21_AVAILABLE or score is None:
            print("⚠️  Cannot save musical files - music21 not available")
            return

        try:
            # Save as MIDI
            midi_file = f"{base_filename}.mid"
            score.write('midi', fp=midi_file)
            print(f"🎵 MIDI saved: {midi_file}")

            # Save as MusicXML (can be opened in most music notation software)
            xml_file = f"{base_filename}.musicxml"
            score.write('musicxml', fp=xml_file)
            print(f"📄 MusicXML saved: {xml_file}")

            # Save as ABC notation (text format)
            abc_file = f"{base_filename}.abc"
            score.write('abc', fp=abc_file)
            print(f"📝 ABC notation saved: {abc_file}")

        except Exception as e:
            print(f"⚠️  Error saving files: {e}")

        # Always save the measure sequence
        with open(f"{base_filename}_sequence.txt", 'w') as f:
            f.write("Mozart Dice Waltz - Generated Measure Sequence\n")
            f.write("=" * 50 + "\n\n")
            f.write("Measures used: " + " ".join(map(str, measures)) + "\n\n")

            for i, measure_num in enumerate(measures, 1):
                half = "First" if i <= 8 else "Second"
                pos = ((i - 1) % 8) + 1
                f.write(f"{i:2d}. {half} half, position {pos}: Measure {measure_num:3d}\n")

        print(f"📋 Sequence saved: {base_filename}_sequence.txt")

def main():
    """Main function"""
    print("🎼 Advanced Mozart Dice Waltz Generator 🎼")
    print("=" * 50)

    if not MUSIC21_AVAILABLE:
        print("\n💡 To generate actual sheet music, install music21:")
        print("   pip install music21")
        print("\nContinuing with basic functionality...\n")

    generator = AdvancedMozartDiceWaltz()
    measures, score = generator.generate_waltz_with_music()

    print(f"\n🎵 Complete waltz sequence:")
    print(f"   {' '.join(map(str, measures))}")

    # Save files
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"mozart_waltz_{timestamp}"

    if MUSIC21_AVAILABLE and score:
        generator.save_musical_files(score, measures, base_filename)
        print(f"\n✨ Waltz generated successfully!")
        print(f"   Open the .musicxml file in MuseScore, Finale, or Sibelius")
        print(f"   Play the .mid file in any MIDI player")
    else:
        # Save at least the sequence
        with open(f"{base_filename}_sequence.txt", 'w') as f:
            f.write("Mozart Dice Waltz - Generated Measure Sequence\n")
            f.write("=" * 50 + "\n\n")
            f.write("Measures: " + " ".join(map(str, measures)) + "\n")
        print(f"📋 Measure sequence saved to: {base_filename}_sequence.txt")

if __name__ == "__main__":
    main()