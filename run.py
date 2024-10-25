import os
import subprocess
import time
from datetime import datetime

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class SimpleRunner:
    def __init__(self):
        self.history = []  # Menyimpan riwayat file yang dijalankan
        self.favorites = set()  # Menyimpan file favorit
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        self.clear_screen()
        print(f"""{Colors.CYAN}
╔══════════════════════════════════╗
║        TEPAKS QUICK RUNNER       ║
║  Simple & Fast Python Launcher   ║
╚══════════════════════════════════╝{Colors.RESET}""")
        print(f"\n{Colors.GREEN}Whatsapp: https://wa.me/+6281392742485{Colors.RESET}")

    def show_help(self):
        print(f"""
{Colors.BOLD}Panduan Penggunaan:{Colors.RESET}
1. Ketik nomor file untuk menjalankan
2. Perintah khusus:
   {Colors.GREEN}f{Colors.RESET} = Tampilkan file favorit
   {Colors.GREEN}h{Colors.RESET} = Tampilkan riwayat
   {Colors.GREEN}r{Colors.RESET} = Refresh daftar file
   {Colors.GREEN}c{Colors.RESET} = Bersihkan layar
   {Colors.GREEN}q{Colors.RESET} = Keluar program
   {Colors.GREEN}?{Colors.RESET} = Tampilkan panduan ini
""")

    def get_python_files(self, directory='.'):
        python_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    # Jika file di direktori saat ini, tampilkan nama file saja
                    display_path = file if root == '.' else full_path
                    python_files.append((display_path, full_path))
        return python_files

    def run_file(self, file_path):
        try:
            print(f"\n{Colors.BLUE}[Menjalankan] {file_path}{Colors.RESET}")
            print("=" * 50)
            start_time = time.time()
            subprocess.run(['python', file_path], check=True)
            duration = time.time() - start_time
            print("=" * 50)
            print(f"{Colors.GREEN}[Selesai] Waktu eksekusi: {duration:.2f} detik{Colors.RESET}")
            input(f"\n{Colors.YELLOW}Tekan Enter untuk melanjutkan...{Colors.RESET}")
            self.history.append((file_path, datetime.now()))
            return True
        except Exception as e:
            print(f"{Colors.RED}[Error] {str(e)}{Colors.RESET}")
            input(f"\n{Colors.YELLOW}Tekan Enter untuk melanjutkan...{Colors.RESET}")
            return False

    def show_history(self):
        if not self.history:
            print(f"{Colors.YELLOW}Belum ada riwayat eksekusi.{Colors.RESET}")
            return
        print(f"\n{Colors.BOLD}Riwayat Eksekusi:{Colors.RESET}")
        for path, time in reversed(self.history[-5:]):  # Tampilkan 5 terakhir
            print(f"{time.strftime('%H:%M:%S')} - {path}")

    def refresh_display(self, files):
        self.print_banner()
        print(f"\n{Colors.BOLD}File Python yang Tersedia:{Colors.RESET}")
        for i, (display_path, _) in enumerate(files, 1):
            star = "⭐" if display_path in self.favorites else "  "
            print(f"{Colors.CYAN}{i}.{Colors.RESET} {star} {display_path}")

    def main(self):
        self.print_banner()
        self.show_help()
        
        while True:
            try:
                files = self.get_python_files()
                if not files:
                    print(f"{Colors.RED}Tidak ada file Python di direktori ini.{Colors.RESET}")
                    break

                print(f"\n{Colors.BOLD}File Python yang Tersedia:{Colors.RESET}")
                for i, (display_path, _) in enumerate(files, 1):
                    star = "⭐" if display_path in self.favorites else "  "
                    print(f"{Colors.CYAN}{i}.{Colors.RESET} {star} {display_path}")

                choice = input(f"\n{Colors.BOLD}Pilih nomor file atau perintah (? untuk bantuan): {Colors.RESET}").lower()

                if choice == 'q':
                    self.clear_screen()
                    print(f"{Colors.GREEN}Terima kasih telah menggunakan Tepaks Quick Runner!{Colors.RESET}")
                    break
                elif choice == '?':
                    self.clear_screen()
                    self.print_banner()
                    self.show_help()
                elif choice == 'h':
                    self.clear_screen()
                    self.print_banner()
                    self.show_history()
                elif choice == 'c':
                    self.clear_screen()
                    self.print_banner()
                elif choice == 'r':
                    self.clear_screen()
                    self.print_banner()
                    print(f"{Colors.GREEN}Daftar file diperbarui!{Colors.RESET}")
                elif choice == 'f':
                    self.clear_screen()
                    self.print_banner()
                    if not self.favorites:
                        print(f"{Colors.YELLOW}Belum ada file favorit.{Colors.RESET}")
                    else:
                        print(f"\n{Colors.BOLD}File Favorit:{Colors.RESET}")
                        for fav in self.favorites:
                            print(f"⭐ {fav}")
                elif choice.isdigit() and 1 <= int(choice) <= len(files):
                    idx = int(choice) - 1
                    _, full_path = files[idx]
                    if self.run_file(full_path):
                        self.clear_screen()
                        self.refresh_display(files)
                        # Tanya apakah ingin menambahkan ke favorit
                        if files[idx][0] not in self.favorites:
                            add_fav = input(f"\n{Colors.YELLOW}Tambahkan ke favorit? (y/n): {Colors.RESET}").lower()
                            if add_fav == 'y':
                                self.favorites.add(files[idx][0])
                                print(f"{Colors.GREEN}Ditambahkan ke favorit!{Colors.RESET}")
                    self.clear_screen()
                    self.refresh_display(files)
                else:
                    print(f"{Colors.RED}Pilihan tidak valid. Ketik ? untuk bantuan.{Colors.RESET}")

            except KeyboardInterrupt:
                self.clear_screen()
                print(f"\n{Colors.YELLOW}Program dihentikan oleh pengguna.{Colors.RESET}")
                break
            except Exception as e:
                print(f"{Colors.RED}Error: {str(e)}{Colors.RESET}")
                continue

if __name__ == '__main__':
    runner = SimpleRunner()
    runner.main()