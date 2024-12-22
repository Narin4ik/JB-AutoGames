import pyautogui
import pygetwindow as gw
import time
import tkinter as tk
from tkinter import ttk

def get_window_list():
    return [title.strip() for title in gw.getAllTitles() if title and title.strip()]  # Только окна с ненулевым заголовком

def get_window_coordinates(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        return {
            "left": window.left,
            "top": window.top,
            "width": window.width,
            "height": window.height
        }
    except IndexError:
        print(f"Header window '{window_title}' not found.")
        return None

def get_relative_mouse_position(window_coords):
    if not window_coords:
        return None

    mouse_x, mouse_y = pyautogui.position()
    relative_x = mouse_x - window_coords["left"]
    relative_y = mouse_y - window_coords["top"]

    if 0 <= relative_x <= window_coords["width"] and 0 <= relative_y <= window_coords["height"]:
        return relative_x, relative_y
    else:
        return None

def start_tracking(selected_window):
    window_coords = get_window_coordinates(selected_window)
    if not window_coords:
        return

    print(f"Window coordinates: {window_coords}")

    while True:
        relative_position = get_relative_mouse_position(window_coords)
        if relative_position:
            print(f"The relative position of the mouse: {relative_position}")
        else:
            print("The mouse is outside the window area.")

        time.sleep(1)

def select_window():
    def on_select():
        selected_window = combo.get()
        root.destroy()
        start_tracking(selected_window)

    root = tk.Tk()
    root.title("Get mouse position in window")

    tk.Label(root, text="Select a window:").pack(pady=10)

    window_list = get_window_list()
    combo = ttk.Combobox(root, values=window_list, width=50)
    combo.pack(pady=10)
    combo.current(0)

    tk.Button(root, text="Start", command=on_select).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    select_window()