import threading
from socket import AF_INET, socket, SOCK_STREAM
import tkinter

nickname = input("Choose a nickname : ")
if nickname == 'admin':
    password = input("Enter password for admin : ")

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

stop_thread = False

def receive():
    while True:

        global stop_thread
        if stop_thread:
            break
        try:

            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')

                if next_message == 'PASS':

                    client.send(password.encode('ascii'))

                    if client.recv(1024).decode('ascii')== 'REFUSE':
                        msg_list.insert(tkinter.END, "Connection was refused! wrong password!")
                        stop_thread = True
                elif next_message == 'BAN':
                    msg_list.insert(tkinter.END, 'Connection refused beacuse of ban!')
                    client.close()
                    stop_thread = True
            else:
                msg_list.insert(tkinter.END, message)


        except:
            msg_list.insert(tkinter.END, "An error occurred!")
            client.close()
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    message = f'{nickname}: {msg}'
    if message[len(nickname) + 2:].startswith('/'):
        if nickname == 'admin':
            if message[len(nickname) + 2:].startswith('/kick'):
                client.send(f'KICK {message[len(nickname) + 2 + 6:]}'.encode('ascii'))
            elif message[len(nickname) + 2:].startswith('/ban'):
                client.send(f'BAN {message[len(nickname) + 2 + 5:]}'.encode('ascii'))
        else:
            msg_list.insert(tkinter.END, "Comands can only be executd by admin!")
    elif message[len(nickname) + 2:].startswith('\quit'):
        client.send(f'QUIT'.encode('ascii'))
        client.close()
        top.quit()
    else:
        client.send(message.encode('ascii'))
        if message == f"{nickname}: \quit":
            client.close()
            top.quit()



def on_closing(event=None):
    """This function is to be called when the window is closed."""
    client.close()
    top.quit()

top = tkinter.Tk()
top.title("Chat On!")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

tkinter.mainloop()
















