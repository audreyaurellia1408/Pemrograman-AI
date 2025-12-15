print("Calculator Python")

# ==============================
# LOGIC
# ==============================
def penjumlahan(x, y):
    return x + y

def pengurangan(x, y):
    return x - y

def perkalian(x, y):
    return x * y

def pembagian(x, y):
    return x / y


# ==============================
# PROGRAM UTAMA
# ==============================
while True:
    print("----------------")
    print("1. Penjumlahan")
    print("2. Pengurangan")
    print("3. Perkalian")
    print("4. Pembagian")
    print("----------------")

    tipe = input("Silakan masukkan nomor yang kalian pilih : ")

    if tipe in ('1', '2', '3', '4'):
        angka1 = float(input("Angka pertama : "))
        angka2 = float(input("Angka kedua   : "))
        print("----------------")

        if tipe == '1':
            print("Jawabannya adalah :", penjumlahan(angka1, angka2))
        elif tipe == '2':
            print("Jawabannya adalah :", pengurangan(angka1, angka2))
        elif tipe == '3':
            print("Jawabannya adalah :", perkalian(angka1, angka2))
        elif tipe == '4':
            if angka2 == 0:
                print("Error: tidak bisa dibagi dengan 0")
            else:
                print("Jawabannya adalah :", pembagian(angka1, angka2))
    else:
        print("Pilihan tidak valid!")

    print("----------------")
    ulang = input("Mau lagi? (y = mau lagi / n = cukup): ").lower()

    if ulang == 'n':
        print("Terima kasih, program selesai.")
        break
