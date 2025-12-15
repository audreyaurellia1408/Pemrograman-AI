print("Selamat Datang")

# Input Awalan
nama_pembeli = input("Masukkan Nama Lengkap anda : ")
no_hp = input("Masukkan No. Handphone anda : ")
gender = input("Jenis Kelamin [Pria/Wanita] : ")

# Maksimal pembelian adalah 3
while True:
    belibarang = int(input("Banyaknya Pembelian Barang (max.3) : "))
    if belibarang <= 3:
        break
    print("⛔ Maksimal pembelian hanya 3! Masukkan lagi.")

# List Data
list_nama_barang = []
list_harga = []
list_ukuran = []
list_jumlah_beli = []
list_subtotal = []


# Fungsi List Barang Pria
def bajuPria():
    print("Product baju pria")
    print("1. Jas              - 1.500.000")
    print("2. Kemeja           - 100.000")
    print("3. Kemeja Denim     - 150.000")
    print("4. Batik            - 150.000")
    print("5. Baju Koko        - 100.000")
    print("6. Kaos Polos       - 50.000")
    print("7. Rompi            - 150.000")
    print("8. Jaket Parka      - 200.000")
    print("9. Jaket Kulit      - 400.000")
    print("10. Jaket Windproof - 850.000")
    print()


# Fungsi List Barang Wanita
def bajuWanita():
    print("Product baju wanita")
    print("1. Dress Pesta   - 500.000")
    print("2. Kemeja        - 150.000")
    print("3. Gamis         - 110.000")
    print("4. Daster        - 85.000")
    print("5. T-Shirt       - 75.000")
    print("6. Cardigan      - 50.000")
    print("7. Blazer        - 100.000")
    print("8. Blouse        - 120.000")
    print("9. Jumpsuit      - 170.000")
    print("10. Piyama       - 135.000")
    print()


# Harga pria
harga_barang_pria = {
    "1": ("Jas", 1500000),
    "2": ("Kemeja", 100000),
    "3": ("Kemeja Denim", 150000),
    "4": ("Batik", 150000),
    "5": ("Baju Koko", 100000),
    "6": ("Kaos Polos", 50000),
    "7": ("Rompi", 150000),
    "8": ("Jaket Parka", 200000),
    "9": ("Jaket Kulit", 400000),
    "10": ("Jaket Windproof", 850000)
}

# Harga wanita
harga_barang_wanita = {
    "1": ("Dress Pesta", 500000),
    "2": ("Kemeja", 150000),
    "3": ("Gamis", 110000),
    "4": ("Daster", 85000),
    "5": ("T-Shirt", 75000),
    "6": ("Cardigan", 50000),
    "7": ("Blazer", 100000),
    "8": ("Blouse", 120000),
    "9": ("Jumpsuit", 170000),
    "10": ("Piyama", 135000)
}


# ================= LOOP PEMBELIAN ===================
print()

for i in range(belibarang):
    print(f"Pembelian barang ke-{i+1}")

    # Pilihan daftar barang
    if gender.lower() in ["pria", "male", "cowo", "laki laki"]:
        bajuPria()
        pilihan_baju = input("Masukkan Pilihan Baju [1 ~ 10] : ")

        # Validasi pilihan
        if pilihan_baju not in harga_barang_pria:
            print("⛔ Pesanan tidak valid, pilih 1–10!")
            continue

        ukuran_baju = input("Ukuran [S/M/L/XL] : ")
        if ukuran_baju.upper() not in ["S", "M", "L", "XL"]:
            print("Ukuran tidak diketahui, diset '-' ")
            ukuran_baju = "-"

        list_ukuran.append(ukuran_baju.upper())

        jumlah_beli = int(input("Mau beli berapa? : "))
        list_jumlah_beli.append(jumlah_beli)

        # ✔ FIX DI SINI (yang error sebelumnya)
        nama, harga = harga_barang_pria[pilihan_baju]

        list_nama_barang.append(nama)
        list_harga.append(harga)
        list_subtotal.append(harga * jumlah_beli)

    elif gender.lower() in ["wanita", "female", "cewe", "perempuan"]:
        bajuWanita()
        pilihan_baju = input("Masukkan Pilihan Baju [1 ~ 10] : ")

        # Validasi pilihan
        if pilihan_baju not in harga_barang_wanita:
            print("⛔ Pesanan tidak valid, pilih 1–10!")
            continue

        ukuran_baju = input("Ukuran [S/M/L/XL] : ")
        if ukuran_baju.upper() not in ["S", "M", "L", "XL"]:
            print("Ukuran tidak diketahui, diset '-' ")
            ukuran_baju = "-"

        list_ukuran.append(ukuran_baju.upper())

        jumlah_beli = int(input("Mau beli berapa? : "))
        list_jumlah_beli.append(jumlah_beli)

        nama, harga = harga_barang_wanita[pilihan_baju]
        list_nama_barang.append(nama)
        list_harga.append(harga)
        list_subtotal.append(harga * jumlah_beli)

    else:
        print("Jenis kelamin tidak valid.")
        break

# ================== STRUK ====================

print()
print("=" * 70)
print("                          Program Toko Baju")
print("                             Kelompok 8")
print("=" * 70)
print()

print(f"Nama Pembeli : {nama_pembeli}")
print(f"No. HP       : {no_hp}")
print()

print("Daftar Belanjaan :")
print("=" * 100)
print("{:<30} {:<10} {:>8} {:>12} {:>15}".format(
    "Nama Barang", "Ukuran", "Jumlah", "Harga", "Subtotal"))
print("=" * 100)

for i in range(len(list_nama_barang)):
    print("{:<30} {:<10} {:>8} {:>12} {:>15}".format(
        list_nama_barang[i],
        list_ukuran[i],
        list_jumlah_beli[i],
        list_harga[i],
        list_subtotal[i]
    ))

print("-" * 100)

Total = sum(list_subtotal)
print(f"Total Belanja : Rp{Total:,}".replace(",", "."))

# Diskon
if Total >= 500000:
    print("\nSelamat! Anda Mendapatkan Diskon 25%")
    diskon = Total * 25 / 100
else:
    diskon = 0

jumlah_bayar = Total - diskon
print(f"Total Akhir  : Rp{jumlah_bayar:,}".replace(",", "."))
print("-" * 70)

# Pembayaran
Ubyr = int(input("Bayar : Rp"))
uangkembalian = Ubyr - jumlah_bayar
print("\nUang Kembalian : Rp", uangkembalian)

print("\nTerima Kasih sudah belanja :)")
