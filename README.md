# # Playlist Vibe Builder (Merge Sort Visualizer)
Playlist Vibe Builder (Problem 2): Given a list of songs with title, artist, energy score (0–100), and duration, the user selects a sort key (energy or duration) and the app re-orders the playlist from lowest to highest — animating every comparison and merge so the algorithm is easy to follow.



# Algorithm Name
Merge Sort
-chosen because of its stability. Songs with equal energy scores keep their original relative order, which feels natural for music curation

## Demo video/gif/screenshot of test
<img width="1916" height="994" alt="image" src="https://github.com/user-attachments/assets/19620263-0196-4cc0-86f4-0d73fa2a78b8" />




## Problem Breakdown & Computational Thinking

### Decomposition
- Take a list of songs as input
- Each song has a title and an energy value
- Split the list into smaller sublists
- Sort each sublist using Merge Sort
- Merge sorted lists back together

### Pattern Recognition
- The algorithm repeatedly divides the list into halves
- It compares elements from two lists and merges them in order

### Abstraction
- The app shows key comparisons and merges to the user
- It hides low-level recursion details to keep it simple

### Algorithmic thinking
Input → User enters playlist → Merge Sort processes data → Sorted playlist is displayed

<img width="684" height="790" alt="image" src="https://github.com/user-attachments/assets/81c98cc0-ace6-4d84-9ad6-aa3786fac068" />


## Steps to Run
# 1. Clone or download the project
https://github.com/BZETTI/playlist-sorter-app.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
python app.py

# 4. Open your browser at http://127.0.0.1:7860

## Hugging Face Link

https://huggingface.co/spaces/BZETTI/Playlist_Vibe_Sorter

Testing and Edge Cases

Tested the default 8 songs with both sort keys --> Pass
Tested 1 song --> Pass
Tested 2 songs --> Pass
Tested songs with equal energy --> Pass
Tested a playlist which was already sorted aswell as reverse sorted --> Pass
Tested Error Handling with seconds > 60 aswell as vibe > 100 --> Pass

## Author & AI Acknowledgment

Author: Muhammad Bilal Zahid 

AI Use- Claude (Anthropic) was used at Level 4 to help structure the project and write and review code. All algorithmic logic was understood, verified, and is explained by the author.
