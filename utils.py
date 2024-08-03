import os
import shortuuid


def purge_folder(folder_path):
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")


def put_message_to_queue(message, to, filename=""):
    path = os.environ.get("SMS_MESSAGE_PATH")
    target_file = filename if filename != "" else shortuuid.uuid()
    f = open(path + "/outgoing/" + target_file + ".sms", "w+")
    f.write(f"To: {to}\n\n\n{message}")
    f.close()
