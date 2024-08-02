import os
import tkinter
import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap import Style
from dotenv import load_dotenv


class QueuedMessages(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        msg_path = os.environ.get("SMS_MESSAGE_PATH", "/var/spool/sms") + "/outgoing"

        rowdata = []
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
                rowdata.append((to, msg))
                to = ""
                msg = ""

        coldata = [
            {"text": "To", "stretch": False},
            {"text": "Message", "stretch": True},
        ]

        dt = Tableview(
            master=self,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=False,
            bootstyle=PRIMARY,
        )
        dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)


class SentMessages(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

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

        coldata = [
            "To",
            "Modem",
            "Date sent",
            "Sending time",
            "IMSI",
            "IMEI",
            {"text": "Message", "stretch": True},
        ]

        dt = Tableview(
            master=self,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=False,
            bootstyle=SUCCESS,
        )
        dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)


class FailedMessages(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

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

        coldata = [
            "To",
            "Modem",
            "Date failed",
            "IMSI",
            "IMEI",
            "Failure reason",
            {"text": "Message", "stretch": True},
        ]

        dt = Tableview(
            master=self,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=False,
            bootstyle=DANGER,
        )
        dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)


class LogsWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        self.label = ttk.Label(
            text="Logs",
        )
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
        file_menu.add_command(label="Refresh logs", command=self.refresh_logs)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=quit_app)

        menubar.add_cascade(menu=file_menu, label="Messages")

        self.tabs = ttk.Notebook(padding=5, width=self.winfo_screenwidth())
        self.tabs.add(QueuedMessages(self, padding=2), text="Queued", sticky="nsew")
        self.tabs.add(SentMessages(self, padding=2), text="Sent", sticky="nsew")
        self.tabs.add(FailedMessages(self, padding=2), text="Failed", sticky="nsew")

        self.tabs.pack()
        self.separator = ttk.Separator(style="info.Horizontal.TSeparator")
        self.separator.pack()
        self.logs_window = LogsWindow(self, relief="sunken")
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


def quit_app():
    quit()


if __name__ == "__main__":
    load_dotenv(".env")
    TbSmsTools().mainloop()
