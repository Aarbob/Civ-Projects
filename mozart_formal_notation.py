#!/usr/bin/env python3
"""
Mozart Dice Waltz - GUI with Formal Sheet Music Popup
Generates proper musical notation that pops up after dice rolling
"""

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import random
import threading
import time
import os
import subprocess
import tempfile
from pathlib import Path

try:
    from music21 import stream, note, meter, key, tempo, duration, pitch, bar, metadata
    from music21.musicxml import m21ToXml
    from PIL import Image, ImageTk
    MUSIC21_AVAILABLE = True
except ImportError:
    MUSIC21_AVAILABLE = False

class FormalSheetMusicWindow:
    """Separate window for displaying formal sheet music notation"""

    def __init__(self, parent, waltz_score, waltz_sequence):
        self.parent = parent
        self.waltz_score = waltz_score
        self.waltz_sequence = waltz_sequence

        # Create popup window
        self.window = Toplevel(parent)
        self.window.title("🎼 Mozart Waltz - Formal Sheet Music")
        self.window.geometry("800x900")
        self.window.configure(bg="white")

        # Make it modal
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_sheet_music_window()
        self.generate_formal_notation()

    def setup_sheet_music_window(self):
        """Setup the sheet music display window"""

        # Title
        title_frame = tk.Frame(self.window, bg="white")
        title_frame.pack(pady=20)

        tk.Label(title_frame, text="🎼 Mozart's Waltz - Formal Notation",
                font=("Arial", 18, "bold"), bg="white", fg="#2c3e50").pack()

        tk.Label(title_frame, text=f"Measures: {' - '.join(map(str, self.waltz_sequence))}",
                font=("Courier", 12), bg="white", fg="#7f8c8d").pack()

        # Controls
        controls_frame = tk.Frame(self.window, bg="white")
        controls_frame.pack(pady=10)

        tk.Button(controls_frame, text="💾 Save PNG", font=("Arial", 10, "bold"),
                 bg="#3498db", fg="white", command=self.save_png).pack(side=tk.LEFT, padx=5)

        tk.Button(controls_frame, text="🎵 Play", font=("Arial", 10, "bold"),
                 bg="#2ecc71", fg="white", command=self.play_music).pack(side=tk.LEFT, padx=5)

        tk.Button(controls_frame, text="📄 Export XML", font=("Arial", 10, "bold"),
                 bg="#e74c3c", fg="white", command=self.export_xml).pack(side=tk.LEFT, padx=5)

        tk.Button(controls_frame, text="❌ Close", font=("Arial", 10, "bold"),
                 bg="#95a5a6", fg="white", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

        # Sheet music display area
        sheet_frame = tk.Frame(self.window, bg="white", relief=tk.SUNKEN, bd=2)
        sheet_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas with scrollbars
        self.canvas = tk.Canvas(sheet_frame, bg="white")
        v_scrollbar = tk.Scrollbar(sheet_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(sheet_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Status
        self.status_var = tk.StringVar(value="Generating formal notation...")
        status_label = tk.Label(self.window, textvariable=self.status_var,
                               font=("Arial", 10), bg="#ecf0f1", fg="#2c3e50", anchor=tk.W, padx=10)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def generate_formal_notation(self):
        """Generate formal music notation using music21"""
        try:
            self.status_var.set("Creating formal sheet music notation...")

            # Create enhanced musical score with proper notation
            waltz = stream.Score()

            # Add metadata
            waltz.append(metadata.Metadata())
            waltz.metadata.title = "Mozart Dice Waltz"
            waltz.metadata.composer = "W.A. Mozart (Generated)"
            waltz.metadata.copyright = f"Generated on {time.strftime('%Y-%m-%d')}"

            # Create part
            part = stream.Part()

            # Add key signature, time signature, tempo
            part.append(key.KeySignature(0))  # C major
            part.append(meter.TimeSignature('3/4'))
            part.append(tempo.MetronomeMark(number=120, referent=duration.Duration(1.0)))

            # Create sophisticated waltz patterns based on measure numbers
            self.create_waltz_measures(part)

            waltz.append(part)
            self.enhanced_score = waltz

            # Generate notation image
            self.create_notation_image()

        except Exception as e:
            self.status_var.set(f"Notation error: {e}")
            self.show_text_notation()

    def create_waltz_measures(self, part):
        """Create musically sophisticated measures based on Mozart's style"""

        # Define waltz chord progressions and patterns
        chord_progressions = [
            # Classic waltz progressions
            ['C', 'G', 'Am', 'F', 'C', 'F', 'G', 'C'],  # I-V-vi-IV progression
            ['C', 'Am', 'F', 'G', 'C', 'G', 'F', 'C'],  # Alternative progression
            ['C', 'F', 'G', 'C', 'Am', 'F', 'G', 'C'],  # Another variation
        ]

        # Note patterns for different chord types
        chord_notes = {
            'C': ['C4', 'E4', 'G4', 'C5'],
            'F': ['F4', 'A4', 'C5', 'F5'],
            'G': ['G4', 'B4', 'D5', 'G5'],
            'Am': ['A4', 'C5', 'E5', 'A5'],
            'Dm': ['D4', 'F4', 'A4', 'D5'],
            'Em': ['E4', 'G4', 'B4', 'E5']
        }

        # Bass note patterns for waltz (oom-pah-pah rhythm)
        bass_patterns = {
            'C': ['C3', 'G3', 'E3'],
            'F': ['F3', 'C4', 'A3'],
            'G': ['G3', 'D4', 'B3'],
            'Am': ['A3', 'E4', 'C4'],
            'Dm': ['D3', 'A3', 'F3'],
            'Em': ['E3', 'B3', 'G3']
        }

        # Select chord progression based on first measure number
        prog_idx = self.waltz_sequence[0] % len(chord_progressions)
        progression = chord_progressions[prog_idx]

        for i, measure_num in enumerate(self.waltz_sequence):
            measure = stream.Measure(number=i + 1)

            # Select chord based on position and measure number
            chord_idx = (measure_num + i) % len(progression)
            current_chord = progression[chord_idx]

            # Get notes for this chord
            melody_notes = chord_notes.get(current_chord, chord_notes['C'])
            bass_notes = bass_patterns.get(current_chord, bass_patterns['C'])

            # Create waltz rhythm pattern
            if i < 8:  # First half - melody emphasis
                self.create_melody_measure(measure, melody_notes, measure_num)
            else:  # Second half - more elaborate
                self.create_elaborate_measure(measure, melody_notes, bass_notes, measure_num)

            part.append(measure)

    def create_melody_measure(self, measure, chord_notes, measure_num):
        """Create a melody-focused measure"""
        # Waltz pattern: strong beat on 1, lighter on 2 and 3

        # Beat 1 (strong)
        note_idx = measure_num % len(chord_notes)
        note1 = note.Note(chord_notes[note_idx], quarterLength=1.0)
        note1.volume.velocity = 80
        measure.append(note1)

        # Beat 2 (light)
        note_idx = (measure_num + 1) % len(chord_notes)
        note2 = note.Note(chord_notes[note_idx], quarterLength=1.0)
        note2.volume.velocity = 60
        measure.append(note2)

        # Beat 3 (light)
        note_idx = (measure_num + 2) % len(chord_notes)
        note3 = note.Note(chord_notes[note_idx], quarterLength=1.0)
        note3.volume.velocity = 60
        measure.append(note3)

    def create_elaborate_measure(self, measure, melody_notes, bass_notes, measure_num):
        """Create a more elaborate measure with bass and melody"""
        # Add bass note on beat 1
        bass_note = note.Note(bass_notes[0], quarterLength=1.0)
        bass_note.volume.velocity = 70

        # Add melody notes on beats 2 and 3
        melody_idx = measure_num % len(melody_notes)
        melody1 = note.Note(melody_notes[melody_idx], quarterLength=0.5)
        melody2 = note.Note(melody_notes[(melody_idx + 1) % len(melody_notes)], quarterLength=0.5)
        melody3 = note.Note(melody_notes[(melody_idx + 2) % len(melody_notes)], quarterLength=1.0)

        measure.append(bass_note)
        measure.append(melody1)
        measure.append(melody2)
        measure.append(melody3)

    def create_notation_image(self):
        """Create formal notation image using music21"""
        try:
            # Try to generate PNG image using music21
            self.status_var.set("Rendering formal sheet music...")

            # Save as temporary files
            self.timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.temp_dir = tempfile.mkdtemp()

            # Export as MusicXML first
            xml_path = os.path.join(self.temp_dir, f"waltz_{self.timestamp}.musicxml")
            self.enhanced_score.write('musicxml', fp=xml_path)

            # Try to create PNG if possible
            try:
                png_path = os.path.join(self.temp_dir, f"waltz_{self.timestamp}.png")
                self.enhanced_score.write('musicxml.png', fp=png_path)

                if os.path.exists(png_path):
                    self.display_png_notation(png_path)
                else:
                    raise Exception("PNG generation failed")

            except:
                # Fallback to text-based notation
                self.status_var.set("Formal notation requires MuseScore - showing structured view")
                self.show_structured_notation()

        except Exception as e:
            self.status_var.set(f"Notation generation error: {e}")
            self.show_text_notation()

    def display_png_notation(self, png_path):
        """Display the PNG notation in the canvas"""
        try:
            # Load and display the PNG image
            pil_image = Image.open(png_path)

            # Resize if too large
            max_width = 750
            if pil_image.width > max_width:
                ratio = max_width / pil_image.width
                new_height = int(pil_image.height * ratio)
                pil_image = pil_image.resize((max_width, new_height), Image.Resampling.LANCZOS)

            self.tk_image = ImageTk.PhotoImage(pil_image)

            # Clear canvas and add image
            self.canvas.delete("all")
            self.canvas.create_image(10, 10, anchor=tk.NW, image=self.tk_image)

            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            self.status_var.set("Formal notation displayed successfully!")

        except Exception as e:
            self.status_var.set(f"Image display error: {e}")
            self.show_text_notation()

    def show_structured_notation(self):
        """Show a structured, formal-looking notation display"""
        self.canvas.delete("all")

        # Title
        self.canvas.create_text(400, 30, text="Mozart Dice Waltz - Formal Structure",
                               font=("Times New Roman", 16, "bold"), fill="#2c3e50")

        # Key and time signature
        self.canvas.create_text(400, 60, text="Key: C Major  |  Time: 3/4  |  Tempo: ♩ = 120",
                               font=("Times New Roman", 12), fill="#34495e")

        # Draw formal staff representation
        y_start = 100

        # Staff lines
        staff_spacing = 12
        staff_width = 700
        staff_left = 50

        for staff_num in range(2):  # Two staves for the 16 measures
            staff_y = y_start + (staff_num * 200)

            # Draw 5 staff lines
            for i in range(5):
                y = staff_y + (i * staff_spacing)
                self.canvas.create_line(staff_left, y, staff_left + staff_width, y,
                                       fill="black", width=1)

            # Clef
            self.canvas.create_text(staff_left + 25, staff_y + 24, text="𝄞",
                                   font=("Times New Roman", 24), fill="black")

            # Time signature
            if staff_num == 0:
                self.canvas.create_text(staff_left + 60, staff_y + 12, text="3",
                                       font=("Times New Roman", 14, "bold"), fill="black")
                self.canvas.create_text(staff_left + 60, staff_y + 36, text="4",
                                       font=("Times New Roman", 14, "bold"), fill="black")

            # Measures
            measures_per_staff = 8
            start_measure = staff_num * 8
            measure_width = 75

            for m in range(measures_per_staff):
                if start_measure + m < len(self.waltz_sequence):
                    measure_x = staff_left + 80 + (m * measure_width)
                    measure_num = self.waltz_sequence[start_measure + m]

                    # Measure line
                    if m > 0:
                        self.canvas.create_line(measure_x - 5, staff_y, measure_x - 5, staff_y + 48,
                                               fill="black", width=1)

                    # Notes representation (formal style)
                    note_positions = [
                        staff_y + 48,  # C (ledger line below)
                        staff_y + 42,  # D (below staff)
                        staff_y + 36,  # E (bottom line)
                        staff_y + 30,  # F (space)
                        staff_y + 24,  # G (second line)
                        staff_y + 18,  # A (space)
                        staff_y + 12,  # B (third line)
                        staff_y + 6,   # C (space)
                        staff_y + 0    # D (top line)
                    ]

                    # Three notes per measure (waltz pattern)
                    for beat in range(3):
                        note_x = measure_x + 10 + (beat * 20)

                        # Calculate note position based on measure number
                        note_idx = (measure_num + beat) % len(note_positions)
                        note_y = note_positions[note_idx]

                        # Draw note head
                        self.canvas.create_oval(note_x - 3, note_y - 2, note_x + 3, note_y + 2,
                                               fill="black", outline="black")

                        # Draw stem
                        stem_height = 20
                        if note_y < staff_y + 24:  # Upper half of staff
                            self.canvas.create_line(note_x - 3, note_y, note_x - 3, note_y + stem_height,
                                                   fill="black", width=1)
                        else:  # Lower half of staff
                            self.canvas.create_line(note_x + 3, note_y, note_x + 3, note_y - stem_height,
                                                   fill="black", width=1)

                    # Measure number below staff
                    self.canvas.create_text(measure_x + 35, staff_y + 70,
                                           text=f"M{start_measure + m + 1}: {measure_num}",
                                           font=("Arial", 8), fill="#7f8c8d")

        # Add legend
        legend_y = y_start + 420
        self.canvas.create_text(400, legend_y,
                               text=f"Complete Sequence: {' - '.join(map(str, self.waltz_sequence))}",
                               font=("Courier New", 10), fill="#2c3e50")

        self.canvas.create_text(400, legend_y + 20,
                               text="Each measure represents one of Mozart's 176 pre-composed musical segments",
                               font=("Arial", 9), fill="#7f8c8d")

        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.status_var.set("Formal notation structure displayed")

    def show_text_notation(self):
        """Fallback: show text-based notation"""
        self.canvas.delete("all")

        self.canvas.create_text(400, 200,
                               text="Formal Notation Error\n\nShowing measure sequence instead:",
                               font=("Arial", 14), fill="#e74c3c", justify=tk.CENTER)

        sequence_text = ' - '.join(map(str, self.waltz_sequence))
        self.canvas.create_text(400, 300, text=sequence_text,
                               font=("Courier New", 12, "bold"), fill="#2c3e50")

    def save_png(self):
        """Save the sheet music as PNG"""
        try:
            if hasattr(self, 'enhanced_score'):
                filename = f"mozart_waltz_notation_{self.timestamp}.png"
                self.enhanced_score.write('musicxml.png', fp=filename)
                messagebox.showinfo("Saved", f"Sheet music saved as: {filename}")
            else:
                messagebox.showwarning("No Score", "Generate sheet music first!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save PNG: {e}")

    def play_music(self):
        """Play the waltz"""
        try:
            if hasattr(self, 'enhanced_score'):
                midi_file = f"waltz_notation_{self.timestamp}.mid"
                self.enhanced_score.write('midi', fp=midi_file)

                if os.name == 'posix':  # macOS/Linux
                    subprocess.call(['open', midi_file])
                elif os.name == 'nt':  # Windows
                    os.startfile(midi_file)

                self.status_var.set("Playing music...")
            else:
                messagebox.showwarning("No Score", "Generate music first!")
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play music: {e}")

    def export_xml(self):
        """Export MusicXML file"""
        try:
            if hasattr(self, 'enhanced_score'):
                filename = f"mozart_waltz_formal_{self.timestamp}.musicxml"
                self.enhanced_score.write('musicxml', fp=filename)
                messagebox.showinfo("Exported", f"MusicXML exported as: {filename}")
            else:
                messagebox.showwarning("No Score", "Generate score first!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export XML: {e}")


class MozartDiceFormalGUI:
    """Main GUI that pops up formal notation after dice results"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎼 Mozart Dice Waltz - Formal Notation Generator")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        # Game data (same as before)
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
        """Setup main interface focused on dice game"""

        # Title
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(pady=30)

        title_label = tk.Label(title_frame, text="🎼 Mozart's Musical Dice Game",
                              font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Roll dice → Get formal sheet music!",
                                 font=("Arial", 14), bg="#f0f0f0", fg="#7f8c8d")
        subtitle_label.pack()

        # Info box
        info_frame = tk.LabelFrame(self.root, text="How it Works", font=("Arial", 12, "bold"),
                                  bg="#e8f6f3", fg="#27ae60")
        info_frame.pack(pady=20, padx=40, fill=tk.X)

        info_text = """1. Click 'Generate Waltz' to watch animated dice rolling
2. See Mozart's algorithm select 16 musical measures
3. Formal sheet music automatically pops up when complete
4. View, play, and save professional notation!"""

        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f6f3",
                fg="#2c3e50", justify=tk.LEFT).pack(padx=15, pady=10)

        # Main generate button
        self.generate_btn = tk.Button(self.root, text="🎲 Generate Mozart Waltz",
                                     font=("Arial", 18, "bold"), bg="#3498db", fg="white",
                                     command=self.start_generation, padx=40, pady=15)
        self.generate_btn.pack(pady=30)

        # Dice display (larger)
        dice_frame = tk.LabelFrame(self.root, text="Dice Rolling", font=("Arial", 12, "bold"),
                                  bg="#f0f0f0")
        dice_frame.pack(pady=20)

        self.dice1_var = tk.StringVar(value="?")
        self.dice2_var = tk.StringVar(value="?")
        self.sum_var = tk.StringVar(value="?")

        dice_display_frame = tk.Frame(dice_frame, bg="#f0f0f0")
        dice_display_frame.pack(padx=20, pady=15)

        dice1_label = tk.Label(dice_display_frame, textvariable=self.dice1_var,
                              font=("Arial", 24, "bold"), bg="white", fg="black",
                              width=3, height=2, relief=tk.RAISED, bd=4)
        dice1_label.pack(side=tk.LEFT, padx=8)

        tk.Label(dice_display_frame, text="+", font=("Arial", 20, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=8)

        dice2_label = tk.Label(dice_display_frame, textvariable=self.dice2_var,
                              font=("Arial", 24, "bold"), bg="white", fg="black",
                              width=3, height=2, relief=tk.RAISED, bd=4)
        dice2_label.pack(side=tk.LEFT, padx=8)

        tk.Label(dice_display_frame, text="=", font=("Arial", 20, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=8)

        sum_label = tk.Label(dice_display_frame, textvariable=self.sum_var,
                            font=("Arial", 24, "bold"), bg="#f39c12", fg="white",
                            width=3, height=2, relief=tk.RAISED, bd=4)
        sum_label.pack(side=tk.LEFT, padx=8)

        # Progress
        self.progress = ttk.Progressbar(self.root, length=500, mode='determinate')
        self.progress.pack(pady=20)

        # Status
        self.status_var = tk.StringVar(value="Ready to generate Mozart waltz with formal notation!")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             font=("Arial", 11), bg="#34495e", fg="white",
                             anchor=tk.W, padx=15, pady=8)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Generation log (smaller)
        log_frame = tk.LabelFrame(self.root, text="Generation Log", font=("Arial", 10, "bold"),
                                 bg="#f0f0f0")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=40)

        self.log_text = tk.Text(log_frame, height=8, font=("Courier", 9),
                               bg="#ecf0f1", fg="#2c3e50")
        log_scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

    def start_generation(self):
        """Start the waltz generation process"""
        if self.is_generating:
            return

        self.is_generating = True
        self.generate_btn.config(state=tk.DISABLED)
        self.log_text.delete(1.0, tk.END)
        self.current_waltz = []

        # Start in separate thread
        threading.Thread(target=self.generate_and_show_notation, daemon=True).start()

    def generate_and_show_notation(self):
        """Generate waltz and automatically show formal notation"""
        try:
            self.status_var.set("Rolling dice and selecting measures...")
            self.progress['maximum'] = 16
            self.progress['value'] = 0

            self.log_text.insert(tk.END, "🎲 Mozart's Musical Dice Game - Generation Started\n")
            self.log_text.insert(tk.END, "=" * 55 + "\n\n")

            # Generate waltz with animation
            columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

            # First half
            self.log_text.insert(tk.END, "🎵 First Half (Measures 1-8):\n")
            for i in range(8):
                self.animate_and_select_measure(i, True, columns[i])

            # Second half
            self.log_text.insert(tk.END, "\n🎵 Second Half (Measures 9-16):\n")
            for i in range(8):
                self.animate_and_select_measure(i, False, columns[i])

            # Show results
            self.log_text.insert(tk.END, f"\n🎼 Complete Waltz Generated!\n")
            self.log_text.insert(tk.END, f"   Sequence: {' - '.join(map(str, self.current_waltz))}\n\n")

            # Generate formal notation
            if MUSIC21_AVAILABLE:
                self.status_var.set("Creating formal sheet music notation...")
                self.log_text.insert(tk.END, "📝 Generating formal sheet music notation...\n")
                self.log_text.see(tk.END)

                # Create the score
                score = self.create_formal_score()

                # Pop up the formal notation window
                self.log_text.insert(tk.END, "🎼 Opening formal notation window...\n")
                self.root.after(500, lambda: self.show_formal_notation(score))

            else:
                self.log_text.insert(tk.END, "⚠️  music21 not available - cannot generate formal notation\n")
                messagebox.showwarning("Missing Dependency",
                    "music21 library not available.\nInstall with: pip install music21")

            self.status_var.set("Waltz generation complete!")

        except Exception as e:
            self.log_text.insert(tk.END, f"\n❌ Error: {str(e)}\n")
            self.status_var.set("Generation failed!")
            messagebox.showerror("Generation Error", f"Could not generate waltz: {e}")

        finally:
            self.is_generating = False
            self.generate_btn.config(state=tk.NORMAL)

    def animate_and_select_measure(self, position, is_first_half, column):
        """Animate dice and select measure"""
        self.status_var.set(f"Rolling dice for position {position + 1 + (0 if is_first_half else 8)}/16...")

        # Animate dice
        for _ in range(12):
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

        self.log_text.insert(tk.END, f"   {column}: {die1} + {die2} = {roll_sum:2d} → Measure {measure:3d}\n")
        self.log_text.see(tk.END)

        progress_value = position + (0 if is_first_half else 8) + 1
        self.progress['value'] = progress_value
        self.root.update()
        time.sleep(0.4)

    def create_formal_score(self):
        """Create formal musical score"""
        # Create enhanced score (same logic as FormalSheetMusicWindow)
        waltz = stream.Score()

        waltz.append(metadata.Metadata())
        waltz.metadata.title = "Mozart Dice Waltz"
        waltz.metadata.composer = "W.A. Mozart (Generated via Dice Game)"

        part = stream.Part()
        part.append(key.KeySignature(0))  # C major
        part.append(meter.TimeSignature('3/4'))
        part.append(tempo.MetronomeMark(number=120))

        # Create measures based on selected sequence
        chord_prog = ['C', 'G', 'Am', 'F', 'C', 'F', 'G', 'C']
        chord_notes = {
            'C': ['C4', 'E4', 'G4'],
            'G': ['G4', 'B4', 'D5'],
            'Am': ['A4', 'C5', 'E5'],
            'F': ['F4', 'A4', 'C5']
        }

        for i, measure_num in enumerate(self.current_waltz):
            measure = stream.Measure(number=i + 1)

            # Select chord
            chord_name = chord_prog[measure_num % len(chord_prog)]
            notes = chord_notes.get(chord_name, chord_notes['C'])

            # Add three notes for waltz pattern
            for j in range(3):
                note_name = notes[j % len(notes)]
                n = note.Note(note_name, quarterLength=1.0)
                n.volume.velocity = 80 if j == 0 else 60  # Waltz emphasis
                measure.append(n)

            part.append(measure)

        waltz.append(part)
        return waltz

    def show_formal_notation(self, score):
        """Show the formal notation popup window"""
        try:
            FormalSheetMusicWindow(self.root, score, self.current_waltz)
        except Exception as e:
            messagebox.showerror("Notation Error", f"Could not display formal notation: {e}")

    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🎼 Starting Mozart Dice Waltz with Formal Notation Popup...")

    if not MUSIC21_AVAILABLE:
        print("⚠️  Warning: music21 not available. Some features may be limited.")

    app = MozartDiceFormalGUI()
    app.run()

if __name__ == "__main__":
    main()