import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, PhotoImage, Menu
import pygame
import os
import random
from pygame import error as pygame_error

from PIL import Image, ImageTk

# FINALS_DSA.py

class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.current_node = None
        self.length = 0
        self.playing = False  # Add a playing attribute

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.current_node = self.head
        else:
            new_node.prev = self.current_node
            self.current_node.next = new_node
            self.current_node = new_node
        self.length += 1

    def insert_at_position(self, data, position):
        new_node = Node(data)
        if position == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:
            current = self.head
            for _ in range(position - 1):
                if current.next:
                    current = current.next
                else:
                    break
            new_node.prev = current
            new_node.next = current.next
            if current.next:
                current.next.prev = new_node
            current.next = new_node
        self.length += 1

    def delete(self, position):
        if position == 0:
            if self.head:
                self.head = self.head.next
                if self.head:
                    self.head.prev = None
        else:
            current = self.head
            for _ in range(position):
                if current:
                    current = current.next
                else:
                    break
            if current:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
        self.length -= 1

    def next(self):
        if self.current_node and self.current_node.next:
            self.current_node = self.current_node.next

    def previous(self):
        if self.current_node is not None and self.current_node.prev is not None:
            print("Previous Node before navigation:", self.current_node.prev.data)
            self.current_node = self.current_node.prev
            print("Current Node after navigation:", self.current_node.data)
        else:
            print("No previous node available.")

    def next(self):
        if self.current_node and self.current_node.next:
            self.current_node = self.current_node.next

    def play(self):
        # Implement your play logic here
        self.playing = True

    def pause(self):
        # Implement your pause logic here
        self.playing = False

    def is_playing(self):
        # Return the boolean value of the playing attribute
        return self.playing

    def prev(self):
        if self.current_node and self.current_node.prev:
            self.current_node = self.current_node.prev


class MusicPlayer:
    def __init__(self, master=None):
        self.master = master
        if master is not None:
            # Title
            self.master.title("Melo")

            # Background configuration
            title_font = ("Inter", 12, "bold")
            bg_color = "#111320"
            self.master.configure(bg=bg_color)

        # Functional Things
        self.paused = False
        pygame.mixer.init()
        self.playlist = DoublyLinkedList()
        self.current_music = None

        # Set the minimum and maximum width and height
        self.master.minsize(700, 370)
        self.master.maxsize(700, 370)

        # Calculate the center position
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_position = (screen_width - 700) // 2
        y_position = (screen_height - 370) // 2

        # Set the window position
        self.master.geometry(f"700x370+{x_position}+{y_position}")

        # Set background image using Pillow
        background_image = Image.open("background.png")
        background_image = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.master, image=background_image)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_image  # to prevent garbage collection

        # Create a canvas on the left side
        canvas = tk.Canvas(self.master, width=222, height=370, bg="white")
        canvas.pack(side="left", anchor=tk.NW)

        # Create a buttons
        button_color = "white"
        text_color = "#3A12CD"
        button_font = ("Inter", 14)

        self.prev_button = tk.Button(root, command=self.prev_music, text="⏮", bg=button_color, fg=text_color, bd=0, font=button_font, width=4, height=2).place(x=22, y=313)
        self.pause_button = tk.Button(root, command=self.pause_music, text="⏸", bg=button_color, fg=text_color, bd=0, font=button_font, width=4, height=2).place(x=62, y=313)
        self.play_button = tk.Button(root, command=self.unpause_music, text="▶", bg=button_color, fg=text_color, bd=0, font=button_font, width=4, height=2).place(x=102, y=313)
        self.play_from_top_button = tk.Button(root, command=self.play_from_top, text="⏏", bg="white", fg="red", bd=0, width=2, height=0).place(x=200, y=320)
        self.stop_button = tk.Button(root, command=self.stop_music, text="◼", bg="white", fg="black", bd=0, width=2, height=0).place(x=9, y=283)
        self.next_button = tk.Button(root, command=self.next_music, text="⏭", bg=button_color, fg=text_color, bd=0, font=button_font, width=4, height=2).place(x=142, y=313)
        self.shuffle_button = tk.Button(root, text="⇄", command=self.shuffle_playlist, bg="white", fg="black", bd=0, width=2, height=0).place(x=200, y=283)

        # Create a line at x=33, y=305 with a width of 208
        canvas.create_line(9, 310, 9 + 208, 310, fill="#C9C9C9", width=2)

        # Create a Toggle Menu Button
        toggle_btn = tk.Menubutton(self.master, text='☰', bg='white', fg='black',
                                   font=('Bold', 11), bd=0,
                                   activebackground=None, activeforeground='black',
                                   highlightthickness=0)
        toggle_btn.place(x=14, y=21.31)
        toggle_btn.menu = Menu(toggle_btn, tearoff=0, bg="white")
        toggle_btn.menu.add_command(label="Add Song", command=self.add_music)
        toggle_btn.menu.add_command(label="Sort Alphabetically", command=self.sort_alphabetically)
        toggle_btn.menu.add_command(label="Delete", command=self.delete_music)
        toggle_btn.menu.add_separator()
        toggle_btn.menu.add_command(label="Quit", command=self.quit_app)
        toggle_btn["menu"] = toggle_btn.menu

        # Create a Textbox inside the canvas with vertical scrollbar
        self.textbox = tk.Text(canvas, width=25, height=14, state=tk.DISABLED, bg="seashell3", wrap=tk.WORD)
        self.textbox.place(x=10, y=50, anchor=tk.NW)

        # Add a vertical scrollbar to the Textbox
        scrollbar = tk.Scrollbar(canvas, command=self.textbox.yview)
        scrollbar.place(x=220, y=50, anchor=tk.NW)
        self.textbox.config(yscrollcommand=scrollbar.set)

        # Create a Label on the right for the currently playing song
        self.song_name_label = tk.Label(self.master, text="", font=("Inter", 29, "bold"), bg=bg_color, fg="white",
                                        highlightthickness=0)
        self.song_name_label.place(x=235.83, y=9)

        self.artist_label = tk.Label(self.master, text="", font=("Inter", 15), bg=bg_color, fg="white",
                                     highlightthickness=0)
        self.artist_label.place(x=239, y=50.31)

    def initialize_music(self):
        pygame.mixer.init()


    def create_menu_button(self):
        menu_button = tk.Menubutton(self.master, text="Menu", font=("Inter", 10, "bold"), fg="black",
                                    activebackground="#111320", activeforeground="white", bd=0)

        menu = tk.Menu(menu_button, tearoff=0)
        menu.add_command(label="Add Song", command=self.add_music)
        menu.add_command(label="Sort Alphabetically", command=self.sort_alphabetically)
        menu.add_command(label="Delete", command=self.delete_music)
        menu.add_separator()
        menu.add_command(label="Quit", command=self.quit_app)

        menu_button.configure(menu=menu)
        return menu_button

    def sort_alphabetically(self):
        playlist_items = []
        current = self.playlist.head
        while current:
            playlist_items.append(current.data)
            current = current.next

        # Sort the list of dictionaries based on the 'title' key
        playlist_items.sort(key=lambda x: x.get('title', '').lower())

        self.playlist = DoublyLinkedList()
        for item in playlist_items:
            self.playlist.insert(item)

        # Set current_music to the head of the sorted playlist
        self.current_music = self.playlist.head
        # Play the song at the top of the sorted playlist immediately
        self.play_music()
        self.update_textbox()

    def play_from_top(self):
        if self.playlist.head:
            pygame.mixer.music.load(self.playlist.head.data["file_path"])
            pygame.mixer.music.play()
            self.current_music = self.playlist.head
            self.update_current_song_label()

    def play_music(self):
        if self.current_music:
            pygame.mixer.music.load(self.current_music.data["file_path"])
            pygame.mixer.music.play()
            self.update_current_song_label()

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def unpause_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        elif not pygame.mixer.music.get_busy():
            # If not paused and no music is currently playing, play the music
            self.play_music()

    def stop_music(self):
        pygame.mixer.music.stop()

    def add_music(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
            if file_path:
                if not self.is_valid_mp3(file_path):
                    raise ValueError("Invalid or corrupt MP3 file. Please choose a valid MP3 file.")
                if self.check_duplicate(file_path):
                    raise ValueError("Duplicate file found.")

                title = ""
                artist = ""

                while not title.strip() or not artist.strip():
                    title = simpledialog.askstring("Song Info", "Enter the Title of the song:")
                    artist = simpledialog.askstring("Song Info", "Enter the Artist of the song:")

                    if not title.strip() or not artist.strip():
                        messagebox.showwarning("Warning", "Title and Artist cannot be empty. Please try again.")

                self.playlist.insert({"title": title, "artist": artist, "file_path": file_path})
                self.current_music = self.playlist.head
                self.update_textbox()

        except Exception as e:
            self.show_error_message(f"Error: {str(e)}")
            self.show_try_again_window()

    def is_valid_mp3(self, file_path):
        try:
            # Attempt to load the MP3 file using pygame.mixer
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            return True
        except pygame_error.PygameError:
            return False

    def check_duplicate(self, file_path):
        current = self.playlist.head
        while current:
            if current.data["file_path"] == file_path:
                return True
            current = current.next
        return False

    def next_music(self):
        if self.current_music and self.current_music.next:
            self.current_music = self.current_music.next
            self.play_music()

    def prev_music(self):
        if self.current_music and self.current_music.prev:
            self.current_music = self.current_music.prev
            self.play_music()

    def quit_app(self):
        self.master.destroy()

    def update_textbox(self):
        self.textbox.config(state=tk.NORMAL)  # Set state to normal to update the content
        self.textbox.delete(1.0, tk.END)  # Clear the existing content
        current = self.playlist.head
        song_no = 1
        while current:
            title = current.data.get("title", "")
            artist = current.data.get("artist", "")
            self.textbox.insert(tk.END, f"No: {song_no} - {title} by {artist}\n")
            current = current.next
            song_no += 1
        self.textbox.config(state=tk.DISABLED)  # Set state back to disabled

    def shuffle_playlist(self):
        playlist_items = []
        current = self.playlist.head
        while current:
            playlist_items.append(current.data)
            current = current.next
        random.shuffle(playlist_items)
        self.playlist = DoublyLinkedList()
        for item in playlist_items:
            self.playlist.insert(item)

        # Set current_music to the head of the shuffled playlist
        self.current_music = self.playlist.head
        self.update_textbox()

        # Play the song at the top of the shuffled playlist immediately
        self.play_music()

    def update_current_song_label(self):
        if self.current_music:
            title = self.current_music.data.get("title", "")
            artist = self.current_music.data.get("artist", "")

            self.song_name_label.config(text=title)
            self.artist_label.config(text=artist)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def show_try_again_window(self):
        try_again_window = tk.Toplevel(self.master)
        try_again_window.title("Try Again")
        try_again_label = tk.Label(try_again_window, text="An error occurred. Please try again.")
        try_again_label.pack(padx=20, pady=20)
        try_again_button = tk.Button(try_again_window, text="OK", command=try_again_window.destroy)
        try_again_button.pack(pady=10)

    def delete_music(self):
        try:
            if not self.playlist.head:
                raise ValueError("Playlist is empty. Nothing to delete.")

            # Ask the user for the song number to delete
            song_number = simpledialog.askinteger("Delete Song", "Enter the song number to delete:",
                                                  parent=self.master, minvalue=1, maxvalue=self.playlist.length)

            if not song_number:
                raise ValueError("Invalid song number entered.")

            # Find the node to delete
            current = self.playlist.head
            for _ in range(song_number - 1):
                current = current.next

            # Check if the deleted song is currently playing
            if current == self.current_music:
                # Stop the music and clear the display labels
                self.stop_music()
                self.song_name_label.config(text="")
                self.artist_label.config(text="")

            # Remove the node from the playlist
            if current.prev:
                current.prev.next = current.next
            else:
                self.playlist.head = current.next

            if current.next:
                current.next.prev = current.prev

            # Adjust the current_music pointer if needed
            if current == self.current_music:
                self.current_music = current.next

            # Update the length
            self.playlist.length -= 1

            # Update the display
            self.update_textbox()
            self.update_current_song_label()

            # Update current_node to point to the last node in the playlist
            current = self.playlist.head
            while current and current.next:
                current = current.next
            self.playlist.current_node = current

        except Exception as e:
            self.show_error_message(f"Error: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)

    # Load the icon image
    icon = tk.PhotoImage(file="Logo.png")

    # Set the window icon
    root.iconphoto(False, icon)

    root.mainloop()