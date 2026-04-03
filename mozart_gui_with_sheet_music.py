#!/usr/bin/env python3
"""
Mozart Dice Waltz - Interactive GUI with Visual Sheet Music Display
Run this to get a popup window with dice game AND sheet music display!
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import time
import os
import subprocess
from pathlib import Path
import tempfile
from PIL import Image, ImageTk

try:
    from music21 import stream, note, meter, key, tempo, duration, environment
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    MUSIC21_AVAILABLE = True

    # Configure music21 for headless operation
    environment.set('musescoreDirectPNGPath', None)
    environment.set('directoryScratch', tempfile.gettempdir())

except ImportError:
    MUSIC21_AVAILABLE = False

class MozartDiceGUIWithSheetMusic:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎼 Mozart's Musical Dice Game - With Sheet Music 🎼")
        self.root.geometry("1200x900")
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
        self.current_score = None
        self.is_generating = False
        self.sheet_music_image = None
        self.setup_ui()

    def setup_ui(self):
        """Create the GUI interface with sheet music display"""

        # Create main container with two panels
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel for controls and details
        left_panel = tk.Frame(main_container, bg="#f0f0f0", width=600)
        main_container.add(left_panel)

        # Right panel for sheet music
        right_panel = tk.Frame(main_container, bg="white", width=600)
        main_container.add(right_panel)

        # === LEFT PANEL ===

        # Title
        title_frame = tk.Frame(left_panel, bg="#f0f0f0")
        title_frame.pack(pady=10)

        title_label = tk.Label(title_frame, text="🎼 Mozart's Dice Game 🎲",
                              font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Generate & View Sheet Music!",
                                 font=("Arial", 10), bg="#f0f0f0", fg="#7f8c8d")
        subtitle_label.pack()

        # Control buttons
        control_frame = tk.Frame(left_panel, bg="#f0f0f0")
        control_frame.pack(pady=15)

        self.generate_btn = tk.Button(control_frame, text="🎲 Generate",
                                     font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                                     command=self.start_generation, padx=15, pady=8)
        self.generate_btn.grid(row=0, column=0, padx=5)

        self.play_btn = tk.Button(control_frame, text="🎵 Play",
                                 font=("Arial", 12, "bold"), bg="#2ecc71", fg="white",
                                 command=self.play_music, padx=15, pady=8, state=tk.DISABLED)
        self.play_btn.grid(row=0, column=1, padx=5)

        self.save_btn = tk.Button(control_frame, text="💾 Save",
                                 font=("Arial", 12, "bold"), bg="#e74c3c", fg="white",
                                 command=self.save_files, padx=15, pady=8, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=2, padx=5)

        # Dice display
        dice_frame = tk.Frame(left_panel, bg="#f0f0f0")
        dice_frame.pack(pady=10)

        tk.Label(dice_frame, text="Current Roll:", font=("Arial", 12, "bold"),
                bg="#f0f0f0").pack()

        dice_display_frame = tk.Frame(dice_frame, bg="#f0f0f0")
        dice_display_frame.pack()

        self.dice1_var = tk.StringVar(value="?")
        self.dice2_var = tk.StringVar(value="?")
        self.sum_var = tk.StringVar(value="?")

        dice1_label = tk.Label(dice_display_frame, textvariable=self.dice1_var,
                              font=("Arial", 16, "bold"), bg="white", fg="black",
                              width=2, height=1, relief=tk.RAISED, bd=3)
        dice1_label.pack(side=tk.LEFT, padx=3)

        tk.Label(dice_display_frame, text="+", font=("Arial", 14, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=3)

        dice2_label = tk.Label(dice_display_frame, textvariable=self.dice2_var,
                              font=("Arial", 16, "bold"), bg="white", fg="black",
                              width=2, height=1, relief=tk.RAISED, bd=3)
        dice2_label.pack(side=tk.LEFT, padx=3)

        tk.Label(dice_display_frame, text="=", font=("Arial", 14, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=3)

        sum_label = tk.Label(dice_display_frame, textvariable=self.sum_var,
                            font=("Arial", 16, "bold"), bg="#f39c12", fg="white",
                            width=2, height=1, relief=tk.RAISED, bd=3)
        sum_label.pack(side=tk.LEFT, padx=3)

        # Progress bar
        self.progress = ttk.Progressbar(left_panel, length=300, mode='determinate')
        self.progress.pack(pady=10)

        # Waltz sequence display
        sequence_frame = tk.LabelFrame(left_panel, text="Generated Sequence",
                                      font=("Arial", 10, "bold"), bg="#f0f0f0")
        sequence_frame.pack(fill=tk.X, pady=5, padx=10)

        self.sequence_text = tk.Text(sequence_frame, height=3, font=("Courier", 9),
                                    bg="white", fg="#2c3e50", wrap=tk.WORD)
        self.sequence_text.pack(padx=5, pady=5, fill=tk.X)

        # Detailed results
        details_frame = tk.LabelFrame(left_panel, text="Generation Log",
                                     font=("Arial", 10, "bold"), bg="#f0f0f0")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

        self.details_text = tk.Text(details_frame, height=8, font=("Courier", 8),
                                   bg="#ecf0f1", fg="#2c3e50")

        scrollbar = tk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)

        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready to generate Mozart waltz!")
        status_bar = tk.Label(left_panel, textvariable=self.status_var,
                             font=("Arial", 9), bg="#34495e", fg="white",
                             anchor=tk.W, padx=10, pady=3)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # === RIGHT PANEL - SHEET MUSIC ===

        sheet_music_frame = tk.LabelFrame(right_panel, text="🎼 Generated Sheet Music",
                                         font=("Arial", 14, "bold"), bg="white")
        sheet_music_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for sheet music display
        self.sheet_canvas = tk.Canvas(sheet_music_frame, bg="white", width=550, height=700)
        sheet_scrollbar = tk.Scrollbar(sheet_music_frame, orient=tk.VERTICAL, command=self.sheet_canvas.yview)
        self.sheet_canvas.configure(yscrollcommand=sheet_scrollbar.set)

        self.sheet_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        sheet_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Initial message
        self.show_initial_sheet_message()

    def show_initial_sheet_message(self):
        """Show initial message in sheet music area"""
        self.sheet_canvas.delete("all")
        self.sheet_canvas.create_text(275, 350, text="🎼\n\nGenerate a waltz to see\nsheet music here!",
                                     font=("Arial", 16), fill="#7f8c8d", justify=tk.CENTER)

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
        self.show_initial_sheet_message()
        self.current_waltz = []

        # Start generation in separate thread
        threading.Thread(target=self.generate_waltz, daemon=True).start()

    def generate_waltz(self):
        """Generate the waltz with animated dice rolling"""
        try:
            self.status_var.set("Generating waltz...")
            self.progress['maximum'] = 16
            self.progress['value'] = 0

            self.details_text.insert(tk.END, "🎲 Mozart's Musical Dice Game\n")
            self.details_text.insert(tk.END, "=" * 35 + "\n\n")

            # Generate first half
            self.details_text.insert(tk.END, "First Half (1-8):\n")
            columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

            for i in range(8):
                self.status_var.set(f"Rolling dice {i+1}/16...")
                self.animate_dice_and_select(i, True, columns[i])

            # Generate second half
            self.details_text.insert(tk.END, "\nSecond Half (9-16):\n")

            for i in range(8):
                self.status_var.set(f"Rolling dice {i+9}/16...")
                self.animate_dice_and_select(i, False, columns[i])

            # Display results
            self.display_results()

            # Generate sheet music
            if MUSIC21_AVAILABLE:
                self.status_var.set("Generating sheet music...")
                self.generate_and_display_sheet_music()
            else:
                self.show_no_music21_message()

            self.status_var.set("Waltz complete!")
            self.play_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)

        except Exception as e:
            self.details_text.insert(tk.END, f"\n❌ Error: {str(e)}\n")
            self.status_var.set("Generation failed!")

        finally:
            self.is_generating = False
            self.generate_btn.config(state=tk.NORMAL)

    def animate_dice_and_select(self, position, is_first_half, column):
        """Animate dice rolling and select measure"""
        # Animate dice rolling
        for _ in range(8):  # Animation frames
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            self.dice1_var.set(str(die1))
            self.dice2_var.set(str(die2))
            self.sum_var.set(str(die1 + die2))
            self.root.update()
            time.sleep(0.08)

        # Final roll
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        roll_sum = die1 + die2

        self.dice1_var.set(str(die1))
        self.dice2_var.set(str(die2))
        self.sum_var.set(str(roll_sum))

        # Select measure
        table = self.first_half_table if is_first_half else self.second_half_table
        measure = table[roll_sum][position]
        self.current_waltz.append(measure)

        self.details_text.insert(tk.END, f"  {column}: {die1}+{die2}={roll_sum:2d} → {measure:3d}\n")
        self.details_text.see(tk.END)

        progress_value = position + (0 if is_first_half else 8) + 1
        self.progress['value'] = progress_value
        self.root.update()
        time.sleep(0.3)

    def display_results(self):
        """Display the waltz sequence results"""
        self.details_text.insert(tk.END, f"\n🎵 Complete Sequence:\n")
        self.details_text.insert(tk.END, f"   {' '.join(map(str, self.current_waltz))}\n\n")

        sequence_str = f"Generated Mozart Waltz:\n{' - '.join(map(str, self.current_waltz))}\n\n"
        sequence_str += f"Measures: 16 | Unique ID: {str(hash(tuple(self.current_waltz)))[-6:]}\n"
        sequence_str += f"One of {11**16:,} possible waltzes!"

        self.sequence_text.insert(tk.END, sequence_str)

    def generate_and_display_sheet_music(self):
        """Generate sheet music and display it in the GUI"""
        try:
            # Create musical score
            waltz = stream.Stream()
            waltz.append(key.KeySignature(0))  # C major
            waltz.append(meter.TimeSignature('3/4'))
            waltz.append(tempo.TempoIndication(number=120))

            # Create more sophisticated musical patterns
            major_scale = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
            chord_tones = {
                'I': ['C4', 'E4', 'G4'],
                'ii': ['D4', 'F4', 'A4'],
                'iii': ['E4', 'G4', 'B4'],
                'IV': ['F4', 'A4', 'C5'],
                'V': ['G4', 'B4', 'D5'],
                'vi': ['A4', 'C5', 'E5'],
                'vii': ['B4', 'D5', 'F5']
            }

            chord_progression = ['I', 'V', 'vi', 'IV', 'I', 'IV', 'V', 'I']

            for i, measure_num in enumerate(self.current_waltz):
                measure = stream.Measure(number=i+1)

                # Choose chord based on measure number and position
                chord_idx = measure_num % len(chord_progression)
                chord_name = chord_progression[chord_idx]
                chord_notes = chord_tones[chord_name]

                # Create waltz rhythm pattern (strong-weak-weak)
                for j in range(3):
                    if j == 0:  # Strong beat
                        note_idx = 0
                    else:  # Weak beats
                        note_idx = (measure_num + j) % len(chord_notes)

                    note_name = chord_notes[note_idx]
                    n = note.Note(note_name, quarterLength=1.0)
                    measure.append(n)

                waltz.append(measure)

            self.current_score = waltz

            # Generate sheet music image using matplotlib
            self.create_sheet_music_image()

        except Exception as e:
            self.details_text.insert(tk.END, f"   ❌ Sheet music error: {e}\n")
            self.show_sheet_music_error(str(e))

    def create_sheet_music_image(self):
        """Create a visual representation of the sheet music"""
        try:
            # Save to temporary files
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.midi_file = f"mozart_waltz_{timestamp}.mid"
            self.xml_file = f"mozart_waltz_{timestamp}.musicxml"

            self.current_score.write('midi', fp=self.midi_file)
            self.current_score.write('musicxml', fp=self.xml_file)

            # Create a simplified visual representation
            self.create_simplified_notation()

            self.details_text.insert(tk.END, f"   ♪ MIDI: {self.midi_file}\n")
            self.details_text.insert(tk.END, f"   ♪ XML: {self.xml_file}\n")
            self.details_text.insert(tk.END, f"   🎼 Sheet music displayed!\n")

        except Exception as e:
            self.details_text.insert(tk.END, f"   ⚠️ Notation error: {e}\n")
            self.show_simple_notation()

    def create_simplified_notation(self):
        """Create a simplified visual notation in the canvas"""
        self.sheet_canvas.delete("all")

        # Title
        self.sheet_canvas.create_text(275, 30, text="Mozart Dice Waltz - Generated Sheet Music",
                                     font=("Arial", 14, "bold"), fill="#2c3e50")

        # Staff lines
        staff_y = 100
        staff_spacing = 15
        staff_width = 500
        staff_left = 25

        # Draw staff lines (treble clef)
        for i in range(5):
            y = staff_y + (i * staff_spacing)
            self.sheet_canvas.create_line(staff_left, y, staff_left + staff_width, y,
                                         fill="black", width=1)

        # Treble clef (simplified)
        self.sheet_canvas.create_text(staff_left + 20, staff_y + 30, text="𝄞",
                                     font=("Arial", 30), fill="black")

        # Time signature
        self.sheet_canvas.create_text(staff_left + 50, staff_y + 15, text="3",
                                     font=("Arial", 16, "bold"), fill="black")
        self.sheet_canvas.create_text(staff_left + 50, staff_y + 45, text="4",
                                     font=("Arial", 16, "bold"), fill="black")

        # Draw measures with notes
        measure_width = 28
        start_x = staff_left + 80

        # Note positions on staff (simplified)
        note_positions = {
            'C4': staff_y + 75,   # Below staff
            'D4': staff_y + 67,   # Below staff
            'E4': staff_y + 60,   # On bottom line
            'F4': staff_y + 52,   # Between lines
            'G4': staff_y + 45,   # Second line
            'A4': staff_y + 37,   # Between lines
            'B4': staff_y + 30,   # Third line
            'C5': staff_y + 22,   # Between lines
            'D5': staff_y + 15,   # Fourth line
            'E5': staff_y + 7,    # Between lines
            'F5': staff_y + 0     # Top line
        }

        # Draw first 8 measures
        for measure_idx in range(min(16, len(self.current_waltz))):
            if measure_idx == 8:  # Start new staff for second half
                staff_y += 120
                for i in range(5):
                    y = staff_y + (i * staff_spacing)
                    self.sheet_canvas.create_line(staff_left, y, staff_left + staff_width, y,
                                                 fill="black", width=1)
                start_x = staff_left + 20

            measure_x = start_x + (measure_idx % 8) * measure_width * 3
            measure_num = self.current_waltz[measure_idx]

            # Draw measure line
            if measure_idx % 8 == 0 and measure_idx > 0:
                self.sheet_canvas.create_line(measure_x - 5, staff_y, measure_x - 5, staff_y + 60,
                                             fill="black", width=2)

            # Simplified note representation - show 3 notes per measure
            notes_in_measure = self.get_notes_for_measure(measure_num)

            for note_idx, note_name in enumerate(notes_in_measure):
                note_x = measure_x + (note_idx * 8) + 5
                note_y = note_positions.get(note_name, staff_y + 30)

                # Draw note head
                self.sheet_canvas.create_oval(note_x - 3, note_y - 2, note_x + 3, note_y + 2,
                                            fill="black", outline="black")

                # Draw stem
                stem_height = 20
                if note_y < staff_y + 30:  # Notes above middle line have stems down
                    self.sheet_canvas.create_line(note_x - 3, note_y, note_x - 3, note_y + stem_height,
                                                 fill="black", width=1)
                else:  # Notes below have stems up
                    self.sheet_canvas.create_line(note_x + 3, note_y, note_x + 3, note_y - stem_height,
                                                 fill="black", width=1)

        # Add measure numbers below
        y_pos = staff_y + 80
        for i in range(min(16, len(self.current_waltz))):
            if i < 8:
                x_pos = start_x + i * measure_width * 3 + 10
                measure_y = 100 + 80
            else:
                x_pos = start_x + (i - 8) * measure_width * 3 + 10
                measure_y = y_pos

            self.sheet_canvas.create_text(x_pos, measure_y,
                                         text=str(self.current_waltz[i]),
                                         font=("Arial", 8), fill="#666")

        # Legend
        legend_y = staff_y + 100
        self.sheet_canvas.create_text(275, legend_y,
                                     text=f"Waltz Sequence: {' - '.join(map(str, self.current_waltz))}",
                                     font=("Arial", 10), fill="#666")

        # Configure scroll region
        self.sheet_canvas.configure(scrollregion=self.sheet_canvas.bbox("all"))

    def get_notes_for_measure(self, measure_num):
        """Get the three notes for a given measure based on its number"""
        # Simple algorithm to convert measure numbers to notes
        major_scale = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

        base_idx = measure_num % len(major_scale)
        note1 = major_scale[base_idx]
        note2 = major_scale[(base_idx + 2) % len(major_scale)]  # Third
        note3 = major_scale[(base_idx + 4) % len(major_scale)]  # Fifth

        return [note1, note2, note3]

    def show_simple_notation(self):
        """Show a simple text-based notation if image generation fails"""
        self.sheet_canvas.delete("all")

        self.sheet_canvas.create_text(275, 50, text="🎼 Mozart Dice Waltz",
                                     font=("Arial", 16, "bold"), fill="#2c3e50")

        # Show measures as numbers
        y_start = 100
        for i, measure in enumerate(self.current_waltz):
            x = 50 + (i % 8) * 60
            y = y_start + (i // 8) * 100

            # Measure box
            self.sheet_canvas.create_rectangle(x-20, y-20, x+20, y+20,
                                             outline="black", fill="#e8f4f8")
            self.sheet_canvas.create_text(x, y-10, text=f"M{i+1}",
                                         font=("Arial", 8), fill="#666")
            self.sheet_canvas.create_text(x, y+5, text=str(measure),
                                         font=("Arial", 12, "bold"), fill="black")

        self.sheet_canvas.create_text(275, y_start + 150,
                                     text="Each number represents one of Mozart's\n176 pre-composed measures",
                                     font=("Arial", 10), fill="#666", justify=tk.CENTER)

    def show_no_music21_message(self):
        """Show message when music21 is not available"""
        self.sheet_canvas.delete("all")
        self.sheet_canvas.create_text(275, 350,
                                     text="🎼\n\nmusic21 not available\nShowing measure sequence instead",
                                     font=("Arial", 14), fill="#e74c3c", justify=tk.CENTER)
        self.show_simple_notation()

    def show_sheet_music_error(self, error_msg):
        """Show error message in sheet music area"""
        self.sheet_canvas.delete("all")
        self.sheet_canvas.create_text(275, 350,
                                     text=f"🎼\n\nSheet music generation error:\n{error_msg}\n\nShowing simplified view",
                                     font=("Arial", 12), fill="#e67e22", justify=tk.CENTER)
        self.show_simple_notation()

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

            messagebox.showinfo("Files Saved", f"Files saved:\n• {filename}\n• {getattr(self, 'midi_file', 'No MIDI')}\n• {getattr(self, 'xml_file', 'No XML')}")
            self.status_var.set(f"Files saved!")

        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save files: {e}")

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🎼 Starting Mozart Dice Waltz GUI with Sheet Music Display...")

    app = MozartDiceGUIWithSheetMusic()
    app.run()

if __name__ == "__main__":
    main()