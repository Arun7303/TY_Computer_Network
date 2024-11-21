import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk

# Function to connect to server and retrieve the webpage
def fetch_webpage():
    # Get the URL entered by the user
    url = url_entry.get().strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        display_error("URL must start with 'http://' or 'https://'.")
        return
    
    # Parse URL to get the host and path
    host, path = parse_url(url)
    if not host:
        display_error("Invalid URL format.")
        return

    # Disable button and show loading status
    fetch_button.config(state="disabled")
    status_label.config(text="Fetching webpage...", foreground="blue")
    
    # Create a TCP socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((host, 80))
            # Send HTTP GET request
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode())

            # Receive the response
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data

        # Decode response and separate headers and content
        response_text = response.decode("utf-8", errors="ignore")
        headers, _, body = response_text.partition("\r\n\r\n")

        # Update status, enable button, and display fetched content
        status_label.config(text="Webpage fetched successfully!", foreground="green")
        display_content(headers, body)
        
    except Exception as e:
        display_error(f"Error fetching webpage: {e}")
    
    finally:
        fetch_button.config(state="normal")

# Helper function to parse URL and extract host and path
def parse_url(url):
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    else:
        return None, None

    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"
    
    return host, path

# Display error message
def display_error(message):
    messagebox.showerror("Error", message)
    status_label.config(text="Failed to fetch webpage", foreground="red")
    details_text.config(state="normal")
    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, message)
    details_text.config(state="disabled")

# Display headers and content in the GUI
def display_content(headers, body):
    details_text.config(state="normal")
    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, headers)
    details_text.config(state="disabled")
    
    content_text.config(state="normal")
    content_text.delete("1.0", tk.END)
    content_text.insert(tk.END, body)
    content_text.config(state="disabled")

# Set up the GUI using tkinter
root = tk.Tk()
root.title("HTTP Web Client")
root.geometry("800x600")
root.config(bg="#f4f4f4")

# Title label
title_label = tk.Label(root, text="HTTP Web Client", font=("Helvetica", 18, "bold"), bg="#f4f4f4")
title_label.pack(pady=10)

# Frame for URL entry
url_frame = tk.Frame(root, bg="#f4f4f4")
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="Website URL:", font=("Helvetica", 12), bg="#f4f4f4")
url_label.grid(row=0, column=0, padx=5)

url_entry = tk.Entry(url_frame, width=50, font=("Helvetica", 12))
url_entry.grid(row=0, column=1, padx=5)

fetch_button = tk.Button(
    url_frame, text="Fetch Webpage", font=("Helvetica", 12), 
    bg="#4CAF50", fg="white", command=fetch_webpage, padx=10, pady=5
)
fetch_button.grid(row=0, column=2, padx=5)

# Status label
status_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"), bg="#f4f4f4")
status_label.pack()

# Frame for displaying headers and content
frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(pady=10, fill="both", expand=True)

# Webpage details area
details_label = tk.Label(frame, text="Webpage Headers:", font=("Helvetica", 12, "bold"), bg="#f4f4f4")
details_label.grid(row=0, column=0, sticky="w")

details_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=20, font=("Courier New", 10), state="disabled", bg="#f9f9f9")
details_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Webpage content area
content_label = tk.Label(frame, text="Webpage Content:", font=("Helvetica", 12, "bold"), bg="#f4f4f4")
content_label.grid(row=0, column=1, sticky="w")

content_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=20, font=("Courier New", 10), state="disabled", bg="#f9f9f9")
content_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Configure resizing behavior
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=2)
frame.grid_rowconfigure(1, weight=1)

root.mainloop()
