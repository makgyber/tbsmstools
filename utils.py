import os
import shortuuid


def put_message_to_queue(message, to, filename=""):
    path = os.environ.get("SMS_MESSAGE_PATH")
    target_file = filename if filename != "" else shortuuid.uuid()
    f = open(path + "/outgoing/" + target_file + ".sms", "w+")
    f.write(f"To: {to}\n\n\n{message}")
    f.close()
