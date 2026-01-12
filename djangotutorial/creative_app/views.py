# creative_app/ai_model.py
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# A tiny Singleton class to hold our Creative Model
class MoodAI:
    def __init__(self):
        # 1. Create a tiny dataset of "Moods" -> "RGB Colors"
        texts = [
            "angry furious mad fire",      # Red
            "happy joy sunny bright",      # Yellow
            "sad rain depressed blue",     # Blue
            "nature grass peace calm",     # Green
            "love passion heart",          # Pink
            "dark night fear horror"       # Black/Purple
        ]
        # Normalize RGB to 0-1
        colors = np.array([
            [1.0, 0.0, 0.0], # Red
            [1.0, 1.0, 0.0], # Yellow
            [0.0, 0.0, 1.0], # Blue
            [0.0, 1.0, 0.0], # Green
            [1.0, 0.0, 1.0], # Pink
            [0.2, 0.0, 0.4]  # Dark Purple
        ])

        # 2. Tokenize
        self.tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
        self.tokenizer.fit_on_texts(texts)
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded = pad_sequences(sequences, maxlen=5, padding='post')

        # 3. Build a simple LSTM Regression Model
        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(100, 8, input_length=5),
            tf.keras.layers.LSTM(16),
            tf.keras.layers.Dense(3, activation='sigmoid') # Outputs R, G, B (0-1)
        ])
        
        self.model.compile(optimizer='adam', loss='mse')
        # Train instantly on startup (very fast for this tiny data)
        self.model.fit(padded, colors, epochs=50, verbose=0)

    def predict_color(self, text):
        seq = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=5, padding='post')
        rgb = self.model.predict(padded)[0]
        # Convert back to 0-255
        return tuple((rgb * 255).astype(int))

# Initialize once
mood_ai = MoodAI()