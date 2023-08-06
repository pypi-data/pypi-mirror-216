import openai
import os
import json

import tkinter as tk
from tkinter import ttk, filedialog, Text, Label, Scrollbar, HORIZONTAL, messagebox, IntVar
from Polly import Polly




# Set your OpenAI API key
openai.api_key = os.getenv("OPENAIKEY")

# Initialize conversation
conversation = []

# Function to handle conversation
def handle_conversation():
    user_input = input_box.get('1.0', tk.END).strip()  # Get text from input_box
    input_box.delete('1.0', tk.END)  # Clear input_box
    conversation_text.insert(tk.END, f"User: {user_input}\n")

    max_tokens_value = token_slider.get()
    temperature_value = temp_slider.get()

    conversation.append({"role": "user", "content": user_input})

    try:
        # Make API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=conversation,
            max_tokens=max_tokens_value,
            temperature=temperature_value
        )

        reply = response['choices'][0]['message']['content']

        conversation_text.insert(tk.END, f"Assistant: {reply}\n")

        # Check if the checkbox is checked
        if polly_check.get():
            synthesizer = Polly(reply)
            synthesizer.start()

        conversation.append({"role": "assistant", "content": reply})

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to save the conversation
def save_conversation():
    filename = filedialog.asksaveasfilename(defaultextension=".json")
    if filename:
        with open(filename, 'w') as f:
            json.dump(conversation, f)

# Function to load the conversation
def load_conversation():
    filename = filedialog.askopenfilename(defaultextension=".json")
    if filename:
        with open(filename, 'r') as f:
            global conversation
            conversation = json.load(f)
            for message in conversation:
                conversation_text.insert(tk.END, f"{message['role'].capitalize()}: {message['content']}\n")

root = tk.Tk()
root.title('Chatbot')
root.geometry('800x600')

# Create main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Configure the grid to expand
main_frame.grid_columnconfigure(0, weight=1)  # Allows column to expand
main_frame.grid_rowconfigure(0, weight=5)  # Allows row to expand
main_frame.grid_rowconfigure(1, weight=1)  # Allows row to expand

# Create scrollbar
scrollbar = Scrollbar(main_frame)
scrollbar.grid(row=0, column=1, sticky='ns')

# Create text widget for conversation
conversation_text = Text(main_frame, yscrollcommand=scrollbar.set)
conversation_text.grid(row=0, column=0, sticky='nsew')  # Fills the entire grid cell

# Connect scrollbar to conversation_text
scrollbar.config(command=conversation_text.yview)

# Create a label for the input box
input_label = Label(main_frame, text="Your input:")
input_label.grid(row=1, column=0, sticky='w')

# Create text widget for input
input_box = Text(main_frame, height=5)
input_box.grid(row=2, column=0, sticky='nsew')  # Fills the entire grid cell

# Create container for the buttons and sliders
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=3, column=0, sticky='ew')

# Create widgets inside button_frame, stacked horizontally
load_button = ttk.Button(button_frame, text="Load Conversation",command=load_conversation)
load_button.grid(row=0, column=0)

save_button = ttk.Button(button_frame, text="Save Conversation",command=save_conversation)
save_button.grid(row=0, column=1)

token_slider = tk.Scale(button_frame, from_=1, to=500, orient=tk.HORIZONTAL, label="Max Tokens")
token_slider.set(50)
token_slider.grid(row=0, column=2)

temp_slider = tk.Scale(button_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Temperature")
temp_slider.set(0.7)
temp_slider.grid(row=0, column=3)

# Add a checkbox for Polly audio output
polly_check = IntVar()
polly_checkbox = tk.Checkbutton(button_frame, text="Use Polly Audio", variable=polly_check)
polly_checkbox.grid(row=0, column=4)

send_button = tk.Button(root, text="Send", command=handle_conversation)
send_button.pack()

root.mainloop()
