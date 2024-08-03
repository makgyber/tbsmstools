import os
import tkinter
import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap import Style
from dotenv import load_dotenv
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class QueuedMessages(ttk.Frame):
    col_data = [
        {"text": "To", "stretch": False},
        {"text": "Message", "stretch": True},
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        self.dt = Tableview(
            master=self,
            autofit=True,
            coldata=self.col_data,
            rowdata=self.get_row_data(),
            paginated=True,
            searchable=False,
            bootstyle=PRIMARY,
        )
        self.dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    def get_row_data(self):
        msg_path = os.environ.get("SMS_MESSAGE_PATH", "/var/spool/sms") + "/outgoing"
        rowData = []
        for x in os.listdir(msg_path):
            if x.endswith(".sms"):
                f = open(f"{msg_path}/{x}")
                to = ""
                msg = ""
                for line in f:
                    if len(line) > 0:
                        if line.startswith("To: "):
                            to = line.replace("To: ", "")
                        else:
                            msg = line
                rowData.append((to, msg))
                to = ""
                msg = ""
        return rowData

    def refresh_data(self):
        self.dt.build_table_data(coldata=self.col_data, rowdata=self.get_row_data())
        self.dt.reset_table()


class SentMessages(ttk.Frame):
    coldata = [
        "To",
        "Modem",
        "Date sent",
        "Sending time",
        "IMSI",
        "IMEI",
        {"text": "Message", "stretch": True},
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        self.dt = Tableview(
            master=self,
            coldata=self.coldata,
            rowdata=self.get_row_data(),
            paginated=True,
            searchable=False,
            bootstyle=SUCCESS,
        )
        self.dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    def refresh_data(self):
        self.dt.build_table_data(coldata=self.coldata, rowdata=self.get_row_data())
        self.dt.reset_table()

    def get_row_data(self):
        msg_path = os.environ.get("SMS_MESSAGE_PATH", "/var/spool/sms") + "/sent"
        rowdata = []
        for x in os.listdir(msg_path):
            if x.endswith(".sms"):
                f = open(f"{msg_path}/{x}")
                to = ""
                msg = ""
                modem = ""
                sent = ""
                sending_time = ""
                imsi = ""
                imei = ""
                for line in f:
                    if len(line) > 0:
                        if line.startswith("To: "):
                            to = line.replace("To: ", "")
                        elif line.startswith("Modem: "):
                            modem = line.replace("Modem: ", "")
                        elif line.startswith("Sent: "):
                            sent = line.replace("Sent: ", "")
                        elif line.startswith("Sending_time: "):
                            sending_time = line.replace("Sending_time: ", "")
                        elif line.startswith("IMSI: "):
                            imsi = line.replace("IMSI: ", "")
                        elif line.startswith("IMEI: "):
                            imei = line.replace("IMEI: ", "")
                        else:
                            msg = line
                rowdata.append((to, modem, sent, sending_time, imsi, imei, msg))
                to = ""
                msg = ""
                modem = ""
                sent = ""
                sending_time = ""
                imsi = ""
                imei = ""
        return rowdata


class FailedMessages(ttk.Frame):
    coldata = [
        "To",
        "Modem",
        "Date failed",
        "IMSI",
        "IMEI",
        "Failure reason",
        {"text": "Message", "stretch": True},
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        self.dt = Tableview(
            master=self,
            coldata=self.coldata,
            rowdata=self.get_row_data(),
            paginated=True,
            searchable=False,
            bootstyle=DANGER,
        )
        self.dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    def refresh_data(self):
        self.dt.build_table_data(coldata=self.coldata, rowdata=self.get_row_data())
        self.dt.reset_table()

    def get_row_data(self):
        msg_path = os.environ.get("SMS_MESSAGE_PATH", "/var/spool/sms") + "/failed"
        rowdata = []
        for x in os.listdir(msg_path):
            if x.endswith(".sms"):
                f = open(f"{msg_path}/{x}")
                to = ""
                msg = ""
                modem = ""
                failed = ""
                failed_reason = ""
                imsi = ""
                imei = ""
                for line in f:
                    if len(line) > 0:
                        if line.startswith("To: "):
                            to = line.replace("To: ", "")
                        elif line.startswith("Modem: "):
                            modem = line.replace("Modem: ", "")
                        elif line.startswith("Failed: "):
                            failed = line.replace("Failed: ", "")
                        elif line.startswith("Fail_reason: "):
                            failed_reason = line.replace("Fail_reason: ", "")
                        elif line.startswith("IMSI: "):
                            imsi = line.replace("IMSI: ", "")
                        elif line.startswith("IMEI: "):
                            imei = line.replace("IMEI: ", "")
                        else:
                            msg = line
                rowdata.append((to, modem, failed, imsi, imei, failed_reason, msg))
                to = ""
                msg = ""
                modem = ""
                failed = ""
                failed_reason = ""
                imsi = ""
                imei = ""
        return rowdata


class LogsWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        self.label = ttk.Label(text="Refresh logs")
        self.label.pack(padx=5)
        self.output_text = ttk.Text()
        self.output_text.pack(fill=BOTH, expand=YES, padx=5, pady=5)


#  def create_sent_table(self):
#      pass
#
#  def create_message_form(self):
#      container = ttk.Frame(self)
#      container.pack(fill=X, expand=YES, pady=(15, 10))
#      self.to = ttk.StringVar(value="")
#      self.message = ttk.StringVar(value="")
#      self.create_form_entry("To:", self.to, container)
#      self.create_form_entry("Message:", self.message, container)
#      self.create_buttonbox(container)
#      return container
#
# def create_form_entry(self, label, variable, root):
#    """Create a single form entry"""
#    container = ttk.Frame(root)
#    container.pack(fill=X, expand=NO, pady=5)
#    lbl = ttk.Label(master=container, text=label.title(), width=10)
#    lbl.pack(side=LEFT, padx=5)
#    ent = ttk.Entry(master=container, textvariable=variable)
#    ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
#
# def create_buttonbox(self, root):
#    """Create the application buttonbox"""
#    container = ttk.Frame(root)
#    container.pack(fill=X, expand=YES, pady=(15, 10))
#    sub_btn = ttk.Button(
#       master=container,
#       text="Submit",
#       command=self.on_submit,
#       bootstyle=SUCCESS,
#       width=6,
#    )
#    sub_btn.pack(side=RIGHT, padx=5)
#    sub_btn.focus_set()
#    cnl_btn = ttk.Button(
#       master=container,
#       text="Cancel",
#       command=self.on_cancel,
#       bootstyle=DANGER,
#       width=6,
#    )
#    cnl_btn.pack(side=RIGHT, padx=5)
#    return container
#
# def on_submit(self):
#    """Print the contents to console and return the values."""
#    print("Name:", self.name.get())
#    print("Address:", self.address.get())
#    print("Phone:", self.phone.get())
#    return self.name.get(), self.address.get(), self.phone.get()
#


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
        file_menu.add_command(label="Modem activity logs", command=self.refresh_logs)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=quit_app)

        menubar.add_cascade(menu=file_menu, label="Messages")

        self.tabs = ttk.Notebook(padding=5, width=self.winfo_screenwidth())
        self.queued_messages = QueuedMessages(self, padding=2)
        self.tabs.add(self.queued_messages, text="Queued", sticky="nsew")
        self.sent_messages = SentMessages(self, padding=2)
        self.tabs.add(self.sent_messages, text="Sent", sticky="nsew")
        self.failed_messages = FailedMessages(self, padding=2)
        self.tabs.add(self.failed_messages, text="Failed", sticky="nsew")

        self.tabs.pack()
        self.separator = ttk.Separator(style="info.Horizontal.TSeparator")
        self.separator.pack()
        self.logs_window = LogsWindow(self, relief="sunken")
        self.logs_window.after(3000, self.refresh_logs)
        self.config(menu=menubar)
        # self.refresh_logs()

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
