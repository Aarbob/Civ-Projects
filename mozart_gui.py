#!/usr/bin/env python3
"""
Mozart Dice Waltz - Interactive GUI
Run this to get a popup window with the complete game!
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import time
import os
import subprocess
from pathlib import Path

try:
    from music21 import stream, note, meter, key, tempo, duration
    MUSIC21_AVAILABLE = True
except ImportError:
    MUSIC21_AVAILABLE = False

class MozartDiceGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎼 Mozart's Musical Dice Game 🎲")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # Game data
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

        self.current_waltz = []
        self.is_generating = False
        self.setup_ui()

    def setup_ui(self):
        """Create the GUI interface"""

        # Title
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(pady=20)

        title_label = tk.Label(title_frame, text="🎼 Mozart's Musical Dice Game 🎲",
                              font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Generate unique waltzes by rolling dice!",
                                 font=("Arial", 12), bg="#f0f0f0", fg="#7f8c8d")
        subtitle_label.pack()

        # Control buttons
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(pady=20)

        self.generate_btn = tk.Button(control_frame, text="🎲 Generate Waltz",
                                     font=("Arial", 14, "bold"), bg="#3498db", fg="white",
                                     command=self.start_generation, padx=20, pady=10)
        self.generate_btn.pack(side=tk.LEFT, padx=10)

        self.play_btn = tk.Button(control_frame, text="🎵 Play Music",
                                 font=("Arial", 14, "bold"), bg="#2ecc71", fg="white",
                                 command=self.play_music, padx=20, pady=10, state=tk.DISABLED)
        self.play_btn.pack(side=tk.LEFT, padx=10)

        self.save_btn = tk.Button(control_frame, text="💾 Save Files",
                                 font=("Arial", 14, "bold"), bg="#e74c3c", fg="white",
                                 command=self.save_files, padx=20, pady=10, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=10)

        # Dice display
        dice_frame = tk.Frame(self.root, bg="#f0f0f0")
        dice_frame.pack(pady=20)

        tk.Label(dice_frame, text="Current Roll:", font=("Arial", 14, "bold"),
                bg="#f0f0f0").pack()

        dice_display_frame = tk.Frame(dice_frame, bg="#f0f0f0")
        dice_display_frame.pack()

        self.dice1_var = tk.StringVar(value="?")
        self.dice2_var = tk.StringVar(value="?")
        self.sum_var = tk.StringVar(value="?")

        dice1_label = tk.Label(dice_display_frame, textvariable=self.dice1_var,
                              font=("Arial", 20, "bold"), bg="white", fg="black",
                              width=3, height=2, relief=tk.RAISED, bd=3)
        dice1_label.pack(side=tk.LEFT, padx=5)

        tk.Label(dice_display_frame, text="+", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)

        dice2_label = tk.Label(dice_display_frame, textvariable=self.dice2_var,
                              font=("Arial", 20, "bold"), bg="white", fg="black",
                              width=3, height=2, relief=tk.RAISED, bd=3)
        dice2_label.pack(side=tk.LEFT, padx=5)

        tk.Label(dice_display_frame, text="=", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)

        sum_label = tk.Label(dice_display_frame, textvariable=self.sum_var,
                            font=("Arial", 20, "bold"), bg="#f39c12", fg="white",
                            width=3, height=2, relief=tk.RAISED, bd=3)
        sum_label.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=10)

        # Results display
        results_frame = tk.Frame(self.root, bg="#f0f0f0")
        results_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Waltz sequence display
        sequence_frame = tk.LabelFrame(results_frame, text="Generated Waltz Sequence",
                                      font=("Arial", 12, "bold"), bg="#f0f0f0")
        sequence_frame.pack(fill=tk.X, pady=10)

        self.sequence_text = tk.Text(sequence_frame, height=4, font=("Courier", 11),
                                    bg="white", fg="#2c3e50", wrap=tk.WORD)
        self.sequence_text.pack(padx=10, pady=10, fill=tk.X)

        # Detailed results
        details_frame = tk.LabelFrame(results_frame, text="Generation Details",
                                     font=("Arial", 12, "bold"), bg="#f0f0f0")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.details_text = tk.Text(details_frame, height=10, font=("Courier", 10),
                                   bg="#ecf0f1", fg="#2c3e50")

        scrollbar = tk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)

        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Status bar
        self.status_var = tk.StringVar(value="Ready to generate Mozart waltz!")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             font=("Arial", 10), bg="#34495e", fg="white",
                             anchor=tk.W, padx=10, pady=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def start_generation(self):
        """Start waltz generation in a separate thread"""
        if self.is_generating:
            return

        self.is_generating = True
        self.generate_btn.config(state=tk.DISABLED)
        self.play_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)

        # Clear previous results
        self.sequence_text.delete(1.0, tk.END)
        self.details_text.delete(1.0, tk.END)
        self.current_waltz = []

        # Start generation in separate thread
        threading.Thread(target=self.generate_waltz, daemon=True).start()

    def generate_waltz(self):
        """Generate the waltz with animated dice rolling"""
        try:
            self.status_var.set("Generating waltz...")
            self.progress['maximum'] = 16
            self.progress['value'] = 0

            self.details_text.insert(tk.END, "🎲 Mozart's Musical Dice Game - Generation Log\n")
            self.details_text.insert(tk.END, "=" * 50 + "\n\n")

            # Generate first half
            self.details_text.insert(tk.END, "First Half (Measures 1-8):\n")
            columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

            for i in range(8):
                self.status_var.set(f"Rolling dice for position {i+1}/16...")

                # Animate dice rolling
                for _ in range(10):  # Animation frames
                    die1 = random.randint(1, 6)
                    die2 = random.randint(1, 6)
                    self.dice1_var.set(str(die1))
                    self.dice2_var.set(str(die2))
                    self.sum_var.set(str(die1 + die2))
                    self.root.update()
                    time.sleep(0.1)

                # Final roll
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                roll_sum = die1 + die2

                self.dice1_var.set(str(die1))
                self.dice2_var.set(str(die2))
                self.sum_var.set(str(roll_sum))

                measure = self.first_half_table[roll_sum][i]
                self.current_waltz.append(measure)

                self.details_text.insert(tk.END, f"  {columns[i]}: Roll {die1}+{die2}={roll_sum:2d} → Measure {measure:3d}\n")
                self.details_text.see(tk.END)

                self.progress['value'] = i + 1
                self.root.update()
                time.sleep(0.5)

            # Generate second half
            self.details_text.insert(tk.END, "\nSecond Half (Measures 9-16):\n")

            for i in range(8):
                self.status_var.set(f"Rolling dice for position {i+9}/16...")

                # Animate dice rolling
                for _ in range(10):
                    die1 = random.randint(1, 6)
                    die2 = random.randint(1, 6)
                    self.dice1_var.set(str(die1))
                    self.dice2_var.set(str(die2))
                    self.sum_var.set(str(die1 + die2))
                    self.root.update()
                    time.sleep(0.1)

                # Final roll
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                roll_sum = die1 + die2

                self.dice1_var.set(str(die1))
                self.dice2_var.set(str(die2))
                self.sum_var.set(str(roll_sum))

                measure = self.second_half_table[roll_sum][i]
                self.current_waltz.append(measure)

                self.details_text.insert(tk.END, f"  {columns[i]}: Roll {die1}+{die2}={roll_sum:2d} → Measure {measure:3d}\n")
                self.details_text.see(tk.END)

                self.progress['value'] = i + 9
                self.root.update()
                time.sleep(0.5)

            # Display results
            self.details_text.insert(tk.END, f"\n🎵 Complete Waltz Sequence:\n")
            self.details_text.insert(tk.END, f"   {' - '.join(map(str, self.current_waltz))}\n\n")

            sequence_str = f"Generated Mozart Waltz:\n{' - '.join(map(str, self.current_waltz))}\n\n"
            sequence_str += f"Total measures: 16\n"
            sequence_str += f"Unique waltz ID: {str(hash(tuple(self.current_waltz)))[-8:]}\n"
            sequence_str += f"This is one of {11**16:,} possible waltzes!"

            self.sequence_text.insert(tk.END, sequence_str)

            # Generate music files if music21 is available
            if MUSIC21_AVAILABLE:
                self.details_text.insert(tk.END, "🎼 Generating musical files...\n")
                self.generate_music_files()
            else:
                self.details_text.insert(tk.END, "⚠️  music21 not available - no musical files generated\n")

            self.status_var.set("Waltz generation complete!")
            self.play_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)

        except Exception as e:
            self.details_text.insert(tk.END, f"\n❌ Error: {str(e)}\n")
            self.status_var.set("Generation failed!")

        finally:
            self.is_generating = False
            self.generate_btn.config(state=tk.NORMAL)

    def generate_music_files(self):
        """Generate actual music files using music21"""
        try:
            # Create a simple waltz
            waltz = stream.Stream()
            waltz.append(key.KeySignature(0))  # C major
            waltz.append(meter.TimeSignature('3/4'))
            waltz.append(tempo.TempoIndication(number=120))

            # Simple note patterns based on measure numbers
            note_patterns = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

            for i, measure_num in enumerate(self.current_waltz):
                measure = stream.Measure(number=i+1)

                # Create a simple pattern based on the measure number
                pattern_idx = measure_num % len(note_patterns)
                base_note = note_patterns[pattern_idx]

                # Add three quarter notes for 3/4 time
                for j in range(3):
                    note_name = note_patterns[(pattern_idx + j) % len(note_patterns)]
                    n = note.Note(note_name, quarterLength=1.0)
                    measure.append(n)

                waltz.append(measure)

            # Save files with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.midi_file = f"mozart_waltz_{timestamp}.mid"
            self.xml_file = f"mozart_waltz_{timestamp}.musicxml"

            waltz.write('midi', fp=self.midi_file)
            waltz.write('musicxml', fp=self.xml_file)

            self.details_text.insert(tk.END, f"   ♪ MIDI file: {self.midi_file}\n")
            self.details_text.insert(tk.END, f"   ♪ MusicXML file: {self.xml_file}\n")

        except Exception as e:
            self.details_text.insert(tk.END, f"   ❌ Music generation error: {e}\n")

    def play_music(self):
        """Play the generated MIDI file"""
        if not self.current_waltz:
            messagebox.showwarning("No Waltz", "Generate a waltz first!")
            return

        try:
            if hasattr(self, 'midi_file') and os.path.exists(self.midi_file):
                # Try to open with default MIDI player
                if os.name == 'nt':  # Windows
                    os.startfile(self.midi_file)
                elif os.name == 'posix':  # macOS/Linux
                    subprocess.call(['open', self.midi_file])

                self.status_var.set("Playing music...")
                self.details_text.insert(tk.END, f"\n🎵 Playing: {self.midi_file}\n")
                self.details_text.see(tk.END)
            else:
                messagebox.showinfo("Music Playback",
                    f"Waltz sequence: {' - '.join(map(str, self.current_waltz))}\n\n"
                    "This represents your unique Mozart waltz!\n"
                    "Each number is one of Mozart's 176 pre-composed measures.")
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play music: {e}")

    def save_files(self):
        """Save waltz information to files"""
        if not self.current_waltz:
            messagebox.showwarning("No Waltz", "Generate a waltz first!")
            return

        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"mozart_waltz_log_{timestamp}.txt"

            with open(filename, 'w') as f:
                f.write("Mozart's Musical Dice Game - Waltz Log\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Measures: {' - '.join(map(str, self.current_waltz))}\n\n")
                f.write("Position breakdown:\n")

                columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                for i, measure in enumerate(self.current_waltz):
                    half = "First" if i < 8 else "Second"
                    pos = columns[i % 8]
                    f.write(f"{i+1:2d}. {half} half, Col {pos}: Measure {measure:3d}\n")

            messagebox.showinfo("Files Saved", f"Waltz log saved as:\n{filename}")
            self.status_var.set(f"Files saved: {filename}")

        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save files: {e}")

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🎼 Starting Mozart Dice Waltz GUI...")

    app = MozartDiceGUI()
    app.run()

if __name__ == "__main__":
    main()