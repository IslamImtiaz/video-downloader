from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window

import yt_dlp
import threading
import os

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 20

    MDTextField:
        id: url_input
        hint_text: "Enter video URL"
        mode: "rectangle"
        size_hint_y: None
        height: "48dp"

    MDRaisedButton:
        text: "Select Folder & Download"
        pos_hint: {"center_x": 0.5}
        on_release: app.open_file_manager()
'''

class VideoDownloaderApp(MDApp):
    def build(self):
        self.dialog = None
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.start_download
        )
        return Builder.load_string(KV)

    def open_file_manager(self):
        self.file_manager.show('/')  # Start at root directory

    def close_file_manager(self, *args):
        self.file_manager.close()
        self.manager_open = False

    def show_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="Close", on_release=self.close_dialog)
            ]
        )
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

    def start_download(self, folder_path):
        self.close_file_manager()

        url = self.root.ids.url_input.text.strip()
        if not url:
            Snackbar(text="Please enter a video URL.").open()
            return

        if not os.path.isdir(folder_path):
            Snackbar(text="Invalid folder selected.").open()
            return

        self.show_dialog("Downloading...", "Please wait while your video downloads.")
        threading.Thread(target=self.download_video, args=(url, folder_path), daemon=True).start()

    def download_video(self, url, folder):
        try:
            output_path = os.path.join(folder, "%(title)s.%(ext)s")
            ydl_opts = {'outtmpl': output_path, 'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.dialog.title = "Download Complete"
            self.dialog.text = f"Saved to:\n{folder}"
        except Exception as e:
            self.dialog.title = "Error"
            self.dialog.text = f"Failed to download: {str(e)}"

if __name__ == '__main__':
    Window.size = (400, 600)
    VideoDownloaderApp().run()