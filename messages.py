import os
from tkinter import BOTH, YES

import ttkbootstrap as ttk
from ttkbootstrap import PRIMARY, SUCCESS, DANGER
from ttkbootstrap.tableview import Tableview


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
