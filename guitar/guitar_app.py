import sounddevice as sd
import numpy as np
import librosa
from collections import deque

SR = 22050
DURATION = 0.8
SMOOTHING_WINDOW = 2 
history = deque(maxlen=SMOOTHING_WINDOW)

# --- MASIVNÍ KNIHOVNA AKORDŮ ---
# Indexy tónů: [C, C#, D, D#, E, F, F#, G, G#, A, A#, B]
CHORD_TEMPLATES = {
    # DUR
    'C dur': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'C# dur': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    'D dur': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'D# dur': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    'E dur': [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    'F dur': [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'F# dur': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    'G dur': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    'G# dur': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    'A dur': [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    'B dur (H)': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    'H dur': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    
    # MOLL
    'C moll': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    'D moll': [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    'E moll': [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'F moll': [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    'G moll': [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    'A moll': [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    'B moll (Hm)': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    
    # SEDMIČKY (7, maj7, m7)
    'C7': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'D7': [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'E7': [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    'G7': [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'A7': [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    'Dmaj7': [0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    'Amaj7': [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    
    # OSTATNÍ (Sus, Add)
    'Dsus4': [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    'Asus4': [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    'Cadd9': [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'Em9': [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
}

def identify_chord(audio):
    # Chromagram s vyšším rozlišením
    chroma = librosa.feature.chroma_cqt(y=audio, sr=SR, n_chroma=12, bins_per_octave=24)
    mean_chroma = np.mean(chroma, axis=1)
    
    # Posílení nejsilnějších tónů pro potlačení šumu
    mean_chroma = mean_chroma**2 
    norm = np.linalg.norm(mean_chroma)
    if norm < 0.01: return "Ticho", 0
    mean_chroma /= norm

    best_name = "???"
    max_sim = -1

    for name, template in CHORD_TEMPLATES.items():
        t = np.array(template) / np.linalg.norm(template)
        # Výpočet podobnosti
        similarity = np.dot(mean_chroma, t)
        if similarity > max_sim:
            max_sim = similarity
            best_name = name
            
    return best_name, max_sim

print("🚀 Aplikace připravena! Knihovna obsahuje 30+ akordů.")

try:
    while True:
        rec = sd.rec(int(DURATION * SR), samplerate=SR, channels=1)
        sd.wait()
        audio = rec.flatten()
        
        if np.max(np.abs(audio)) > 0.06:
            chord, score = identify_chord(audio)
            
            if score > 0.65:
                history.append(chord)
                if len(history) == SMOOTHING_WINDOW and len(set(history)) == 1:
                    print(f"🎸 Detekováno: {chord} (shoda {int(score*100)}%)")
except KeyboardInterrupt:
    print("\nVypínám...")