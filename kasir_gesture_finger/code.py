# =========================================================
# Blueberry Breeze Gesture Cashier
# FINAL VERSION — CAMERA ALWAYS ON TOP + STEP MODE
# FIXED: FINGER 4 NOT DETECTED AS 5 ANYMORE
# + MIRROR MODE (TANGAN KANAN → KANAN LAYAR)
# =========================================================

import cv2
import mediapipe as mp
import threading
import time
from datetime import datetime


# =========================================================
# GESTURE DETECTOR — ALWAYS ON CAMERA WINDOW
# =========================================================
class GestureDetector(threading.Thread):
    def __init__(self, cam_idx=0):
        super().__init__()
        self.daemon = True

        self.cap = cv2.VideoCapture(cam_idx)
        self.running = False

        # MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.latest = None
        self.hand_detected = False

    def run(self):
        self.running = True

        cv2.namedWindow("Gesture Camera", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Gesture Camera", cv2.WND_PROP_TOPMOST, 1)

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Proses deteksi pakai frame asli (tidak di-flip)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            self.hand_detected = bool(result.multi_hand_landmarks)
            count = None

            if result.multi_hand_landmarks:
                for hand in result.multi_hand_landmarks:
                    # Gambar landmark di frame asli dulu
                    self.mp_draw.draw_landmarks(
                        frame, hand, self.mp_hands.HAND_CONNECTIONS)

                    count = self.count_fingers(hand)

            self.latest = count

            # Tulis teks di frame asli
            cv2.putText(frame, f"Fingers: {count}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # ==============================
            # MIRROR MODE UNTUK TAMPILAN
            # ==============================
            display = cv2.flip(frame, 1)  # Tampilan seperti kaca

            cv2.imshow("Gesture Camera", display)

            key = cv2.waitKey(1)
            if key == ord('q'):
                self.stop()
                break

            time.sleep(0.002)

        self.cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False

    def get(self):
        return self.latest

    # =========================================================
    # FINGER DETECTOR — FIXED VERSION (4 vs 5 JARI)
    # =========================================================
    def count_fingers(self, hand):
        lm = hand.landmark

        # ------------ Deteksi 4 jari selain jempol ------------
        tips = [8, 12, 16, 20]   # fingertip index, middle, ring, pinky
        fingers = 0

        for tip in tips:
            pip = tip - 2  # joint below tip
            if lm[tip].y < lm[pip].y:
                fingers += 1

        # ------------ Deteksi Jempol ------------
        # Estimasi orientasi tangan (kanan atau kiri)
        is_right = lm[17].x < lm[5].x

        if is_right:
            thumb_open = lm[4].x > lm[2].x   # jempol ke kanan (tangan kanan)
        else:
            thumb_open = lm[4].x < lm[2].x   # jempol ke kiri (tangan kiri)

        # Jika jempol terbuka → tambah 1 jari
        if thumb_open:
            return fingers + 1

        return fingers


# =========================================================
# READY MODE — 0 JARI STABIL 0.4 DETIK
# =========================================================
def wait_ready():
    print("\n✊ Kepalkan tangan (0 jari) untuk melanjutkan langkah...")

    stable_start = None

    while True:
        g = detector.get()

        if not detector.hand_detected:
            stable_start = None
            time.sleep(0.01)
            continue

        if g == 0:
            if stable_start is None:
                stable_start = time.time()
            elif time.time() - stable_start >= 0.4:
                print("> READY! Silakan lakukan gesture berikutnya.")
                time.sleep(0.25)
                return
        else:
            stable_start = None

        time.sleep(0.01)


# =========================================================
# GESTURE INPUT (SETELAH READY)
# =========================================================
def wait_gesture(allowed, message):
    wait_ready()
    print(message)

    last = None
    while True:
        g = detector.get()

        if detector.hand_detected and g in allowed:
            if g != last:
                print(f"> Gesture diterima: {g}")
                time.sleep(0.25)
                return g

        last = g
        time.sleep(0.01)


def wait_quantity(message):
    return wait_gesture([1, 2, 3, 4, 5], message)


# =========================================================
# PROGRAM KASIR BERTAHAP
# =========================================================
def main():
    global detector
    detector = GestureDetector()
    detector.start()
    time.sleep(0.5)

    print("\n                 BLUEBERRY BREEZE                  ")
    print("===================================================")

    nama = input("Nama Pelanggan: ")
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    menu = {
        1: ("Blueberry Cloud Latte", 28000),
        2: ("Lemon Ice Sparkle", 22000),
        3: ("Mini Pancake Bites", 25000),
        4: ("Choco Lava Slice", 30000),
        5: ("Creamy Carbonara Bowl", 35000)
    }

    pesanan = []

    def show_menu():
        print("\n================ MENU ================")
        for k, v in menu.items():
            print(f"{k}. {v[0]:25} | Rp{v[1]:,}")
        print("=====================================")

    # ====================== PILIH MENU AWAL ======================
    show_menu()

    pilih = wait_gesture(
        [1, 2, 3, 4, 5],
        "Tunjukkan 1–5 jari untuk memilih menu pertama:"
    )

    jumlah = wait_quantity("Tunjukkan jumlah pembelian (1–5 jari):")

    for _ in range(jumlah):
        pesanan.append({"menu": pilih, "harga": menu[pilih][1]})

    print(f"➡ {jumlah} x {menu[pilih][0]} ditambahkan.")

    # ====================== LOOP AKSI ======================
    while True:
        total = len(pesanan)
        bayar = sum(p["harga"] for p in pesanan)

        print("\n=============== RINGKASAN ===============")
        print(f"Total Item       : {total}")
        print(f"Total Pembayaran : Rp{bayar:,}")
        print("----------------------------------------")
        print("Aksi (1=Tambah | 2=Kurangi | 5=Selesai)")

        aksi = wait_gesture([1, 2, 5],
                            "Tunjukkan gesture aksi (1/2/5):"
                            )

        # ====================== TAMBAH ======================
        if aksi == 1:
            show_menu()

            pilih2 = wait_gesture(
                [1, 2, 3, 4, 5],
                "Tunjukkan menu yang ingin ditambah:"
            )

            jumlah2 = wait_quantity("Tunjukkan jumlah tambahan (1–5 jari):")

            for _ in range(jumlah2):
                pesanan.append({"menu": pilih2, "harga": menu[pilih2][1]})

            print(f"➡ Ditambah: {jumlah2} x {menu[pilih2][0]}")

        # ====================== KURANGI ======================
        elif aksi == 2:
            counted = {}
            for p in pesanan:
                counted[p["menu"]] = counted.get(p["menu"], 0) + 1

            print("\nPesanan saat ini:")
            for m, j in counted.items():
                print(f"{m}. {menu[m][0]} x{j}")

            target = wait_gesture(
                [1, 2, 3, 4, 5],
                "Tunjukkan menu yang ingin dikurangi:"
            )

            jumlah_kurang = wait_quantity("Tunjukkan jumlah yang dikurangi:")

            removed = 0
            for item in pesanan[:]:
                if item["menu"] == target and removed < jumlah_kurang:
                    pesanan.remove(item)
                    removed += 1

            print("➡ Pesanan dikurangi!")

        # ====================== SELESAI ======================
        elif aksi == 5:
            print("\nTransaksi selesai! Mencetak struk...")
            break

    # ====================== CETAK STRUK ======================
    print("\n===================== STRUK PEMBELIAN =====================")
    print(f"Nama Pelanggan   : {nama}")
    print(f"Waktu Pembelian  : {waktu}")
    print("------------------------------------------------------------")

    detail = {}
    for p in pesanan:
        detail.setdefault(p["menu"], {"harga": p["harga"], "jumlah": 0})
        detail[p["menu"]]["jumlah"] += 1

    for m, d in detail.items():
        subtotal = d["harga"] * d["jumlah"]
        print(f"- {menu[m][0]} x{d['jumlah']} = Rp{subtotal:,}")

    print("------------------------------------------------------------")
    print(f"TOTAL PEMBAYARAN : Rp{sum(p['harga'] for p in pesanan):,}")
    print("============================================================")
    print(" TERIMA KASIH TELAH BELANJA DI BLUEBERRY BREEZE ❤️ ")

    detector.stop()


# =========================================================
# RUN PROGRAM
# =========================================================
if __name__ == "__main__":
    main()