// =====================================================
// MINI POS - Kasir & Keranjang Belanja Sederhana
// Qinthafa Treza Aimar - 124140155 - Kelas RA
// =====================================================

// ---------- Konstanta aturan aplikasi ----------
const KUNCI_STORAGE = "keranjangBelanja"; // nama key di localStorage
const NAMA_MIN = 3;                       // minimal karakter nama barang
const HARGA_MIN = 500;                    // minimal harga satuan
const QTY_MIN = 1;                        // minimal jumlah barang
const BATAS_DISKON = 50000;               // total minimal untuk dapat diskon
const PERSEN_DISKON = 10;                 // besar diskon dalam persen

// ---------- Mengambil elemen HTML ----------
const formBarang = document.getElementById("form-barang");
const inputNama = document.getElementById("nama-barang");
const inputHarga = document.getElementById("harga-barang");
const inputQty = document.getElementById("qty-barang");
const errorNama = document.getElementById("error-nama");
const errorHarga = document.getElementById("error-harga");
const errorQty = document.getElementById("error-qty");

const isiKeranjang = document.getElementById("isi-keranjang");
const pesanKosong = document.getElementById("pesan-kosong");
const btnReset = document.getElementById("btn-reset");

const elTotalBelanja = document.getElementById("total-belanja");
const elInfoDiskon = document.getElementById("info-diskon");
const elNominalDiskon = document.getElementById("nominal-diskon");
const elTotalAkhir = document.getElementById("total-akhir");
const inputUangBayar = document.getElementById("uang-bayar");
const elKembalian = document.getElementById("kembalian");
const pesanBayar = document.getElementById("pesan-bayar");

// ---------- Data utama ----------
// Keranjang adalah array berisi objek barang: { id, nama, harga, qty }
// Saat halaman dibuka, isinya langsung diambil dari localStorage.
let keranjang = muatKeranjang();

// =====================================================
// FUNGSI BANTUAN
// =====================================================

// Mengubah angka menjadi format Rupiah, contoh: 15000 -> "Rp 15.000"
function formatRupiah(angka) {
  return "Rp " + angka.toLocaleString("id-ID");
}

// =====================================================
// LOCALSTORAGE
// =====================================================

// Menyimpan keranjang. localStorage hanya bisa menyimpan teks,
// jadi array diubah dulu menjadi teks JSON dengan JSON.stringify().
function simpanKeranjang() {
  localStorage.setItem(KUNCI_STORAGE, JSON.stringify(keranjang));
}

// Memuat keranjang. Teks JSON diubah kembali menjadi array dengan JSON.parse().
// Kalau belum ada data (atau datanya rusak), kembalikan array kosong.
function muatKeranjang() {
  try {
    const dataTersimpan = localStorage.getItem(KUNCI_STORAGE);
    return dataTersimpan ? JSON.parse(dataTersimpan) : [];
  } catch (error) {
    console.error("Gagal membaca localStorage:", error);
    return [];
  }
}

// =====================================================
// VALIDASI FORM
// =====================================================

// Menampilkan atau menghapus pesan error pada satu input.
// Kalau pesan kosong (""), berarti input tersebut valid.
function aturError(input, elemenError, pesan) {
  elemenError.textContent = pesan;
  if (pesan === "") {
    input.classList.remove("input-salah");
  } else {
    input.classList.add("input-salah");
  }
}

// Memeriksa ketiga input.
// Mengembalikan objek barang kalau semua valid, atau null kalau ada yang salah.
function validasiForm() {
  const nama = inputNama.value.trim();
  const hargaTeks = inputHarga.value.trim();
  const qtyTeks = inputQty.value.trim();
  const harga = Number(hargaTeks);
  const qty = Number(qtyTeks);
  let valid = true;

  // Nama barang: wajib diisi, minimal 3 karakter
  if (nama === "") {
    aturError(inputNama, errorNama, "Nama barang wajib diisi.");
    valid = false;
  } else if (nama.length < NAMA_MIN) {
    aturError(inputNama, errorNama, "Nama barang minimal " + NAMA_MIN + " karakter.");
    valid = false;
  } else {
    aturError(inputNama, errorNama, "");
  }

  // Harga satuan: wajib angka, minimal Rp 500
  if (hargaTeks === "" || isNaN(harga)) {
    aturError(inputHarga, errorHarga, "Harga wajib diisi dengan angka.");
    valid = false;
  } else if (harga < HARGA_MIN) {
    aturError(inputHarga, errorHarga, "Harga minimal " + formatRupiah(HARGA_MIN) + ".");
    valid = false;
  } else {
    aturError(inputHarga, errorHarga, "");
  }

  // Qty: wajib bilangan bulat, minimal 1
  if (qtyTeks === "" || isNaN(qty)) {
    aturError(inputQty, errorQty, "Jumlah wajib diisi dengan angka.");
    valid = false;
  } else if (!Number.isInteger(qty)) {
    aturError(inputQty, errorQty, "Jumlah harus bilangan bulat.");
    valid = false;
  } else if (qty < QTY_MIN) {
    aturError(inputQty, errorQty, "Jumlah minimal " + QTY_MIN + ".");
    valid = false;
  } else {
    aturError(inputQty, errorQty, "");
  }

  if (!valid) {
    return null;
  }

  // id unik dipakai untuk menandai barang mana yang dihapus
  return { id: Date.now(), nama: nama, harga: harga, qty: qty };
}

// =====================================================
// PERHITUNGAN (KALKULATOR)
// =====================================================

// Menghitung total belanja, diskon, dan total akhir dari isi keranjang.
function hitungRingkasan() {
  // reduce menjumlahkan subtotal (harga x qty) semua barang
  const total = keranjang.reduce(function (jumlah, barang) {
    return jumlah + barang.harga * barang.qty;
  }, 0);

  // Diskon 10% hanya berlaku kalau total minimal Rp 50.000
  const dapatDiskon = total >= BATAS_DISKON;
  const diskon = dapatDiskon ? (total * PERSEN_DISKON) / 100 : 0;
  const totalAkhir = total - diskon;

  return { total: total, diskon: diskon, totalAkhir: totalAkhir, dapatDiskon: dapatDiskon };
}

// Menghitung kembalian berdasarkan isi input "Uang Bayar".
function hitungKembalian() {
  const ringkasan = hitungRingkasan();
  const uangTeks = inputUangBayar.value.trim();
  const uangBayar = Number(uangTeks);

  // Belum ada barang atau uang belum diisi: tidak ada yang dihitung
  if (keranjang.length === 0 || uangTeks === "") {
    elKembalian.textContent = "-";
    pesanBayar.textContent = "";
    return;
  }

  if (isNaN(uangBayar) || uangBayar < 0) {
    elKembalian.textContent = "-";
    pesanBayar.textContent = "Uang bayar harus berupa angka positif.";
    return;
  }

  const kembalian = uangBayar - ringkasan.totalAkhir;

  if (kembalian < 0) {
    // Math.abs mengubah angka negatif jadi positif untuk ditampilkan
    elKembalian.textContent = "-";
    pesanBayar.textContent =
      "Uang belum mencukupi, kurang " + formatRupiah(Math.abs(kembalian)) + ".";
  } else {
    elKembalian.textContent = formatRupiah(kembalian);
    pesanBayar.textContent = "";
  }
}

// =====================================================
// MENAMPILKAN DATA KE HALAMAN (RENDER)
// =====================================================

// Membuat satu sel tabel (<td>). textContent dipakai (bukan innerHTML)
// supaya nama barang yang diketik user tidak dijalankan sebagai kode HTML.
function buatSel(isi, kelas) {
  const sel = document.createElement("td");
  sel.textContent = isi;
  if (kelas) {
    sel.className = kelas;
  }
  return sel;
}

// Menggambar ulang seluruh isi tabel keranjang.
function renderKeranjang() {
  isiKeranjang.innerHTML = ""; // kosongkan tabel dulu

  keranjang.forEach(function (barang, index) {
    const baris = document.createElement("tr");

    baris.appendChild(buatSel(index + 1));
    baris.appendChild(buatSel(barang.nama));
    baris.appendChild(buatSel(formatRupiah(barang.harga), "angka"));
    baris.appendChild(buatSel(barang.qty, "angka"));
    baris.appendChild(buatSel(formatRupiah(barang.harga * barang.qty), "angka"));

    // Tombol hapus untuk baris ini
    const selAksi = document.createElement("td");
    const btnHapus = document.createElement("button");
    btnHapus.type = "button";
    btnHapus.className = "btn btn-hapus";
    btnHapus.textContent = "Hapus";
    btnHapus.addEventListener("click", function () {
      hapusBarang(barang.id);
    });
    selAksi.appendChild(btnHapus);
    baris.appendChild(selAksi);

    isiKeranjang.appendChild(baris);
  });

  // Pesan "keranjang kosong" hanya muncul kalau tidak ada barang
  pesanKosong.style.display = keranjang.length === 0 ? "block" : "none";
}

// Menampilkan total, diskon, dan total akhir.
function renderRingkasan() {
  const ringkasan = hitungRingkasan();

  elTotalBelanja.textContent = formatRupiah(ringkasan.total);
  elNominalDiskon.textContent = "- " + formatRupiah(ringkasan.diskon);
  elTotalAkhir.textContent = formatRupiah(ringkasan.totalAkhir);

  if (ringkasan.dapatDiskon) {
    elInfoDiskon.textContent = "(" + PERSEN_DISKON + "%)";
  } else {
    elInfoDiskon.textContent = "(belanja min. " + formatRupiah(BATAS_DISKON) + ")";
  }
}

// Satu fungsi untuk memperbarui semua tampilan sekaligus.
// Dipanggil setiap kali isi keranjang berubah.
function perbaruiTampilan() {
  renderKeranjang();
  renderRingkasan();
  hitungKembalian();
}

// =====================================================
// AKSI: TAMBAH, HAPUS, RESET
// =====================================================

function tambahBarang(event) {
  event.preventDefault(); // cegah halaman reload saat form dikirim

  const barangBaru = validasiForm();
  if (barangBaru === null) {
    return; // ada input yang salah, barang tidak dimasukkan
  }

  keranjang.push(barangBaru);
  simpanKeranjang();
  perbaruiTampilan();

  formBarang.reset(); // kosongkan form setelah berhasil
  inputNama.focus();
}

function hapusBarang(id) {
  // filter membuat array baru berisi semua barang KECUALI yang id-nya cocok
  keranjang = keranjang.filter(function (barang) {
    return barang.id !== id;
  });
  simpanKeranjang();
  perbaruiTampilan();
}

function resetTransaksi() {
  if (keranjang.length > 0 && !confirm("Kosongkan keranjang dan mulai transaksi baru?")) {
    return;
  }

  keranjang = [];
  localStorage.removeItem(KUNCI_STORAGE); // bersihkan data di localStorage
  inputUangBayar.value = "";
  formBarang.reset();
  aturError(inputNama, errorNama, "");
  aturError(inputHarga, errorHarga, "");
  aturError(inputQty, errorQty, "");
  perbaruiTampilan();
}

// =====================================================
// EVENT LISTENER
// =====================================================

formBarang.addEventListener("submit", tambahBarang);
btnReset.addEventListener("click", resetTransaksi);

// "input" terpicu setiap kali isi kolom berubah, jadi kembalian
// langsung terhitung saat kasir mengetik nominal uang.
inputUangBayar.addEventListener("input", hitungKembalian);

// Tampilkan data dari localStorage saat halaman pertama kali dibuka
perbaruiTampilan();
