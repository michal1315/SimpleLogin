import data
import messages
import log_logic


def log_write():
    messages.show_message(messages.create_account_log)
    data.log_to_write = input()
    write_line(data.log_to_write)


def pass_write():
    messages.show_message(messages.create_account_pass)
    data.pass_to_write = input()
    write_line(data.pass_to_write)


def write_line(to_write):
    log_logic.file_operation.write(to_write + "\n")


def add_new_account():
    log_write()
    pass_write()
    return 0
