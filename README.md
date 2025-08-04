# 🎧 Multi-Audio Importer — Blender Add-on

**Easily import all audio tracks from multi-track video files into Blender's Video Sequence Editor (VSE).**

---

## 🔧 Features

- Detects and lists all audio tracks in a video using `ffprobe`.
- Lets you choose which tracks to import.
- Automatically imports them into the VSE.
- Works with `.mkv`, `.mp4`, and other container formats.

---

## 🛠 Requirements

- **Blender** (version 3.0+ recommended)
- [**FFmpeg**](https://ffmpeg.org/download.html) installed and added to your system’s **PATH**
-  this is the toturial video : https://www.youtube.com/watch?v=JR36oH35Fgg&ab_channel=Koolac
WARNING : make sure complete the video and restart your PC


---

## 📥 Installation Instructions

### 1. ✅ Install FFmpeg (if not already installed)

Download FFmpeg from:  
👉 [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Extract it (e.g., to `C:\ffmpeg`), and then:

**Add `ffmpeg/bin` to your system PATH:**

- Press `Win + R`, type `sysdm.cpl`, press Enter.
- Go to **Advanced** tab → Click **Environment Variables**.
- Under **System Variables**, select `Path` → click **Edit**.
- Click **New** → Paste the full path to the `bin` folder.  
  Example: `C:\ffmpeg\bin`
- Click **OK** to save and restart your PC.

### 2. 📦 Install the Add-on in Blender

1. Download the Python file:  
   `multi_audio_importer.py`
   
2. Open Blender → go to **Edit > Preferences > Add-ons**

3. Click **Install...** and choose the `.py` file.

4. Enable the add-on by checking the box next to **Multi Audio Importer**.

---

## 🎬 How to Use

1. Open the **Video Editing workspace** in Blender.

2. In the **Side Panel** (press `N` if it's hidden), go to the **"Multi Audio Import"** tab.

3. Click **"Scan Audio Tracks"** and select your video file.

4. You'll see a list of audio tracks detected in the video.

5. Select the ones you want, then click **"Import Selected Tracks"**.

---

## ❓ Troubleshooting

- **"Error running ffprobe: [WinError 2]"**  
  → Make sure `ffprobe` is installed and its folder is added to your system **PATH**.

- **No audio tracks found?**  
  → Try with a known multi-track video like `.mkv` with multiple audio languages.



## Surround UI for Sound Strips
https://github.com/tin2tin/Surround_UI_for_Sound_Strips

## Files for Testing

Test files can be found here: https://drive.google.com/drive/folders/1JxmeedtAtgmoafXv9rroiDOS2vEX7N4b
