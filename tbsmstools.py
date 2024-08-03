import os
import tkinter
import subprocess

import shortuuid
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from messages import QueuedMessages, SentMessages, FailedMessages


class LogsWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(
            fill=BOTH, expand=YES, side=BOTTOM, padx=5, pady=5, ipadx=10, ipady=10
        )
        self.config(relief=RIDGE)

        ttk.Label(
            self,
            text="Modem activity logs",
            justify=LEFT,
            anchor="w",
            font=("Helvetica", 16),
        ).pack(fill=X, expand=YES, padx=10)

        self.output_text = ttk.ScrolledText(self)
        self.output_text.bind("<Key>", lambda e: "break")
        self.output_text.pack(fill=BOTH, expand=True, side=BOTTOM, padx=10, pady=10)


class MessageForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES, side=TOP, padx=20, pady=20)
        self.config(relief=SUNKEN)
        self.columnconfigure(2, weight=1)
        ttk.Label(
            self,
            text="Create new SMS message",
            width=60,
            font=("Helvetica", 18),
        ).grid(columnspan=2, pady=10, padx=10)

        ttk.Label(
            self,
            text="To: ",
        ).grid(row=1, column=0, sticky="ew", pady=10, padx=(10, 10))
        self.to_entry = ttk.Entry(self)
        self.to_entry.grid(row=1, column=1, sticky="ew", columnspan=2, padx=20)

        ttk.Label(self, text="Body: ").grid(
            row=2, column=0, sticky="ew", pady=10, padx=(10, 10)
        )
        self.body_text = ttk.Text(self, height=3)
        self.body_text.grid(row=2, column=1, sticky="ew", columnspan=2, padx=20)
        self.submit_btn = ttk.Button(
            self,
            text="Submit",
            command=self.on_submit,
            style="success.TButton",
        )
        self.submit_btn.grid(
            row=4, column=2, sticky="ew", pady=10, padx=(10, 20), columnspan=1
        )

    def on_submit(self):
        path = os.environ.get("SMS_MESSAGE_PATH")
        f = open(path + "/outgoing/" + shortuuid.uuid() + ".sms", "w")
        to = self.to_entry.get()
        message = self.body_text.get("1.0", END)
        f.write(f"To: {to}\n\n\n{message}")
        f.close()
        self.to_entry.delete(0, END)
        self.body_text.delete("0.0", END)


class TbSmsTools(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("SMS Tools")
        self.style = Style("darkly")

        menubar = ttk.Menu()
        file_menu = ttk.Menu(menubar, tearoff=False)
        file_menu.add_command(
            label="New Message",
        )
        file_menu.add_command(label="Refresh logs", command=self.refresh_logs)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=quit_app)

        menubar.add_cascade(menu=file_menu, label="Messages")

        self.message_form = MessageForm(self)

        self.tabs = ttk.Notebook(
            padding=10,
            width=self.winfo_screenwidth(),
        )
        self.queued_messages = QueuedMessages(self, padding=2)
        self.tabs.add(self.queued_messages, text="Queued", sticky="nsew")
        self.sent_messages = SentMessages(self, padding=2)
        self.tabs.add(self.sent_messages, text="Sent", sticky="nsew")
        self.failed_messages = FailedMessages(self, padding=2)
        self.tabs.add(self.failed_messages, text="Failed", sticky="nsew")
        self.tabs.pack()

        self.logs_window = LogsWindow(self)

        self.logs_window.after(3000, self.refresh_logs)
        self.config(menu=menubar)
        self.refresh_logs()

    def refresh_logs(self):
        # The command you want to execute
        command = "tail " + os.environ.get("TAIL_LOG_PATH", "")

        # Use subprocess to run the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Display the output in the Text widget
        self.logs_window.output_text.delete("1.0", ttk.END)  # Clear previous output
        self.logs_window.output_text.insert(ttk.END, result.stdout)
        self.logs_window.output_text.insert(ttk.END, result.stderr)


class MessageHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"File {event.src_path} has been modified")
        if "outgoing" in event.src_path:
            app.queued_messages.refresh_data()
        if "sent" in event.src_path:
            app.sent_messages.refresh_data()
        if "failed" in event.src_path:
            app.failed_messages.refresh_data()


def quit_app():
    quit()


if __name__ == "__main__":
    load_dotenv(".env")
    app = TbSmsTools()
    event_handler = MessageHandler()
    observer = Observer()
    observer.schedule(event_handler, os.environ.get("SMS_MESSAGE_PATH"), recursive=True)
    observer.start()
    app.mainloop()
    observer.stop()
    observer.join()
