import socket
import threading
import sys
import getpass

from selis.computerinfo import ComputerInfo
from selis.utils import convert_color, guide_to_exit, clear_screen, open_url


class ChatClient:
    def __init__(self, ip, port, nickname):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((ip, port))
        except:
            print(convert_color(f"[-] Sever not found", style="FAIL"))
            sys.exit()

        self.nickname = nickname
        self.send_client_info_to_sever()
        self.is_running = True


    def send_client_info_to_sever(self):
        client_computer = ComputerInfo().get()
        msg = self.nickname + "/" + client_computer
        self.send_message(msg)


    def send_message(self, message):
        self.connection.send(message.encode())


    def process_receiving_message(self):
        while True:
            try:
                response = self.connection.recv(1024).decode()

                if not response and self.connection:
                    print(convert_color("[-] Sever is not opening", style="FAIL"))
                    guide_to_exit()
                    break

                elif "admin/open-url" in response:
                    url = response.split(" ")[1]
                    open_url(url)

                elif response == "admin/close-server":
                    print(convert_color("[-] Admin closes the server", style="FAIL"))
                    guide_to_exit()
                    self.connection.close()
                    sys.exit(0)

                else:
                    print(response)

            except Exception:
                print(convert_color("[-] Connection is closed", style="FAIL"))
                self.connection.close()
                break


    def process_admin_mode(self):
        password = getpass.getpass(convert_color("[*] Admin's Password: \n>> ", style="ENDC"))
        msg = "check-admin/" + self.nickname + "/" + password
        self.send_message(msg)


    def process_sending_message(self):
        try:
            while True:
                content = input()

                if content == "/exit":
                    self.send_message(f"client/exit {self.nickname}")
                    self.connection.close()
                    break

                elif content == "/clear":
                    clear_screen()

                elif content == "/ls":
                    self.send_message(content)

                elif content == "/admin-mode":
                    self.process_admin_mode()

                elif content == "/close-server":
                    self.send_message(content)
                
                elif content == "/close":
                    self.send_message(content)

                elif content == "/open":
                    self.send_message(content)

                elif "/kick" in content:
                    self.send_message(content)

                elif "/ban" in content:
                    self.send_message(content)

                elif "/un-ban" in content:
                    self.send_message(content)

                elif "/open-url" in content:
                    self.send_message(content)

                elif "/msg" in content:
                    self.send_message(content)

                else:
                    content = convert_color(f">>> ({self.nickname}): {content}", style="ENDC")
                    self.send_message(content)
        except:
            sys.exit()


    def start(self):
        recieve_threading = threading.Thread(target=self.process_receiving_message)
        recieve_threading.start()
        
        send_threading = threading.Thread(target=self.process_sending_message)
        send_threading.start()

        recieve_threading.join()
        send_threading.join()
