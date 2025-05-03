import json
import os
from datetime import datetime

FILE_PATH = 'data_barang.json'

# Load data
def load_data():
    if os.path.exists(FILE_PATH):
        if os.stat(FILE_PATH).st_size == 0:  # Cek apakah file kosong
            return {}
        with open(FILE_PATH, 'r') as f:
            return json.load(f)
    return {}


# Simpan data
def save_data(data):
    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# Login
def login():
    user = input("Masukkan username (admin/staff): ").strip()
    if user == "admin":
        password = input("Password admin: ")
        if password == "admin123":
            return "admin"
    elif user == "staff":
        return "staff"
    print("Login gagal.")
    return None

# Tambah barang baru
def tambah_barang(data):
    kode = input("Kode barang: ")
    if kode in data:
        print("Barang sudah ada.")
        return
    nama = input("Nama barang: ")
    qty = int(input("Stok awal: "))
    harga = float(input("Harga: "))
    data[kode] = {
        "nama": nama,
        "harga": harga,
        "stok": [{"jumlah": qty, "tanggal": datetime.now().isoformat()}]
    }
    print("Barang ditambahkan.")

# Tambah stok (FIFO: disimpan per batch)
def tambah_stok(data):
    kode = input("Kode barang: ")
    if kode not in data:
        print("Barang tidak ditemukan.")
        return
    qty = int(input("Jumlah tambahan: "))
    data[kode]["stok"].append({
        "jumlah": qty,
        "tanggal": datetime.now().isoformat()
    })
    print("Stok ditambahkan.")

# Kurangi stok sesuai FIFO
def kurangi_stok(data):
    kode = input("Kode barang: ")
    if kode not in data:
        print("Barang tidak ditemukan.")
        return
    total = int(input("Jumlah yang ingin dikeluarkan: "))
    stok_list = data[kode]["stok"]
    i = 0
    while total > 0 and i < len(stok_list):
        if stok_list[i]["jumlah"] <= total:
            total -= stok_list[i]["jumlah"]
            stok_list.pop(i)
        else:
            stok_list[i]["jumlah"] -= total
            total = 0
    if total > 0:
        print("Stok tidak mencukupi!")
    else:
        print("Stok berhasil dikurangi.")

# Lihat semua stok
def lihat_stok(data):
    if not data:
        print("Belum ada data.")
    else:
        for kode, info in data.items():
            total = sum(batch["jumlah"] for batch in info["stok"])
            print(f"{kode} - {info['nama']} | Total Stok: {total} | Harga: {info['harga']}")
            for batch in info["stok"]:
                print(f"    - {batch['jumlah']} unit pada {batch['tanggal']}")

# Edit barang
def edit_barang(data):
    kode = input("Masukkan kode barang: ")
    if kode in data:
        nama = input("Nama baru: ")
        data[kode]["nama"] = nama
        print("Nama barang diperbarui.")
    else:
        print("Barang tidak ditemukan.")

# Edit harga
def edit_harga(data):
    kode = input("Kode barang: ")
    if kode in data:
        harga = float(input("Harga baru: "))
        data[kode]["harga"] = harga
        print("Harga diperbarui.")
    else:
        print("Barang tidak ditemukan.")

# Hapus barang
def hapus_barang(data):
    kode = input("Kode barang: ")
    if kode in data:
        del data[kode]
        print("Barang dihapus.")
    else:
        print("Barang tidak ditemukan.")

# Cari barang
def cari_barang(data):
    keyword = input("Nama/kode barang: ").lower()
    found = False
    for kode, info in data.items():
        if keyword in kode.lower() or keyword in info["nama"].lower():
            total = sum(batch["jumlah"] for batch in info["stok"])
            print(f"{kode} - {info['nama']} | Total Stok: {total} | Harga: {info['harga']}")
            found = True
    if not found:
        print("Barang tidak ditemukan.")

# Menu
def main():
    data = load_data()
    role = login()
    if not role:
        return

    while True:
        print("\n=== Sistem Inventori FIFO ===")
        print("1. Tambah Barang")
        print("2. Tambah Stok Barang")
        print("3. Kurangi Stok Barang")
        print("4. Lihat Stok Barang")
        print("5. Edit Barang" if role == "admin" else "5. (Tidak tersedia)")
        print("6. Edit Harga" if role == "admin" else "6. (Tidak tersedia)")
        print("7. Hapus Barang" if role == "admin" else "7. (Tidak tersedia)")
        print("8. Cari Barang")
        print("9. Keluar")

        pilihan = input("Pilih menu (1-9): ")

        if pilihan == "1" and role == "admin":
            tambah_barang(data)
        elif pilihan == "2":
            tambah_stok(data)
        elif pilihan == "3":
            kurangi_stok(data)
        elif pilihan == "4":
            lihat_stok(data)
        elif pilihan == "5" and role == "admin":
            edit_barang(data)
        elif pilihan == "6" and role == "admin":
            edit_harga(data)
        elif pilihan == "7" and role == "admin":
            hapus_barang(data)
        elif pilihan == "8":
            cari_barang(data)
        elif pilihan == "9":
            save_data(data)
            print("Data disimpan. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid atau tidak tersedia.")

if __name__ == "__main__":
    main()
