import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import colorsys

class MoodAI:
    def __init__(self):
        # 1. Training Data: Stronger associations
        # We repeat the keywords to ensure they stick
        data = [
            ("angry furious mad fire blood burn kill", [1.0, 0.0, 0.0]),       # Red
            ("happy joy sunny bright light smile fun", [1.0, 1.0, 0.0]),       # Yellow
            ("sad rain depressed tears ocean blue cry", [0.0, 0.0, 1.0]),      # Pure Blue
            ("nature grass peace forest calm tree growth", [0.0, 1.0, 0.0]),   # Pure Green
            ("love passion heart sweet kiss romance", [1.0, 0.0, 1.0]),        # Magenta
            ("night fear horror death dark shadow", [0.2, 0.0, 0.3]),          # Dark Violet
            ("energy power electric shock thunder spark", [0.0, 1.0, 1.0]),    # Cyan
            ("orange citrus fruit sunset warm autumn", [1.0, 0.5, 0.0]),       # Orange
            ("snow cold freeze winter white cloud ice", [0.9, 0.9, 0.9]),      # White/Grey
        ]
        
        texts = [item[0] for item in data]
        colors = np.array([item[1] for item in data])

        # 2. Tokenize
        self.tokenizer = Tokenizer(num_words=200, oov_token="<OOV>")
        self.tokenizer.fit_on_texts(texts)
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded = pad_sequences(sequences, maxlen=10, padding='post')

        # 3. Improved Model Architecture
        self.model = tf.keras.Sequential([
            # mask_zero=True is CRITICAL. It ignores the 0 padding.
            # Without this, "angry" (1 word) + 9 zeros = diluted signal (Pink)
            # With this, "angry" = 100% Red signal.
            tf.keras.layers.Embedding(200, 24, input_length=10, mask_zero=True),
            
            tf.keras.layers.GlobalAveragePooling1D(),
            
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(3, activation='sigmoid') 
        ])
        
        # Use a higher learning rate to force the model to memorize these colors quickly
        opt = tf.keras.optimizers.Adam(learning_rate=0.01)
        self.model.compile(optimizer=opt, loss='mse')
        
        # Train
        self.model.fit(padded, colors, epochs=150, verbose=0)

    def predict_color(self, text):
        seq = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=10, padding='post')
        
        # Get raw RGB prediction (0.0 - 1.0)
        rgb = self.model.predict(padded)[0]
        r, g, b = rgb
        
        # --- FIX: Color Boosting via HSV ---
        # Convert RGB to HSV (Hue, Saturation, Value)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        # 1. Boost Saturation: If it's not white/black, force it to be vivid
        # If saturation is low (pastel), bump it up.
        if s > 0.1: 
            s = max(s, 0.7) # Minimum saturation 70%
            
        # 2. Boost Brightness (Value): Ensure it's not muddy
        v = max(v, 0.8) # Minimum brightness 80%

        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
        # Clip to ensure valid range
        r, g, b = np.clip([r, g, b], 0.0, 1.0)

        return tuple((np.array([r, g, b]) * 255).astype(int))

mood_ai = MoodAI()