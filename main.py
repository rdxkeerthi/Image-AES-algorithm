import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def encrypt_image(image_path, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    with open(image_path, 'rb') as file:
        image_data = file.read()
    encrypted_data = cipher.encrypt(image_data)
    with open('encrypted_image.png', 'wb') as file:
        file.write(iv + encrypted_data)

def decrypt_image(image_path, key):
    with open(image_path, 'rb') as file:
        iv = file.read(16)
        encrypted_data = file.read()
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    with open('decrypted_image.png', 'wb') as file:
        file.write(decrypted_data)

def browse_image():
    path = filedialog.askopenfilename(filetypes=[("Image File",'.jpg .jpeg .png')])
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, path)

def encrypt():
    image_path = image_path_entry.get()
    if not os.path.exists(image_path):
        result_label.config(text="Image file not found!")
        return
    key = key_entry.get().encode('utf-8')
    if len(key) != 16:
        result_label.config(text="Key should be 16 bytes long!")
        return
    encrypt_image(image_path, key)
    result_label.config(text="Image Encrypted Successfully!")

def decrypt():
    image_path = image_path_entry.get()
    if not os.path.exists(image_path):
        result_label.config(text="Image file not found!")
        return
    key = key_entry.get().encode('utf-8')
    if len(key) != 16:
        result_label.config(text="Key should be 16 bytes long!")
        return
    decrypt_image(image_path, key)
    result_label.config(text="Image Decrypted Successfully!")

root = tk.Tk()
root.title("Image Encryption and Decryption")
author = "IPsq Keerthivasan"

image_path_label = tk.Label(root, text="Image Path:")
image_path_label.grid(row=0, column=0)
image_path_entry = tk.Entry(root, width=50)
image_path_entry.grid(row=0, column=1)
browse_button = tk.Button(root, text="Browse", command=browse_image)
browse_button.grid(row=0, column=2)

key_label = tk.Label(root, text="Key:")
key_label.grid(row=1, column=0)
key_entry = tk.Entry(root, width=50)
key_entry.grid(row=1, column=1)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.grid(row=2, column=0)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.grid(row=2, column=1)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2)

root.mainloop()