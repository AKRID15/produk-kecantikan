import csv
from collections import deque
from datetime import datetime, timedelta

produk_awal = [
    ("SK001", "Viva milk cleanser 100ml", "skincare", 50, 8000),
    ("SK002", "Viva face tonic 100ml", "skincare", 50, 8000),
    ("SK003", "Cetaphil Gentle Skin Cleanser 58ml", "skincare", 50, 55000),
    ("SK004", "Hadalabo Ultimate Moisturizing Milk 100ml", "skincare", 50, 57000),
    ("SK005", "Madagascar Centela", "skincare", 50, 0),
    ("SK006", "AIR - FIT SUNCREAM LIGHT SPF 30 PA++++ 50ml", "skincare", 50, 130000),
    ("BD001", "Nalpamara herbal soap 75g", "bodycare", 50, 25000),
    ("BD002", "Marina Hand & Body Lotion 460ml", "bodycare", 50, 18000),
    ("BD003", "Nivea Daily protection sun lotion 33 SPF PA+++ 100ml", "bodycare", 50, 45000),
    ("BD004", "Purbasari lulur mandi 200gram", "bodycare", 50, 20000),
    ("BD005", "Vaseline GLUTA-HYA 100ml", "bodycare", 50, 34000),
    ("BD006", "FAV BEAUTY body lotion 300ml", "bodycare", 50, 79000)
]

def safe_input(prompt):
    try:
        return input(prompt)
    except OSError:
        print(f"(Input tidak tersedia: {prompt})")
        return ""

class ProdukKecantikan:
    def __init__(self):
        self.produk = {}
        self.transaksi = deque()
        self.restok_log = []
        self.CSV_FILE = "produk_kecantikan.csv"
        self.TRANSAKSI_FILE = "transaksi.csv"
        self.load_data()

    def generate_kode(self, kategori):
        prefix = "SK" if kategori == "skincare" else "BD"
        existing = [int(k[2:]) for k in self.produk if k.startswith(prefix)]
        next_num = max(existing, default=0) + 1
        return f"{prefix}{str(next_num).zfill(3)}"

    def load_data(self):
        try:
            with open(self.CSV_FILE, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    kode = row['kode']
                    self.produk[kode] = {
                        'nama': row['nama'],
                        'kategori': row['kategori'],
                        'stok': int(row['stok']),
                        'harga': int(row['harga'])
                    }
        except FileNotFoundError:
            for kode, nama, kategori, stok, harga in produk_awal:
                self.produk[kode] = {
                    'nama': nama,
                    'kategori': kategori,
                    'stok': stok,
                    'harga': harga
                }
            self.simpan_data()

    def simpan_data(self):
        with open(self.CSV_FILE, mode='w', newline='') as file:
            fieldnames = ['kode', 'nama', 'kategori', 'stok', 'harga']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for kode, data in self.produk.items():
                row = {'kode': kode, **data}
                writer.writerow(row)

    def tambah_produk(self):
        kategori = safe_input("Kategori (skincare/bodycare): ").lower()
        if kategori not in ["skincare", "bodycare"]:
            print("Kategori tidak valid!")
            return
        kode = self.generate_kode(kategori)
        nama = safe_input("Nama produk: ")
        stok = int(safe_input("Stok awal: ") or 0)
        harga = int(safe_input("Harga: ") or 0)
        self.produk[kode] = {'nama': nama, 'kategori': kategori, 'stok': stok, 'harga': harga}
        self.simpan_data()
        print(f"Produk berhasil ditambahkan dengan kode {kode}.")

    def edit_produk(self):
        kode = safe_input("Masukkan kode produk yang ingin diedit: ")
        if kode not in self.produk:
            print("Produk tidak ditemukan.")
            return
        data = self.produk[kode]
        print(f"Data saat ini: Nama: {data['nama']}, Kategori: {data['kategori']}, Stok: {data['stok']}, Harga: {data['harga']}")
        pilihan = safe_input("Ubah (nama/stok/harga/kategori/semua): ").lower()
        if pilihan == "nama":
            data['nama'] = safe_input("Nama baru: ")
        elif pilihan == "stok":
            data['stok'] = int(safe_input("Stok baru: ") or data['stok'])
        elif pilihan == "harga":
            data['harga'] = int(safe_input("Harga baru: ") or data['harga'])
        elif pilihan == "kategori":
            data['kategori'] = safe_input("Kategori baru: ")
        elif pilihan == "semua":
            data['nama'] = safe_input("Nama baru: ")
            data['kategori'] = safe_input("Kategori baru: ")
            data['stok'] = int(safe_input("Stok baru: "))
            data['harga'] = int(safe_input("Harga baru: "))
        self.simpan_data()
        print("Produk berhasil diedit.")

    def hapus_produk(self):
        kode = safe_input("Masukkan kode produk yang ingin dihapus: ")
        if kode in self.produk:
            konfirmasi = safe_input(f"Apakah yakin ingin menghapus produk {self.produk[kode]['nama']}? (y/n): ").lower()
            if konfirmasi == 'y':
                del self.produk[kode]
                self.simpan_data()
                print("Produk berhasil dihapus.")
            else:
                print("Penghapusan dibatalkan.")
        else:
            print("Produk tidak ditemukan.")

    def transaksi_penjualan(self):
        print("Transaksi dimulai. Ketik 'selesai' untuk mengakhiri.")
        total_transaksi = []
        while True:
            kode = safe_input("Kode produk: ").strip().upper()
            if kode == 'SELESAI':
                break
            if kode not in self.produk:
                print("Kode produk tidak ditemukan.")
                continue
            jumlah = int(safe_input("Jumlah dibeli: ") or 0)
            if jumlah > self.produk[kode]['stok']:
                print("Stok tidak mencukupi.")
                continue
            self.produk[kode]['stok'] -= jumlah
            self.transaksi.append((kode, jumlah))
            total_transaksi.append((kode, jumlah, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            lanjut = safe_input("Tambah produk lain? (y/n): ").lower()
            if lanjut != 'y':
                break
        self.simpan_data()
        if total_transaksi:
            with open(self.TRANSAKSI_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                for item in total_transaksi:
                    writer.writerow([item[0], item[1], item[2]])
            print("Transaksi berhasil disimpan.")
        else:
            print("Tidak ada produk yang dibeli.")

    def restok_produk(self):
        print("\nRestok dimulai. Ketik 'selesai' untuk mengakhiri.")
        while True:
            kode = safe_input("Kode produk: ").strip().upper()
            if kode == 'SELESAI':
                break
            if kode not in self.produk:
                print("Kode produk tidak ditemukan.")
                continue
            jumlah = int(safe_input("Jumlah restok: ") or 0)
            self.produk[kode]['stok'] += jumlah
            self.restok_log.append((kode, jumlah))
            lanjut = safe_input("Restok produk lain? (y/n): ").lower()
            if lanjut != 'y':
                break
        self.simpan_data()
        print("Restok selesai.")

    def laporan_penjualan(self):
        try:
            with open(self.TRANSAKSI_FILE, mode='r') as file:
                reader = list(csv.reader(file))
                kategori = safe_input("Kategori laporan (semua/skincare/bodycare): ").lower()
                mode_waktu = safe_input("Pilih rentang waktu (semua/harian/mingguan/bulanan): ").lower()

                now = datetime.now()
                hari_ini = now.date()

                total = 0
                print("Laporan Penjualan:")
                for row in reader:
                    if len(row) == 3:
                        kode, jumlah, tanggal = row[0], int(row[1]), row[2]
                        try:
                            waktu_transaksi = datetime.strptime(tanggal, "%Y-%m-%d %H:%M:%S")
                            tanggal_transaksi = waktu_transaksi.date()
                        except:
                            continue
                    elif len(row) == 2:
                        kode, jumlah = row[0], int(row[1])
                        tanggal_transaksi = None
                        tanggal = "-"
                    else:
                        continue

                    if mode_waktu == "harian" and tanggal_transaksi != hari_ini:
                        continue
                    elif mode_waktu == "mingguan" and tanggal_transaksi and tanggal_transaksi < (hari_ini - timedelta(days=7)):
                        continue
                    elif mode_waktu == "bulanan" and tanggal_transaksi and tanggal_transaksi < (hari_ini - timedelta(days=30)):
                        continue

                    if kode in self.produk and (kategori == 'semua' or self.produk[kode]['kategori'] == kategori):
                        nama = self.produk[kode]['nama']
                        harga = self.produk[kode]['harga']
                        subtotal = harga * jumlah
                        print(f"{nama} x{jumlah} = Rp{subtotal} | Waktu: {tanggal}")
                        total += subtotal
                print(f"Total Penjualan: Rp{total}")
        except FileNotFoundError:
            print("Belum ada data transaksi.")

    def cari_produk(self):
        kata = safe_input("Masukkan kata kunci pencarian (nama/kategori): ").lower()
        hasil = False
        print("\nHasil Pencarian:")
        for kode, data in self.produk.items():
            if kata in data['nama'].lower() or kata in data['kategori'].lower():
                print(f"[{kode}] {data['nama']} ({data['kategori']}) - Rp{data['harga']} | Stok: {data['stok']}")
                hasil = True
        if not hasil:
            print("Tidak ada produk yang sesuai.")

    def lihat_produk(self):
        print("Pilih kategori produk yang ingin dilihat:")
        print("1. Semua Produk\n2. Skincare\n3. Bodycare")
        pilihan = safe_input("Masukkan pilihan (1/2/3): ")

        def tampilkan(kategori_filter=None):
            print("Daftar Produk Tersedia:")
            urut = sorted(self.produk.items(), key=lambda x: x[0])
            kategori_terakhir = None
            for kode, data in urut:
                if kategori_filter and data['kategori'] != kategori_filter:
                    continue
                if kategori_filter is None and data['kategori'] != kategori_terakhir:
                    print(f"-- {data['kategori'].upper()} --")
                    kategori_terakhir = data['kategori']
                print(f"[{kode}] {data['nama']} ({data['kategori']}) - Rp{data['harga']} | Stok: {data['stok']}")

        if pilihan == '1':
            tampilkan()
        elif pilihan == '2':
            tampilkan("skincare")
        elif pilihan == '3':
            tampilkan("bodycare")
        else:
            print("Pilihan tidak valid.")

    def notifikasi_stok_menipis(self):
        print("\n[NOTIFIKASI] Produk dengan stok menipis (<= 10):")
        ada = False
        for kode, data in self.produk.items():
            if data['stok'] <= 10:
                print(f"[{kode}] {data['nama']} | Stok: {data['stok']}")
                ada = True
        if not ada:
            print("Tidak ada produk dengan stok menipis.")

    def menu(self):
        self.notifikasi_stok_menipis()
        while True:
            print("""
===== SISTEM MANAJEMEN PRODUK KECANTIKAN =====
1. Lihat Produk Tersedia
2. Tambah Produk
3. Edit Produk
4. Hapus Produk
5. Transaksi Penjualan
6. Restok Produk
7. Laporan Penjualan
8. Cari Produk
0. Keluar
""")
            pilihan = safe_input("Pilih menu: ")
            if pilihan == '1':
                self.lihat_produk()
            elif pilihan == '2':
                self.tambah_produk()
            elif pilihan == '3':
                self.edit_produk()
            elif pilihan == '4':
                self.hapus_produk()
            elif pilihan == '5':
                self.transaksi_penjualan()
            elif pilihan == '6':
                self.restok_produk()
            elif pilihan == '7':
                self.laporan_penjualan()
            elif pilihan == '8':
                self.cari_produk()
            elif pilihan == '0':
                print("Keluar dari aplikasi. Sampai jumpa!")
                break
            else:
                print("Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    app = ProdukKecantikan()
    app.menu()
