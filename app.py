import messages
import logic


messages.show_message(messages.hello_txt)
messages.show_message(messages.login_txt)
logic.type_login()
messages.show_message(messages.pass_txt)
logic.type_password()
# print(f"Podane log: {data.usr_login}")
# print(f"Podane hasło: {data.usr_pass}")

logic.credential_check()
