import data
import messages
import write_logic

file_operation = open(data.file_name, mode="r+", encoding="utf-8")
lines_read = file_operation.readlines()


def type_login():
    data.usr_login = input()


def type_password():
    data.usr_pass = input()


def credential_check():
    file_lines_num = file_len()
    current_line = 0

    for read_line in range(file_lines_num):
        if current_line < file_lines_num:
            login = lines_read[current_line].strip("\n")
            password = lines_read[current_line + 1].strip("\n")
            # print(f"login: {login}")
            # print(f"pass: {password}")
            # print(f"login podany: {data.usr_login}")
            # print(f"pass podany: {data.usr_pass}")
            current_line += 2

            if login == data.usr_login and password == data.usr_pass:
                messages.show_message(messages.good_credential)
                break
        else:
            messages.show_message(messages.bad_credential)
            messages.show_message(messages.create_account_answer)
            create_account_chose()


def create_account_chose():
    answer = input()
    if answer.lower() == "y":

        messages.show_message(messages.create_account_yes)
        write_logic.log_write()
        write_logic.pass_write()
        messages.show_message(messages.create_account_finish)
        exit()
    else:
        messages.show_message(messages.create_account_no)


def file_len():
    lines_num = 0
    for data in lines_read:
        lines_num += 1
    return lines_num
