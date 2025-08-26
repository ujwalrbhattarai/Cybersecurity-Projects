import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image
import wave
import os

class ImageSoundConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image <-> Sound Converter")
        self.root.geometry("400x180")

        self.label = tk.Label(root, text="Choose an option:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.btn_img_to_sound = tk.Button(root, text="Convert Image to Sound", width=25, command=self.image_to_sound)
        self.btn_img_to_sound.pack(pady=5)

        self.btn_sound_to_img = tk.Button(root, text="Convert Sound to Image", width=25, command=self.sound_to_image)
        self.btn_sound_to_img.pack(pady=5)

    def image_to_sound(self):
        image_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
        )
        if not image_path:
            return
        try:
            img = Image.open(image_path).convert('L')  # Grayscale
            data = np.array(img)
            height, width = data.shape
            norm_data = (data / 255.0) * 2 - 1
            audio_data = (norm_data.flatten() * 32767).astype(np.int16)

            # Ask user where to save audio file
            output_wav_path = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav")],
                title="Save Audio File As"
            )
            if not output_wav_path:
                return  # User cancelled

            with wave.open(output_wav_path, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(44100)
                wf.writeframes(audio_data.tobytes())

            # Save metadata file next to the chosen audio file
            meta_path = output_wav_path.rsplit('.', 1)[0] + "_meta.txt"
            with open(meta_path, 'w') as f:
                f.write(f"{width},{height}")

            messagebox.showinfo("Success", f"Audio saved as {output_wav_path}\nMetadata saved as {meta_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image to sound:\n{e}")

    def sound_to_image(self):
        wav_path = filedialog.askopenfilename(
            title="Select WAV File",
            filetypes=[("WAV files", "*.wav")]
        )
        if not wav_path:
            return
        meta_path = filedialog.askopenfilename(
            title="Select Meta File",
            filetypes=[("Text files", "*.txt")]
        )
        if not meta_path:
            return
        try:
            with open(meta_path, 'r') as f:
                dims = f.read().strip().split(',')
                width, height = int(dims[0]), int(dims[1])

            with wave.open(wav_path, 'r') as wf:
                frames = wf.readframes(wf.getnframes())
                audio_data = np.frombuffer(frames, dtype=np.int16)

            img_data = ((audio_data.astype(np.float32) / 32767.0) + 1) / 2 * 255
            img_data = img_data.astype(np.uint8)
            img_data = img_data[:width*height]
            img_data = img_data.reshape((height, width))
            img = Image.fromarray(img_data, mode='L')

            # Ask user where to save the retrieved image file
            output_image_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png")],
                title="Save Retrieved Image As"
            )
            if not output_image_path:
                return  # User cancelled

            img.save(output_image_path)
            messagebox.showinfo("Success", f"Image saved as {output_image_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert sound to image:\n{e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageSoundConverterGUI(root)
    root.mainloop()
