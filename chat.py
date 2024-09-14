import os
import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai



genai.configure(api_key="add your own api key from gemini")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
except Exception as e:
    raise SystemExit(f"Failed to initialize the model: {e}")

chat_session = model.start_chat(history=[])

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generative AI Chatbot")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, width=80)
        self.entry.pack(padx=10, pady=(0, 10), side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0, 10), side=tk.RIGHT)

    def send_message(self, event=None):
        user_input = self.entry.get()
        if not user_input.strip():
            return

        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, f"You: {user_input}\n")
        self.text_area.config(state='disabled')
        self.entry.delete(0, tk.END)

        try:
            response = chat_session.send_message(user_input)
            ai_response = response.text.strip()
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"AI: {ai_response}\n")
            self.text_area.config(state='disabled')
            self.text_area.yview(tk.END)
        except Exception as e:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"Error: {e}\n")
            self.text_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

