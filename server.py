#Ragib Ahsan and Aanya Kutty
import PySimpleGUI as sg
import socket
import threading
import sqlite3

layout = [[sg.Frame("Users", [[sg.Multiline(key="-CLIENTS-", size=(30, 10), disabled=True)]]), sg.Button("Start Chatting")],[sg.Text("Host: "), sg.Text("0.0.0.0", key="-HOST-"), sg.Text("Port: "), sg.Text("8080", key="-PORT-")]]
window = sg.Window("Peer to Peer Server", layout)

host_add = "0.0.0.0"
host_port = 8080
clients = []
clients_names = []

def start_serve():
    global host_add, host_port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host_add, host_port))
    server.listen(5)
    window["-HOST-"].update(host_add)
    window["-PORT-"].update(host_port)
    threading._start_new_thread(listen, (server, ""))

def listen(server, y):
    global clients, clients_names
    while True:
        client, addr = server.accept()
        clients.append(client)
        threading._start_new_thread(messaging, (client, addr))

def messaging(client_connection, client_ip_addr):
    global clients, clients_names
    client_msg = ""
    client_name  = client_connection.recv(4096).decode()
    welcome_msg = "Welcome to the chatroom " 
    client_connection.send(welcome_msg.encode())

    clients_names.append(client_name)
    
    server_msg = f"{client_name} has joined the chat."
    for c in clients:
        if c != client_connection:
            c.send(server_msg.encode())

    update_client_names_display(clients_names) 

    while True:
        data = client_connection.recv(4096).decode()
        if not data: break
        if data == "exit": break

        client_msg = data

        idx = clients.index(client_connection)
        sending_client_name = clients_names[idx]

        for c in clients:
            if c != client_connection:
                server_msg = str(client_msg)
                c.send(server_msg.encode())

    idx = clients.index(client_connection)
    del clients_names[idx]
    del clients[idx]
    server_msg = "See you later!"
    client_connection.send(server_msg.encode())
    client_connection.close()

    update_client_names_display(clients_names) 

def update_client_names_display(name_list):
    clients_str = "\n".join(name_list)
    window["-CLIENTS-"].update(clients_str)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "Start Chatting":
        start_serve()

window.close()