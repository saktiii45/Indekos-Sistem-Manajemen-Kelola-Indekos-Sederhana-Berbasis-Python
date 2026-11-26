import pandas as pd   # library pandas untuk membaca, menulis, dan menampilkan CSV
import os             # untuk membersihkan layar terminal (cls/clear)

# =====================================================================
# BAGIAN 1: PENGATURAN DAN DATA AWAL
# =====================================================================

PEMISAH_CSV = ','

# Daftar semua tabel (satu tabel = satu file CSV).
DAFTAR_TABEL = ['profil', 'kamar', 'reservasi', 'pembayaran', 'tata_tertib']

# Nama kolom tiap tabel. Kolom 'id' tidak ditulis di sini
KOLOM_TABEL = {
    # peran berisi 'admin' atau 'penghuni' (dipakai untuk filtering)
    'profil': ['username', 'password', 'nama', 'no_hp', 'peran'],
    # kode = kode unik kamar (dibuat otomatis), nomor = nomor kamar (tidak boleh dobel)
    'kamar': ['kode', 'nomor', 'tipe', 'harga', 'status'],
    # penghuni_id = id dari tabel profil, kode_kamar = kode dari tabel kamar
    'reservasi': ['penghuni_id', 'kode_kamar', 'tgl_masuk', 'durasi_bulan', 'total_bayar', 'status'],
    'pembayaran': ['reservasi_id', 'nominal', 'tanggal', 'status'],
}

# Kolom yang isinya ANGKA. Dipakai saat membaca file CSV supaya kolom ini diubah dari teks menjadi int.
KOLOM_ANGKA_CSV = ['id', 'harga', 'durasi_bulan', 'total_bayar',
                   'nominal', 'reservasi_id', 'penghuni_id']

# Status reservasi yang boleh dipakai
STATUS_RESERVASI = ['menunggu', 'aktif', 'selesai', 'batal']

# Data bawaan yang dipakai jika file CSV belum ada
DATA_AWAL_KOST = {
    'profil': [
        {'id': 1, 'username': 'admin', 'password': 'admin123',
         'nama': 'Administrator', 'no_hp': '-', 'peran': 'admin'}
    ],
    'kamar': [
        {'id': 1, 'kode': 'KMR001', 'nomor': 'A1', 'tipe': 'Standar', 'harga': 600000, 'status': 'tersedia'},
        {'id': 2, 'kode': 'KMR002', 'nomor': 'A2', 'tipe': 'Standar', 'harga': 600000, 'status': 'tersedia'},
        {'id': 3, 'kode': 'KMR003', 'nomor': 'B1', 'tipe': 'Deluxe', 'harga': 900000, 'status': 'tersedia'},
    ],
    'reservasi': [],
    'pembayaran': [],
    'tata_tertib': [
        'Jam malam pukul 22.00 WIB.',
        'Dilarang membawa tamu lawan jenis ke dalam kamar.',
        'Jaga kebersihan kamar dan area bersama.',
        'Pembayaran paling lambat tanggal 10 setiap bulan.',
        'Dilarang merokok di dalam kamar.',
        'Dilarang mengganggu kenyamanan penghuni lain.',
    ],
}


# =====================================================================
# BAGIAN 2: MEMBACA DAN MENYIMPAN FILE CSV
# =====================================================================

def muat_data():
    """Membaca semua file CSV memakai pandas, lalu mengembalikan datanya."""
    data_hasil = {}

    for nama_tabel in DAFTAR_TABEL:
        nama_file_csv = 'kost_' + nama_tabel + '.csv'

        # Mode 'a' membuat file kosong jika file belum ada (jadi tanpa try/except)
        file_csv = open(nama_file_csv, 'a', encoding='utf-8')
        file_csv.close()

        # Cek apakah file masih kosong
        file_csv = open(nama_file_csv, 'r', encoding='utf-8')
        isi_file = file_csv.read()
        file_csv.close()

        if isi_file == '':
            # File masih kosong -> pakai data bawaan
            data_hasil[nama_tabel] = DATA_AWAL_KOST[nama_tabel]
        else:
            # dtype=str : semua kolom dibaca sebagai teks dulu, supaya password
            #             atau no_hp seperti 0123 tidak berubah menjadi angka 123.
            tabel_pandas = pd.read_csv(nama_file_csv, sep=PEMISAH_CSV,
                                       dtype=str, keep_default_na=False)

            if nama_tabel == 'tata_tertib':
                # Tata tertib hanya satu kolom 'aturan' -> jadikan list teks
                data_hasil[nama_tabel] = tabel_pandas['aturan'].tolist()
            else:
                # Kolom yang berisi angka diubah dari teks menjadi int
                for nama_kolom in KOLOM_ANGKA_CSV:
                    if nama_kolom in tabel_pandas.columns:
                        tabel_pandas[nama_kolom] = tabel_pandas[nama_kolom].astype(int)
                # Setiap baris tabel menjadi satu dictionary
                data_hasil[nama_tabel] = tabel_pandas.to_dict('records')

    return data_hasil


def simpan_data():
    """Menulis semua data (variabel data_kost) ke file CSV memakai pandas."""
    for nama_tabel in DAFTAR_TABEL:
        nama_file_csv = 'kost_' + nama_tabel + '.csv'

        if nama_tabel == 'tata_tertib':
            tabel_pandas = pd.DataFrame({'aturan': data_kost[nama_tabel]})
        else:
            daftar_kolom = ['id'] + KOLOM_TABEL[nama_tabel]
            tabel_pandas = pd.DataFrame(data_kost[nama_tabel], columns=daftar_kolom)

        # index=False : nomor baris bawaan pandas tidak ikut ditulis ke file
        tabel_pandas.to_csv(nama_file_csv, sep=PEMISAH_CSV, index=False, encoding='utf-8')


# Variabel utama yang menyimpan semua data selama program berjalan
data_kost = muat_data()
simpan_data()   


# =====================================================================
# BAGIAN 3: ALAT BANTU (fungsi kecil yang dipakai berulang-ulang)
# =====================================================================

def bersihkan_layar():
    """Membersihkan layar terminal: 'cls' untuk Windows, 'clear' untuk Linux/Mac."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def jeda():
    """Menahan layar supaya hasil bisa dibaca. Setelah Enter, layar dibersihkan oleh menu."""
    input('\n  Tekan Enter untuk lanjut...')


def format_rupiah(angka):
    """Contoh: 1800000 -> Rp 1.800.000"""
    teks_angka = '{:,}'.format(angka)      
    teks_angka = teks_angka.replace(',', '.')
    return 'Rp ' + teks_angka


def minta_teks(pertanyaan, nilai_lama=None):
    """
    Meminta input teks dari pengguna.
    - Jika nilai_lama tidak diisi : input tidak boleh kosong.
    - Jika nilai_lama diisi       : menekan Enter berarti memakai nilai lama.
    """
    while True:
        isi_input = input('  ' + pertanyaan + ': ').strip()
        if PEMISAH_CSV in isi_input:
            print('  Tidak boleh memakai tanda koma (,).')
        elif isi_input == '' and nilai_lama is None:
            print('  Tidak boleh kosong.')
        elif isi_input == '':
            return nilai_lama
        else:
            return isi_input


def minta_angka(pertanyaan, nilai_lama=None):
    """Sama seperti minta_teks, tetapi isinya harus angka bulat lebih dari 0."""
    while True:
        isi_input = input('  ' + pertanyaan + ': ').strip()
        if isi_input == '' and nilai_lama is not None:
            return nilai_lama
        if not isi_input.isdigit():
            print('  Masukkan angka bulat positif.')
        elif int(isi_input) == 0:
            print('  Angka harus lebih dari 0.')
        else:
            return int(isi_input)


def minta_status_reservasi(nilai_lama):
    """Meminta status reservasi. Enter = pakai nilai_lama."""
    while True:
        isi_input = input('  status (menunggu/aktif/selesai/batal) [' + nilai_lama + ']: ').strip().lower()
        if isi_input == '':
            return nilai_lama
        if isi_input in STATUS_RESERVASI:
            return isi_input
        print('  Status tidak valid.')


def cari_by_id(nama_tabel, id_dicari):
    """Mencari satu baris berdasarkan id. Hasil: dictionary, atau None jika tidak ada."""
    for data_baris in data_kost[nama_tabel]:
        if data_baris['id'] == id_dicari:
            return data_baris
    return None


def buat_id_baru(nama_tabel):
    """id baru = id terbesar yang ada + 1"""
    id_terbesar = 0
    for data_baris in data_kost[nama_tabel]:
        if data_baris['id'] > id_terbesar:
            id_terbesar = data_baris['id']
    return id_terbesar + 1


def filter_profil(peran):
    """Filtering tabel profil: ambil hanya yang perannya 'admin' atau 'penghuni'."""
    daftar_hasil = []
    for data_profil in data_kost['profil']:
        if data_profil['peran'] == peran:
            daftar_hasil.append(data_profil)
    return daftar_hasil


def cari_kamar_by_kode(kode_kamar):
    for data_kamar in data_kost['kamar']:
        if data_kamar['kode'] == kode_kamar:
            return data_kamar
    return None


def cari_nama_penghuni(penghuni_id):
    data_profil = cari_by_id('profil', penghuni_id)
    if data_profil is None:
        return '-'
    return data_profil['nama']


def username_dobel(username_cek, id_sendiri):
    """True jika username sudah dipakai profil lain (id_sendiri tidak dihitung)."""
    for data_profil in data_kost['profil']:
        if data_profil['username'] == username_cek and data_profil['id'] != id_sendiri:
            return True
    return False


def nomor_kamar_dobel(nomor_cek, id_sendiri):
    """True jika nomor kamar sudah dipakai kamar lain (id_sendiri tidak dihitung)."""
    for data_kamar in data_kost['kamar']:
        if data_kamar['nomor'] == nomor_cek and data_kamar['id'] != id_sendiri:
            return True
    return False


def buat_kode_kamar():
    """
    Membuat kode kamar unik: KMR001, KMR002, KMR003, ...
    Angka terakhir dicari dari kode yang ada, lalu ditambah 1.
    """
    angka_terbesar = 0
    for data_kamar in data_kost['kamar']:
        angka_kode = int(data_kamar['kode'][3:])   # 'KMR003' -> ambil '003' -> 3
        if angka_kode > angka_terbesar:
            angka_terbesar = angka_kode
    angka_baru = angka_terbesar + 1
    return 'KMR' + str(angka_baru).zfill(3)        # zfill(3): 4 -> '004'


# =====================================================================
# BAGIAN 4: ATURAN RESERVASI DAN TOTAL BAYAR
# =====================================================================

def hitung_total_bayar(kode_kamar, durasi_bulan):
    """
    Total bayar = harga kamar per bulan x durasi (bulan).
    Totalnya disimpan di data reservasi, jadi kalau harga kamar berubah
    di kemudian hari, total reservasi lama tidak ikut berubah.
    """
    data_kamar = cari_kamar_by_kode(kode_kamar)
    if data_kamar is None:
        return 0
    return data_kamar['harga'] * durasi_bulan


def hitung_sudah_dibayar(reservasi_id):
    """Menjumlahkan semua pembayaran milik satu reservasi."""
    jumlah = 0
    for data_pembayaran in data_kost['pembayaran']:
        if data_pembayaran['reservasi_id'] == reservasi_id:
            jumlah = jumlah + data_pembayaran['nominal']
    return jumlah


def cek_reservasi(data_cek, id_sendiri):
    """
    Memeriksa sebuah reservasi sebelum disimpan:
      1. penghuninya harus terdaftar
      2. kode kamarnya harus ada
      3. kamarnya belum dipesan reservasi lain
      4. total bayar tidak boleh lebih kecil dari yang sudah dibayar
    Hasil: True jika boleh disimpan, False jika tidak.
    id_sendiri = id reservasi yang sedang diubah (0 jika reservasi baru).
    """
    # 1. Cek penghuni (harus ada di tabel profil dan perannya penghuni)
    data_profil = cari_by_id('profil', data_cek['penghuni_id'])
    if data_profil is None or data_profil['peran'] != 'penghuni':
        print('  ID penghuni tidak ditemukan.')
        return False

    # 2. Cek kamar
    if cari_kamar_by_kode(data_cek['kode_kamar']) is None:
        print('  Kode kamar tidak ditemukan.')
        return False

    # 3. Cek apakah kamar sudah dipesan reservasi lain
    if data_cek['status'] == 'menunggu' or data_cek['status'] == 'aktif':
        for reservasi_lain in data_kost['reservasi']:
            bukan_diri_sendiri = (reservasi_lain['id'] != id_sendiri)
            kamar_sama = (reservasi_lain['kode_kamar'] == data_cek['kode_kamar'])
            if bukan_diri_sendiri and kamar_sama:
                if reservasi_lain['status'] == 'menunggu' or reservasi_lain['status'] == 'aktif':
                    print('  Kamar sudah dipesan/ditempati.')
                    return False

    # 4. Cek total bayar terhadap pembayaran yang sudah masuk
    if data_cek['total_bayar'] < hitung_sudah_dibayar(id_sendiri):
        print('  Total bayar baru lebih kecil dari pembayaran yang sudah masuk.')
        return False

    return True


def perbarui_status_kamar():
    """
    Menyesuaikan status kamar dengan data reservasi:
    kamar yang punya reservasi 'menunggu' atau 'aktif' -> 'terisi', selain itu 'tersedia'.
    """
    # Langkah 1: anggap semua kamar tersedia
    for data_kamar in data_kost['kamar']:
        data_kamar['status'] = 'tersedia'

    # Langkah 2: tandai kamar yang sedang dipakai reservasi
    for data_reservasi in data_kost['reservasi']:
        if data_reservasi['status'] == 'menunggu' or data_reservasi['status'] == 'aktif':
            data_kamar = cari_kamar_by_kode(data_reservasi['kode_kamar'])
            if data_kamar is not None:
                data_kamar['status'] = 'terisi'


def perbarui_status_pembayaran(reservasi_id):
    """
    Status pembayaran diisi otomatis: pembayaran yang membuat total terkumpul
    mencapai total bayar -> 'lunas', pembayaran sebelumnya -> 'cicilan'.
    """
    data_reservasi = cari_by_id('reservasi', reservasi_id)
    if data_reservasi is None:
        return

    jumlah_terkumpul = 0
    for data_pembayaran in data_kost['pembayaran']:
        if data_pembayaran['reservasi_id'] == reservasi_id:
            jumlah_terkumpul = jumlah_terkumpul + data_pembayaran['nominal']
            if data_pembayaran['nominal'] == 0:
                data_pembayaran['status'] = 'belum bayar'   # tagihan awal, belum ada uang masuk
            elif jumlah_terkumpul >= data_reservasi['total_bayar']:
                data_pembayaran['status'] = 'lunas'
            else:
                data_pembayaran['status'] = 'cicilan'


def buat_tagihan_awal(data_reservasi):
    """
    Dipanggil setelah reservasi dibuat.
    - status 'menunggu'  -> otomatis dibuatkan satu baris di tabel pembayaran
                            (nominal 0, status 'belum bayar') sebagai tagihan awal.
    - status selain itu  -> hanya tersimpan di tabel reservasi.
    """
    if data_reservasi['status'] != 'menunggu':
        return
    data_tagihan = {
        'id': buat_id_baru('pembayaran'),
        'reservasi_id': data_reservasi['id'],
        'nominal': 0,
        'tanggal': '-',
        'status': 'belum bayar',
    }
    data_kost['pembayaran'].append(data_tagihan)


def tampilkan_detail_reservasi(data_reservasi):
    """Menampilkan informasi lengkap satu reservasi, termasuk total bayar dan sisanya."""
    data_kamar = cari_kamar_by_kode(data_reservasi['kode_kamar'])
    sudah_dibayar = hitung_sudah_dibayar(data_reservasi['id'])
    sisa_tagihan = data_reservasi['total_bayar'] - sudah_dibayar

    print('\n=== DETAIL RESERVASI ===')
    print('  ID reservasi    : ' + str(data_reservasi['id']))
    print('  Penghuni        : ' + cari_nama_penghuni(data_reservasi['penghuni_id'])
          + ' (ID ' + str(data_reservasi['penghuni_id']) + ')')
    print('  Kode kamar      : ' + data_reservasi['kode_kamar'])
    print('  Nomor kamar     : ' + data_kamar['nomor'])
    print('  Tipe kamar      : ' + data_kamar['tipe'])
    print('  Tanggal masuk   : ' + data_reservasi['tgl_masuk'])
    print('  Durasi          : ' + str(data_reservasi['durasi_bulan']) + ' bulan')
    print('  Harga per bulan : ' + format_rupiah(data_kamar['harga']))
    print('  Total bayar     : ' + format_rupiah(data_reservasi['total_bayar']))
    print('  Sudah dibayar   : ' + format_rupiah(sudah_dibayar))
    print('  Sisa tagihan    : ' + format_rupiah(sisa_tagihan))
    print('  Status          : ' + data_reservasi['status'])


# =====================================================================
# BAGIAN 5: MENAMPILKAN DAN MENGHAPUS DATA (dipakai menu admin)
# =====================================================================

def lihat_data(nama_tabel, daftar_data):
    """Menampilkan data dalam bentuk tabel pandas (kolom password tidak ditampilkan)."""
    if len(daftar_data) == 0:
        print('  (data kosong)')
        return

    # Susun daftar kolom yang akan ditampilkan, kecuali password
    daftar_kolom_tampil = []
    for nama_kolom in ['id'] + KOLOM_TABEL[nama_tabel]:
        if nama_kolom != 'password':
            daftar_kolom_tampil.append(nama_kolom)

    # Ubah list data menjadi tabel pandas lalu cetak (index=False = tanpa nomor baris)
    tabel_pandas = pd.DataFrame(daftar_data, columns=daftar_kolom_tampil)
    print(tabel_pandas.to_string(index=False))


def boleh_dihapus(nama_tabel, data_baris, id_akun_login):
    """Memeriksa apakah sebuah data aman dihapus (tidak dipakai data lain)."""
    if nama_tabel == 'profil':
        if data_baris['id'] == id_akun_login:
            print('  Tidak dapat menghapus akun yang sedang login.')
            return False
        for data_reservasi in data_kost['reservasi']:
            if data_reservasi['penghuni_id'] == data_baris['id']:
                print('  Penghuni ini masih punya data reservasi, tidak dapat dihapus.')
                return False

    if nama_tabel == 'kamar':
        for data_reservasi in data_kost['reservasi']:
            if data_reservasi['kode_kamar'] == data_baris['kode']:
                print('  Kamar ini masih punya data reservasi, tidak dapat dihapus.')
                return False

    if nama_tabel == 'reservasi':
        # Tagihan awal (nominal 0) boleh ikut terhapus, tetapi pembayaran yang sudah masuk tidak
        for data_pembayaran in data_kost['pembayaran']:
            if data_pembayaran['reservasi_id'] == data_baris['id'] and data_pembayaran['nominal'] > 0:
                print('  Reservasi ini sudah punya pembayaran, hapus pembayarannya dulu.')
                return False

    return True


def hapus_data(nama_tabel, id_akun_login, peran):
    # Langkah 1: minta ID yang akan dihapus lalu cari datanya
    id_dicari = minta_angka('ID yang dihapus')
    data_ditemukan = cari_by_id(nama_tabel, id_dicari)

    # Untuk tabel profil, hanya data dengan peran yang sesuai menu yang boleh disentuh
    if data_ditemukan is not None and nama_tabel == 'profil':
        if data_ditemukan['peran'] != peran:
            data_ditemukan = None
    if data_ditemukan is None:
        print('  ID tidak ditemukan.')
        return

    # Langkah 2: cek apakah aman dihapus
    if not boleh_dihapus(nama_tabel, data_ditemukan, id_akun_login):
        return

    # Langkah 3: minta konfirmasi
    jawaban_yakin = input('  Yakin hapus? (y/t): ').strip().lower()
    if jawaban_yakin != 'y':
        return

    # Langkah 4: buat daftar baru yang isinya semua data KECUALI yang dihapus
    daftar_baru = []
    for data_baris in data_kost[nama_tabel]:
        if data_baris['id'] != id_dicari:
            daftar_baru.append(data_baris)
    data_kost[nama_tabel] = daftar_baru

    if nama_tabel == 'reservasi':
        # Hapus juga tagihan awal (nominal 0) milik reservasi ini
        daftar_pembayaran_baru = []
        for data_pembayaran in data_kost['pembayaran']:
            if data_pembayaran['reservasi_id'] != id_dicari:
                daftar_pembayaran_baru.append(data_pembayaran)
        data_kost['pembayaran'] = daftar_pembayaran_baru
        perbarui_status_kamar()
    if nama_tabel == 'pembayaran':
        perbarui_status_pembayaran(data_ditemukan['reservasi_id'])
    simpan_data()
    print('  Data berhasil dihapus.')


# =====================================================================
# BAGIAN 6: PROFIL (ADMIN DAN PENGHUNI DALAM SATU TABEL)
# =====================================================================

def tambah_profil(peran):
    """Menambah akun baru. peran = 'admin' atau 'penghuni'."""
    data_baru = {'id': buat_id_baru('profil')}

    # Username tidak boleh sama dengan akun lain (admin maupun penghuni)
    while True:
        username_baru = minta_teks('username')
        if username_dobel(username_baru, 0):
            print('  Username sudah dipakai.')
        else:
            break
    data_baru['username'] = username_baru
    data_baru['password'] = minta_teks('password')
    data_baru['nama'] = minta_teks('nama')

    # Admin tidak punya no_hp, jadi diisi tanda '-'
    if peran == 'penghuni':
        data_baru['no_hp'] = minta_teks('no_hp')
    else:
        data_baru['no_hp'] = '-'
    data_baru['peran'] = peran

    data_kost['profil'].append(data_baru)
    simpan_data()
    print('  Akun berhasil dibuat dengan ID ' + str(data_baru['id']) + '.')


def ubah_profil_oleh_admin(peran):
    """Admin mengubah data akun admin lain / penghuni berdasarkan ID."""
    id_dicari = minta_angka('ID yang diubah')
    data_ditemukan = cari_by_id('profil', id_dicari)
    if data_ditemukan is None or data_ditemukan['peran'] != peran:
        print('  ID tidak ditemukan.')
        return

    print('  (Tekan Enter jika tidak ingin mengubah)')
    while True:
        username_baru = minta_teks('username [' + data_ditemukan['username'] + ']',
                                   data_ditemukan['username'])
        if username_dobel(username_baru, id_dicari):
            print('  Username sudah dipakai.')
        else:
            break
    password_baru = minta_teks('password [(disembunyikan)]', data_ditemukan['password'])
    nama_baru = minta_teks('nama [' + data_ditemukan['nama'] + ']', data_ditemukan['nama'])
    no_hp_baru = data_ditemukan['no_hp']
    if peran == 'penghuni':
        no_hp_baru = minta_teks('no_hp [' + data_ditemukan['no_hp'] + ']', data_ditemukan['no_hp'])

    # Semua input benar -> pindahkan ke data asli, lalu simpan
    data_ditemukan['username'] = username_baru
    data_ditemukan['password'] = password_baru
    data_ditemukan['nama'] = nama_baru
    data_ditemukan['no_hp'] = no_hp_baru
    simpan_data()
    print('  Data berhasil diubah.')


def ubah_profil_sendiri(akun_login):
    """Mengubah username, nama, dan password akun yang sedang login."""
    print('\n=== UBAH PROFIL ===')
    print('  Username : ' + akun_login['username'])
    print('  Nama     : ' + akun_login['nama'])

    # Langkah 1: minta password sekarang sebagai konfirmasi
    password_input = input('  Masukkan password untuk konfirmasi: ').strip()
    if password_input != akun_login['password']:
        print('  Password salah. Profil tidak diubah.')
        return

    # Langkah 2: minta nilai baru. Tekan Enter = nilai lama dipertahankan.
    print('  (Tekan Enter jika tidak ingin mengubah)')
    while True:
        username_baru = minta_teks('username baru [' + akun_login['username'] + ']',
                                   akun_login['username'])
        if username_dobel(username_baru, akun_login['id']):
            print('  Username sudah dipakai.')
        else:
            break
    nama_baru = minta_teks('nama baru [' + akun_login['nama'] + ']', akun_login['nama'])
    password_baru = minta_teks('password baru [(disembunyikan)]', akun_login['password'])

    # Langkah 3: simpan
    akun_login['username'] = username_baru
    akun_login['nama'] = nama_baru
    akun_login['password'] = password_baru
    simpan_data()
    print('  Profil berhasil diubah.')
    print('  Gunakan username dan password terbaru saat login berikutnya.')


# =====================================================================
# BAGIAN 7: KAMAR
# =====================================================================

def tambah_kamar():
    data_baru = {'id': buat_id_baru('kamar')}

    # Nomor kamar tidak boleh dobel (ditulis huruf besar)
    while True:
        nomor_baru = minta_teks('nomor kamar').upper()
        if nomor_kamar_dobel(nomor_baru, 0):
            print('  Nomor kamar sudah ada, pakai nomor lain.')
        else:
            break

    data_baru['kode'] = buat_kode_kamar()   # kode unik dibuat otomatis
    data_baru['nomor'] = nomor_baru
    data_baru['tipe'] = minta_teks('tipe')
    data_baru['harga'] = minta_angka('harga per bulan')
    data_baru['status'] = 'tersedia'

    data_kost['kamar'].append(data_baru)
    simpan_data()
    print('  Kamar berhasil ditambahkan dengan kode ' + data_baru['kode'] + '.')


def ubah_kamar():
    id_dicari = minta_angka('ID yang diubah')
    data_ditemukan = cari_by_id('kamar', id_dicari)
    if data_ditemukan is None:
        print('  ID tidak ditemukan.')
        return

    print('  Kode kamar : ' + data_ditemukan['kode'] + ' (tidak dapat diubah)')
    print('  (Tekan Enter jika tidak ingin mengubah)')
    while True:
        nomor_baru = minta_teks('nomor [' + data_ditemukan['nomor'] + ']',
                                data_ditemukan['nomor']).upper()
        if nomor_kamar_dobel(nomor_baru, id_dicari):
            print('  Nomor kamar sudah ada, pakai nomor lain.')
        else:
            break
    tipe_baru = minta_teks('tipe [' + data_ditemukan['tipe'] + ']', data_ditemukan['tipe'])
    harga_baru = minta_angka('harga [' + str(data_ditemukan['harga']) + ']', data_ditemukan['harga'])

    # Status kamar tidak diisi manual, karena diatur otomatis oleh data reservasi
    data_ditemukan['nomor'] = nomor_baru
    data_ditemukan['tipe'] = tipe_baru
    data_ditemukan['harga'] = harga_baru
    simpan_data()
    print('  Data berhasil diubah.')


# =====================================================================
# BAGIAN 8: RESERVASI (ADMIN)
# =====================================================================

def tambah_reservasi_admin():
    # Tampilkan daftar penghuni dan kamar supaya admin tahu ID dan kode yang dipilih
    print('Daftar penghuni:')
    lihat_data('profil', filter_profil('penghuni'))
    print('Daftar kamar:')
    lihat_data('kamar', data_kost['kamar'])

    data_baru = {'id': buat_id_baru('reservasi')}
    data_baru['penghuni_id'] = minta_angka('ID penghuni')
    data_baru['kode_kamar'] = minta_teks('kode kamar (contoh KMR001)').upper()
    data_baru['tgl_masuk'] = minta_teks('tgl_masuk (DD-MM-YYYY)')
    data_baru['durasi_bulan'] = minta_angka('durasi_bulan')
    data_baru['status'] = minta_status_reservasi('menunggu')
    data_baru['total_bayar'] = hitung_total_bayar(data_baru['kode_kamar'], data_baru['durasi_bulan'])

    if not cek_reservasi(data_baru, 0):
        return
    data_kost['reservasi'].append(data_baru)
    buat_tagihan_awal(data_baru)    # status 'menunggu' -> masuk juga ke tabel pembayaran
    perbarui_status_kamar()
    simpan_data()
    print('  Reservasi berhasil ditambahkan.')
    tampilkan_detail_reservasi(data_baru)


def ubah_reservasi_admin():
    id_dicari = minta_angka('ID yang diubah')
    data_ditemukan = cari_by_id('reservasi', id_dicari)
    if data_ditemukan is None:
        print('  ID tidak ditemukan.')
        return

    print('  (Tekan Enter jika tidak ingin mengubah)')
    data_sementara = {}     # nilai baru ditampung dulu di sini
    data_sementara['penghuni_id'] = minta_angka('penghuni_id [' + str(data_ditemukan['penghuni_id']) + ']',
                                                data_ditemukan['penghuni_id'])
    data_sementara['kode_kamar'] = minta_teks('kode_kamar [' + data_ditemukan['kode_kamar'] + ']',
                                              data_ditemukan['kode_kamar']).upper()
    data_sementara['tgl_masuk'] = minta_teks('tgl_masuk [' + data_ditemukan['tgl_masuk'] + ']',
                                             data_ditemukan['tgl_masuk'])
    data_sementara['durasi_bulan'] = minta_angka('durasi_bulan [' + str(data_ditemukan['durasi_bulan']) + ']',
                                                 data_ditemukan['durasi_bulan'])
    data_sementara['status'] = minta_status_reservasi(data_ditemukan['status'])
    data_sementara['total_bayar'] = hitung_total_bayar(data_sementara['kode_kamar'],
                                                       data_sementara['durasi_bulan'])

    # Cek, lalu pindahkan nilai baru ke data asli dan simpan
    if not cek_reservasi(data_sementara, id_dicari):
        return
    for nama_kolom in data_sementara:
        data_ditemukan[nama_kolom] = data_sementara[nama_kolom]
    perbarui_status_kamar()
    perbarui_status_pembayaran(id_dicari)
    simpan_data()
    print('  Reservasi berhasil diubah.')
    tampilkan_detail_reservasi(data_ditemukan)


# =====================================================================
# BAGIAN 9: PEMBAYARAN (ADMIN)
# =====================================================================

def tambah_pembayaran():
    id_reservasi = minta_angka('ID reservasi')
    data_reservasi = cari_by_id('reservasi', id_reservasi)
    if data_reservasi is None:
        print('  ID reservasi tidak ditemukan.')
        return
    if data_reservasi['status'] == 'batal':
        print('  Reservasi ini sudah dibatalkan.')
        return

    # Tampilkan tagihan supaya admin tahu berapa yang harus dibayar
    sudah_dibayar = hitung_sudah_dibayar(id_reservasi)
    sisa_tagihan = data_reservasi['total_bayar'] - sudah_dibayar
    print('  Total bayar   : ' + format_rupiah(data_reservasi['total_bayar']))
    print('  Sudah dibayar : ' + format_rupiah(sudah_dibayar))
    print('  Sisa tagihan  : ' + format_rupiah(sisa_tagihan))
    if sisa_tagihan == 0:
        print('  Reservasi ini sudah lunas.')
        return

    nominal_baru = minta_angka('nominal')
    if nominal_baru > sisa_tagihan:
        print('  Nominal melebihi sisa tagihan.')
        return
    tanggal_baru = minta_teks('tanggal (DD-MM-YYYY)')

    # Cari tagihan awal (nominal 0) milik reservasi ini. Jika ada, barisnya diisi
    # supaya tidak ada baris ganda; jika tidak ada, dibuat baris baru.
    data_tagihan = None
    for data_pembayaran in data_kost['pembayaran']:
        if data_pembayaran['reservasi_id'] == id_reservasi and data_pembayaran['nominal'] == 0:
            data_tagihan = data_pembayaran

    if data_tagihan is None:
        data_tagihan = {'id': buat_id_baru('pembayaran'), 'reservasi_id': id_reservasi,
                        'nominal': nominal_baru, 'tanggal': tanggal_baru, 'status': 'cicilan'}
        data_kost['pembayaran'].append(data_tagihan)
    else:
        data_tagihan['nominal'] = nominal_baru
        data_tagihan['tanggal'] = tanggal_baru

    # Status dihitung ulang otomatis
    perbarui_status_pembayaran(id_reservasi)
    simpan_data()
    print('  Pembayaran berhasil ditambahkan, status: ' + data_tagihan['status'] + '.')
    print('  Sisa tagihan sekarang: ' + format_rupiah(sisa_tagihan - nominal_baru))


def ubah_pembayaran():
    id_dicari = minta_angka('ID yang diubah')
    data_ditemukan = cari_by_id('pembayaran', id_dicari)
    if data_ditemukan is None:
        print('  ID tidak ditemukan.')
        return

    data_reservasi = cari_by_id('reservasi', data_ditemukan['reservasi_id'])
    # Batas nominal = total bayar dikurangi pembayaran LAIN milik reservasi yang sama
    batas_nominal = data_reservasi['total_bayar'] - (hitung_sudah_dibayar(data_reservasi['id'])
                                                     - data_ditemukan['nominal'])

    print('  ID reservasi : ' + str(data_ditemukan['reservasi_id']) + ' (tidak dapat diubah)')
    print('  Nominal maksimal: ' + format_rupiah(batas_nominal))
    print('  (Tekan Enter jika tidak ingin mengubah)')
    nominal_baru = minta_angka('nominal [' + str(data_ditemukan['nominal']) + ']', data_ditemukan['nominal'])
    if nominal_baru > batas_nominal:
        print('  Nominal melebihi sisa tagihan.')
        return
    tanggal_baru = minta_teks('tanggal [' + data_ditemukan['tanggal'] + ']', data_ditemukan['tanggal'])

    data_ditemukan['nominal'] = nominal_baru
    data_ditemukan['tanggal'] = tanggal_baru
    perbarui_status_pembayaran(data_ditemukan['reservasi_id'])
    simpan_data()
    print('  Data berhasil diubah.')


# =====================================================================
# BAGIAN 10: MENU ADMIN
# =====================================================================

def lihat_tata_tertib():
    print('\n=== TATA TERTIB ===')
    nomor_aturan = 1
    for teks_aturan in data_kost['tata_tertib']:
        print('  ' + str(nomor_aturan) + '. ' + teks_aturan)
        nomor_aturan = nomor_aturan + 1


def menu_crud(nama_tabel, judul_menu, id_akun_login, peran=''):
    """
    Menu Lihat/Tambah/Ubah/Hapus untuk admin.
    peran hanya dipakai untuk tabel 'profil' ('admin' atau 'penghuni').
    """
    while True:
        print('\n=== ' + judul_menu + ' ===')
        if nama_tabel == 'reservasi':
            print('1. Lihat  2. Tambah  3. Ubah  4. Hapus  5. Detail  0. Kembali')
        else:
            print('1. Lihat  2. Tambah  3. Ubah  4. Hapus  0. Kembali')
        pilihan_menu = input('Pilih: ').strip()
        bersihkan_layar()

        if pilihan_menu == '1':
            if nama_tabel == 'profil':
                lihat_data('profil', filter_profil(peran))   # filtering berdasarkan peran
            else:
                lihat_data(nama_tabel, data_kost[nama_tabel])
        elif pilihan_menu == '2':
            if nama_tabel == 'profil':
                tambah_profil(peran)
            elif nama_tabel == 'kamar':
                tambah_kamar()
            elif nama_tabel == 'reservasi':
                tambah_reservasi_admin()
            else:
                tambah_pembayaran()
        elif pilihan_menu == '3':
            if nama_tabel == 'profil':
                ubah_profil_oleh_admin(peran)
            elif nama_tabel == 'kamar':
                ubah_kamar()
            elif nama_tabel == 'reservasi':
                ubah_reservasi_admin()
            else:
                ubah_pembayaran()
        elif pilihan_menu == '4':
            hapus_data(nama_tabel, id_akun_login, peran)
        elif pilihan_menu == '5' and nama_tabel == 'reservasi':
            id_dicari = minta_angka('ID reservasi')
            data_ditemukan = cari_by_id('reservasi', id_dicari)
            if data_ditemukan is None:
                print('  ID tidak ditemukan.')
            else:
                tampilkan_detail_reservasi(data_ditemukan)
        elif pilihan_menu == '0':
            return
        else:
            print('  Pilihan tidak valid.')

        jeda()


def menu_admin(akun_login):
    while True:
        print('\n=== MENU ADMIN (' + akun_login['nama'] + ') ===')
        print('1. Reservasi')
        print('2. Pembayaran')
        print('3. Kamar')
        print('4. Admin')
        print('5. Penghuni')
        print('6. Lihat Tata Tertib')
        print('7. Ubah Profil Saya')
        print('0. Logout')
        pilihan_menu = input('Pilih: ').strip()
        bersihkan_layar()

        if pilihan_menu == '1':
            menu_crud('reservasi', 'RESERVASI', akun_login['id'])
        elif pilihan_menu == '2':
            menu_crud('pembayaran', 'PEMBAYARAN', akun_login['id'])
        elif pilihan_menu == '3':
            menu_crud('kamar', 'KAMAR', akun_login['id'])
        elif pilihan_menu == '4':
            menu_crud('profil', 'ADMIN', akun_login['id'], 'admin')
        elif pilihan_menu == '5':
            menu_crud('profil', 'PENGHUNI', akun_login['id'], 'penghuni')
        elif pilihan_menu == '6':
            lihat_tata_tertib()
        elif pilihan_menu == '7':
            ubah_profil_sendiri(akun_login)
        elif pilihan_menu == '0':
            print('Logout berhasil.')
            return
        else:
            print('  Pilihan tidak valid.')

        jeda()


# =====================================================================
# BAGIAN 11: FITUR DAN MENU PENGHUNI
# =====================================================================

def buat_reservasi_penghuni(akun_login):
    # Langkah 1: tampilkan kamar yang masih kosong
    print('Kamar tersedia:')
    daftar_kamar_kosong = []
    for data_kamar in data_kost['kamar']:
        if data_kamar['status'] == 'tersedia':
            daftar_kamar_kosong.append(data_kamar)
    lihat_data('kamar', daftar_kamar_kosong)

    # Langkah 2: id penghuni dan status diisi otomatis oleh program
    data_baru = {
        'id': buat_id_baru('reservasi'),
        'penghuni_id': akun_login['id'],
        'status': 'menunggu',
    }

    # Langkah 3: minta kode kamar, tgl_masuk (DD-MM-YYYY), dan durasi_bulan (angka)
    data_baru['kode_kamar'] = minta_teks('kode kamar (contoh KMR001)').upper()
    data_baru['tgl_masuk'] = minta_teks('tgl_masuk (DD-MM-YYYY)')
    data_baru['durasi_bulan'] = minta_angka('durasi_bulan')
    data_baru['total_bayar'] = hitung_total_bayar(data_baru['kode_kamar'], data_baru['durasi_bulan'])

    # Langkah 4: cek, simpan, lalu tampilkan detail
    if not cek_reservasi(data_baru, 0):
        return
    data_kost['reservasi'].append(data_baru)
    buat_tagihan_awal(data_baru)    # status 'menunggu' -> masuk juga ke tabel pembayaran
    perbarui_status_kamar()
    simpan_data()
    print('  Reservasi dibuat, menunggu konfirmasi admin.')
    tampilkan_detail_reservasi(data_baru)


def cari_reservasi_milik(akun_login, id_dicari):
    """Mencari reservasi berdasarkan id, hanya jika milik penghuni yang login."""
    data_ditemukan = cari_by_id('reservasi', id_dicari)
    if data_ditemukan is None:
        return None
    if data_ditemukan['penghuni_id'] != akun_login['id']:
        return None
    return data_ditemukan


def ubah_reservasi_penghuni(akun_login):
    # Langkah 1: minta ID reservasi, hanya boleh reservasi milik sendiri
    id_dicari = minta_angka('ID reservasi yang diubah')
    data_ditemukan = cari_reservasi_milik(akun_login, id_dicari)
    if data_ditemukan is None:
        print('  Reservasi tidak ditemukan.')
        return

    # Langkah 2: hanya reservasi berstatus 'menunggu' yang boleh diubah
    if data_ditemukan['status'] != 'menunggu':
        print('  Hanya reservasi berstatus menunggu yang dapat diubah.')
        return

    # Langkah 3: minta nilai baru. Tekan Enter = nilai lama dipertahankan.
    print('  (Tekan Enter jika tidak ingin mengubah)')
    data_sementara = {'penghuni_id': data_ditemukan['penghuni_id'], 'status': data_ditemukan['status']}
    data_sementara['kode_kamar'] = minta_teks('kode_kamar [' + data_ditemukan['kode_kamar'] + ']',
                                              data_ditemukan['kode_kamar']).upper()
    data_sementara['tgl_masuk'] = minta_teks('tgl_masuk [' + data_ditemukan['tgl_masuk'] + ']',
                                             data_ditemukan['tgl_masuk'])
    data_sementara['durasi_bulan'] = minta_angka('durasi_bulan [' + str(data_ditemukan['durasi_bulan']) + ']',
                                                 data_ditemukan['durasi_bulan'])
    data_sementara['total_bayar'] = hitung_total_bayar(data_sementara['kode_kamar'],
                                                       data_sementara['durasi_bulan'])

    # Langkah 4: cek, lalu simpan
    if not cek_reservasi(data_sementara, id_dicari):
        return
    for nama_kolom in data_sementara:
        data_ditemukan[nama_kolom] = data_sementara[nama_kolom]
    perbarui_status_kamar()
    perbarui_status_pembayaran(id_dicari)
    simpan_data()
    print('  Reservasi diubah.')
    tampilkan_detail_reservasi(data_ditemukan)


def menu_reservasi_penghuni(akun_login):
    while True:
        print('\n=== RESERVASI SAYA ===')
        print('1. Lihat  2. Buat  3. Ubah  4. Detail  0. Kembali')
        pilihan_menu = input('Pilih: ').strip()
        bersihkan_layar()

        if pilihan_menu == '1':
            # Ambil hanya reservasi milik penghuni yang sedang login
            daftar_reservasi_saya = []
            for data_reservasi in data_kost['reservasi']:
                if data_reservasi['penghuni_id'] == akun_login['id']:
                    daftar_reservasi_saya.append(data_reservasi)
            lihat_data('reservasi', daftar_reservasi_saya)
        elif pilihan_menu == '2':
            buat_reservasi_penghuni(akun_login)
        elif pilihan_menu == '3':
            ubah_reservasi_penghuni(akun_login)
        elif pilihan_menu == '4':
            id_dicari = minta_angka('ID reservasi')
            data_ditemukan = cari_reservasi_milik(akun_login, id_dicari)
            if data_ditemukan is None:
                print('  Reservasi tidak ditemukan.')
            else:
                tampilkan_detail_reservasi(data_ditemukan)
        elif pilihan_menu == '0':
            return
        else:
            print('  Pilihan tidak valid.')

        jeda()


def lihat_pembayaran_penghuni(akun_login):
    # Langkah 1: kumpulkan reservasi milik penghuni ini
    daftar_reservasi_saya = []
    daftar_id_milik = []
    for data_reservasi in data_kost['reservasi']:
        if data_reservasi['penghuni_id'] == akun_login['id']:
            daftar_reservasi_saya.append(data_reservasi)
            daftar_id_milik.append(data_reservasi['id'])

    # Langkah 2: ambil pembayaran yang reservasinya milik penghuni ini
    daftar_pembayaran_saya = []
    for data_pembayaran in data_kost['pembayaran']:
        if data_pembayaran['reservasi_id'] in daftar_id_milik:
            daftar_pembayaran_saya.append(data_pembayaran)

    print('\n=== PEMBAYARAN SAYA ===')
    lihat_data('pembayaran', daftar_pembayaran_saya)

    # Langkah 3: ringkasan total bayar, sudah dibayar, dan sisa tiap reservasi
    for data_reservasi in daftar_reservasi_saya:
        sudah_dibayar = hitung_sudah_dibayar(data_reservasi['id'])
        sisa_tagihan = data_reservasi['total_bayar'] - sudah_dibayar
        print('\n  Reservasi ID ' + str(data_reservasi['id']) + ' (' + data_reservasi['status'] + ')')
        print('    Total bayar   : ' + format_rupiah(data_reservasi['total_bayar']))
        print('    Sudah dibayar : ' + format_rupiah(sudah_dibayar))
        print('    Sisa tagihan  : ' + format_rupiah(sisa_tagihan))


def menu_penghuni(akun_login):
    while True:
        print('\n=== MENU PENGHUNI (' + akun_login['nama'] + ') ===')
        print('1. Reservasi (Lihat/Buat/Ubah/Detail)')
        print('2. Lihat Pembayaran')
        print('3. Lihat Kamar')
        print('4. Lihat Tata Tertib')
        print('5. Ubah Profil Saya')
        print('0. Logout')
        pilihan_menu = input('Pilih: ').strip()
        bersihkan_layar()

        if pilihan_menu == '1':
            menu_reservasi_penghuni(akun_login)
        elif pilihan_menu == '2':
            lihat_pembayaran_penghuni(akun_login)
        elif pilihan_menu == '3':
            print('\n=== DAFTAR KAMAR ===')
            lihat_data('kamar', data_kost['kamar'])
        elif pilihan_menu == '4':
            lihat_tata_tertib()
        elif pilihan_menu == '5':
            ubah_profil_sendiri(akun_login)
        elif pilihan_menu == '0':
            print('Logout berhasil.')
            return
        else:
            print('  Pilihan tidak valid.')

        jeda()


# =====================================================================
# BAGIAN 12: LOGIN, REGISTER, DAN MENU UTAMA
# =====================================================================

def login():
    """
    Admin dan penghuni sekarang ada dalam satu tabel (profil),
    jadi cukup satu perulangan. Peran akun dibaca dari kolom 'peran'.
    """
    username_input = minta_teks('Username')
    password_input = minta_teks('Password')

    for data_akun in data_kost['profil']:
        if data_akun['username'] == username_input and data_akun['password'] == password_input:
            print('Login berhasil. Selamat datang, ' + data_akun['nama'] + '!')
            return data_akun, data_akun['peran']

    print('Username atau password salah.')
    return None, ''


def register():
    print('\n=== REGISTER PENGHUNI ===')
    tambah_profil('penghuni')
    print('  Silakan login.')


def main():
    while True:
        print('\n===== SISTEM RESERVASI KOST =====')
        print('1. Login')
        print('2. Register Penghuni')
        print('0. Keluar')
        pilihan_menu = input('Pilih: ').strip()
        bersihkan_layar()

        if pilihan_menu == '1':
            akun_login, peran_akun = login()
            if akun_login is None:
                jeda()
            elif peran_akun == 'admin':
                menu_admin(akun_login)
            else:
                menu_penghuni(akun_login)
        elif pilihan_menu == '2':
            register()
            jeda()
        elif pilihan_menu == '0':
            print('Terima kasih.')
            break
        else:
            print('Pilihan tidak valid.')
            jeda()


# Program mulai dari sini
main()
