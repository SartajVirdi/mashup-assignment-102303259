# Mashup Generator

## Project Overview
This project implements a "Mashup" generator that downloads songs of a specified singer from YouTube, cuts them, and merges them into a single audio file. It includes both a **Command Line Interface (CLI)** and a **Web Interface**.

## Features
1. **Download:** Automatically searches and downloads `N` videos of a singer.
2. **Convert:** Extracts audio (MP3) from videos.
3. **Cut:** Trims the first `Y` seconds of each audio.
4. **Merge:** Joins parts into a single output file.
5. **Email:** (Web Service) Zips the result and emails it to the user.

## Program 1: Command Line Usage
**File:** `102303259.py`

### How to Run
```bash
python 102303259.py "Arijit Singh" 20 20 output.mp3
```
