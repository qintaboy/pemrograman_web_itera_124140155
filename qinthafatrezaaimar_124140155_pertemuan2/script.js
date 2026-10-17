// =====================================================
// DASHBOARD TUGAS KULIAH - Personal Dashboard (ES6+)
// Qinthafa Treza Aimar - 124140155 - Kelas RA
// =====================================================

// ---------- Konstanta ----------
const KUNCI_STORAGE = "dashboardTugasKuliah";
const LOKASI_KAMPUS = { nama: "ITERA, Lampung Selatan", lat: -5.3582, lon: 105.3145 };
const URL_CUACA =
  `https://api.open-meteo.com/v1/forecast?latitude=${LOKASI_KAMPUS.lat}&longitude=${LOKASI_KAMPUS.lon}` +
  "&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m" +
  "&timezone=Asia%2FJakarta";
const URL_KUTIPAN = "https://dummyjson.com/quotes/random";
const NAMA_PRIORITAS = { tinggi: "Prioritas tinggi", sedang: "Prioritas sedang", rendah: "Prioritas rendah" };
const URUTAN_PRIORITAS = { tinggi: 0, sedang: 1, rendah: 2 };

// Arti kode cuaca dari Open-Meteo (WMO weather code)
const KODE_CUACA = {
  0: "Cerah", 1: "Cerah berawan", 2: "Berawan sebagian", 3: "Berawan",
  45: "Berkabut", 48: "Berkabut",
  51: "Gerimis ringan", 53: "Gerimis", 55: "Gerimis lebat",
  61: "Hujan ringan", 63: "Hujan sedang", 65: "Hujan lebat",
  80: "Hujan lokal ringan", 81: "Hujan lokal", 82: "Hujan lokal lebat",
  95: "Badai petir", 96: "Badai petir", 99: "Badai petir",
};

// ---------- Fungsi bantuan (arrow function) ----------

// Mencegah teks dari pengguna dijalankan sebagai HTML saat dimasukkan ke template literal
const amankanTeks = (teks) =>
  String(teks)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

// "2026-10-20" -> objek Date jam 00:00 waktu lokal
const keTanggal = (teksTanggal) => {
  const [tahun, bulan, hari] = teksTanggal.split("-").map(Number);
  return new Date(tahun, bulan - 1, hari);
};

// Tanggal hari ini dalam format "YYYY-MM-DD" (untuk nilai default input date)
const hariIniTeks = () => {
  const d = new Date();
  const bulan = String(d.getMonth() + 1).padStart(2, "0");
  const hari = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${bulan}-${hari}`;
};

// Id unik sederhana: waktu sekarang + angka acak, dalam basis 36
const buatId = () => `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;

const formatTanggal = (tanggal, opsi = { weekday: "long", day: "numeric", month: "long", year: "numeric" }) =>
  tanggal.toLocaleDateString("id-ID", opsi);

// =====================================================
// CLASS TaskItem - model data untuk satu tugas
// =====================================================
class TaskItem {
  // Destructuring + nilai default langsung di parameter constructor
  constructor({ id = buatId(), judul, matkul, deadline, prioritas = "sedang", selesai = false }) {
    this.id = id;
    this.judul = judul;
    this.matkul = matkul;
    this.deadline = deadline;
    this.prioritas = prioritas;
    this.selesai = selesai;
  }

  // Getter: selisih hari dari hari ini ke deadline (negatif = sudah lewat)
  get sisaHari() {
    const hariIni = keTanggal(hariIniTeks());
    const satuHari = 24 * 60 * 60 * 1000;
    return Math.round((keTanggal(this.deadline) - hariIni) / satuHari);
  }

  // Label status deadline untuk ditampilkan di daftar
  get statusDeadline() {
    if (this.selesai) return { teks: "Selesai", kelas: "beres" };

    const sisa = this.sisaHari;
    if (sisa < 0) return { teks: `Terlambat ${Math.abs(sisa)} hari`, kelas: "lewat" };
    if (sisa === 0) return { teks: "Deadline hari ini", kelas: "lewat" };
    if (sisa === 1) return { teks: "Deadline besok", kelas: "dekat" };
    if (sisa <= 3) return { teks: `${sisa} hari lagi`, kelas: "dekat" };
    return { teks: `${sisa} hari lagi`, kelas: "" };
  }

  // Membuat salinan baru dengan beberapa data diganti (objek lama tidak diubah)
  ubah(perubahan) {
    return new TaskItem({ ...this, ...perubahan });
  }
}

// =====================================================
// CLASS DashboardApp - state, localStorage, fetch, render
// =====================================================
class DashboardApp {
  constructor() {
    this.tugas = this.muatData();
    this.filter = "semua";
    this.idDiedit = null; // null = mode tambah, berisi id = mode edit

    this.el = {
      form: document.getElementById("form-tugas"),
      judulForm: document.getElementById("judul-form"),
      judul: document.getElementById("input-judul"),
      matkul: document.getElementById("input-matkul"),
      deadline: document.getElementById("input-deadline"),
      prioritas: document.getElementById("input-prioritas"),
      errorJudul: document.getElementById("error-judul"),
      errorMatkul: document.getElementById("error-matkul"),
      errorDeadline: document.getElementById("error-deadline"),
      btnSimpan: document.getElementById("btn-simpan"),
      btnBatal: document.getElementById("btn-batal"),
      daftar: document.getElementById("daftar-tugas"),
      filter: document.getElementById("filter"),
      statistik: document.getElementById("statistik"),
      cuaca: document.getElementById("cuaca-isi"),
      kutipanTeks: document.getElementById("kutipan-teks"),
      kutipanPenulis: document.getElementById("kutipan-penulis"),
      jam: document.getElementById("jam"),
      tanggal: document.getElementById("tanggal"),
      sapaan: document.getElementById("sapaan"),
    };
  }

  // ---------- Memulai aplikasi ----------
  init() {
    this.el.deadline.value = hariIniTeks();
    this.pasangEvent();
    this.render();

    this.perbaruiJam();
    setInterval(() => this.perbaruiJam(), 1000);

    // Dua permintaan API dijalankan bersamaan
    Promise.all([this.ambilCuaca(), this.ambilKutipan()]);
  }

  // ---------- localStorage ----------
  muatData() {
    try {
      const teks = localStorage.getItem(KUNCI_STORAGE);
      const data = teks ? JSON.parse(teks) : [];
      // Data dari localStorage hanya objek biasa, diubah lagi menjadi TaskItem
      return data.map((item) => new TaskItem(item));
    } catch (error) {
      console.error("Gagal membaca localStorage:", error);
      return [];
    }
  }

  simpanData() {
    localStorage.setItem(KUNCI_STORAGE, JSON.stringify(this.tugas));
  }

  // ---------- Operasi data (CRUD) ----------
  // Semua operasi membuat array BARU (immutable), tidak mengubah array lama
  tambahTugas(data) {
    this.tugas = [...this.tugas, new TaskItem(data)];
    this.simpanDanRender();
  }

  editTugas(id, perubahan) {
    this.tugas = this.tugas.map((item) => (item.id === id ? item.ubah(perubahan) : item));
    this.simpanDanRender();
  }

  hapusTugas(id) {
    this.tugas = this.tugas.filter((item) => item.id !== id);
    this.simpanDanRender();
  }

  tandaiSelesai(id) {
    const item = this.tugas.find((t) => t.id === id);
    if (item) this.editTugas(id, { selesai: !item.selesai });
  }

  simpanDanRender() {
    this.simpanData();
    this.render();
  }

  // ---------- Validasi form ----------
  ambilDataForm() {
    const judul = this.el.judul.value.trim();
    const matkul = this.el.matkul.value.trim();
    const deadline = this.el.deadline.value;
    const prioritas = this.el.prioritas.value;

    const error = {
      judul: judul.length < 3 ? "Nama tugas minimal 3 karakter." : "",
      matkul: matkul === "" ? "Mata kuliah wajib diisi." : "",
      deadline: deadline === "" ? "Pilih tanggal deadline." : "",
    };

    this.tampilkanError(this.el.judul, this.el.errorJudul, error.judul);
    this.tampilkanError(this.el.matkul, this.el.errorMatkul, error.matkul);
    this.tampilkanError(this.el.deadline, this.el.errorDeadline, error.deadline);

    const valid = Object.values(error).every((pesan) => pesan === "");
    return valid ? { judul, matkul, deadline, prioritas } : null;
  }

  tampilkanError(input, elemen, pesan) {
    elemen.textContent = pesan;
    input.classList.toggle("input-salah", pesan !== "");
  }

  // ---------- Mode edit ----------
  mulaiEdit(id) {
    const item = this.tugas.find((t) => t.id === id);
    if (!item) return;

    // Destructuring untuk mengambil properti yang dibutuhkan
    const { judul, matkul, deadline, prioritas } = item;
    this.idDiedit = id;
    this.el.judul.value = judul;
    this.el.matkul.value = matkul;
    this.el.deadline.value = deadline;
    this.el.prioritas.value = prioritas;

    this.el.judulForm.textContent = "Edit Tugas";
    this.el.btnSimpan.textContent = "Simpan Perubahan";
    this.el.btnBatal.hidden = false;
    this.el.judul.focus();
  }

  resetForm() {
    this.idDiedit = null;
    this.el.form.reset();
    this.el.deadline.value = hariIniTeks();
    this.el.judulForm.textContent = "Tambah Tugas";
    this.el.btnSimpan.textContent = "Tambah Tugas";
    this.el.btnBatal.hidden = true;
    [
      [this.el.judul, this.el.errorJudul],
      [this.el.matkul, this.el.errorMatkul],
      [this.el.deadline, this.el.errorDeadline],
    ].forEach(([input, elemen]) => this.tampilkanError(input, elemen, ""));
  }

  // ---------- Event ----------
  pasangEvent() {
    this.el.form.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = this.ambilDataForm();
      if (!data) return;

      if (this.idDiedit) {
        this.editTugas(this.idDiedit, data);
      } else {
        this.tambahTugas(data);
      }
      this.resetForm();
    });

    this.el.btnBatal.addEventListener("click", () => this.resetForm());

    // Event delegation: satu listener untuk semua tombol di daftar tugas
    this.el.daftar.addEventListener("click", (event) => {
      const tombol = event.target.closest("[data-aksi]");
      if (!tombol) return;

      const { aksi, id } = tombol.dataset;
      if (aksi === "selesai") this.tandaiSelesai(id);
      if (aksi === "edit") this.mulaiEdit(id);
      if (aksi === "hapus") {
        const item = this.tugas.find((t) => t.id === id);
        if (item && confirm(`Hapus tugas "${item.judul}"?`)) {
          if (this.idDiedit === id) this.resetForm();
          this.hapusTugas(id);
        }
      }
    });

    this.el.filter.addEventListener("click", (event) => {
      const chip = event.target.closest("[data-filter]");
      if (!chip) return;
      this.filter = chip.dataset.filter;
      this.el.filter.querySelectorAll(".chip").forEach((c) => c.classList.toggle("aktif", c === chip));
      this.renderTugas();
    });

    document.getElementById("btn-cuaca").addEventListener("click", () => this.ambilCuaca());
    document.getElementById("btn-kutipan").addEventListener("click", () => this.ambilKutipan());
  }

  // ---------- Fetch API (async/await) ----------
  async ambilCuaca() {
    this.el.cuaca.innerHTML = "Memuat cuaca...";
    try {
      const respons = await fetch(URL_CUACA);
      if (!respons.ok) throw new Error(`Server cuaca membalas ${respons.status}`);

      const { current } = await respons.json();
      const {
        temperature_2m: suhu,
        apparent_temperature: terasa,
        relative_humidity_2m: kelembapan,
        wind_speed_10m: angin,
        weather_code: kode,
      } = current;

      this.el.cuaca.innerHTML = `
        <div class="cuaca-utama">
          <span class="cuaca-suhu">${Math.round(suhu)}°C</span>
          <span class="cuaca-kondisi">${KODE_CUACA[kode] ?? "Tidak diketahui"}</span>
        </div>
        <div class="cuaca-detail">
          <span>Terasa ${Math.round(terasa)}°C</span>
          <span>Kelembapan ${kelembapan}%</span>
          <span>Angin ${angin} km/j</span>
        </div>
        <p class="cuaca-lokasi">${LOKASI_KAMPUS.nama} &middot; Open-Meteo</p>
      `;
    } catch (error) {
      console.error("Gagal mengambil cuaca:", error);
      this.el.cuaca.innerHTML = `<p class="pesan-gagal">Cuaca tidak bisa dimuat. Periksa koneksi internet, lalu klik Perbarui.</p>`;
    }
  }

  async ambilKutipan() {
    this.el.kutipanTeks.textContent = "Memuat kutipan...";
    this.el.kutipanPenulis.textContent = "";
    try {
      const respons = await fetch(URL_KUTIPAN);
      if (!respons.ok) throw new Error(`Server kutipan membalas ${respons.status}`);

      const { quote, author } = await respons.json();
      this.el.kutipanTeks.textContent = `"${quote}"`;
      this.el.kutipanPenulis.textContent = `- ${author}`;
    } catch (error) {
      console.error("Gagal mengambil kutipan:", error);
      this.el.kutipanTeks.textContent = '"Sedikit demi sedikit, lama-lama tugas jadi selesai."';
      this.el.kutipanPenulis.textContent = "- Kutipan cadangan (offline)";
    }
  }

  // ---------- Jam & sapaan ----------
  perbaruiJam() {
    const sekarang = new Date();
    const jam = sekarang.getHours();
    // let dipakai karena nilai "waktu" diubah sesuai jam; yang tidak berubah memakai const
    let waktu = "Selamat malam";
    if (jam < 11) waktu = "Selamat pagi";
    else if (jam < 15) waktu = "Selamat siang";
    else if (jam < 18) waktu = "Selamat sore";

    this.el.jam.textContent = sekarang.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" });
    this.el.tanggal.textContent = formatTanggal(sekarang);
    this.el.sapaan.textContent = `${waktu}, Qinthafa!`;
  }

  // ---------- Render ----------
  get tugasTampil() {
    const saringan = {
      semua: () => true,
      belum: (item) => !item.selesai,
      selesai: (item) => item.selesai,
    };

    // Salin dulu dengan spread sebelum sort, supaya this.tugas tidak ikut terurut
    return [...this.tugas]
      .filter(saringan[this.filter])
      .sort(
        (a, b) =>
          a.selesai - b.selesai ||
          a.deadline.localeCompare(b.deadline) ||
          URUTAN_PRIORITAS[a.prioritas] - URUTAN_PRIORITAS[b.prioritas]
      );
  }

  render() {
    this.renderStatistik();
    this.renderTugas();
  }

  renderStatistik() {
    const total = this.tugas.length;
    const selesai = this.tugas.filter((t) => t.selesai).length;
    const mendesak = this.tugas.filter((t) => !t.selesai && t.sisaHari <= 3).length;
    const persen = total === 0 ? 0 : Math.round((selesai / total) * 100);

    const kartu = [
      { angka: total, label: "Total tugas" },
      { angka: total - selesai, label: "Belum selesai" },
      { angka: mendesak, label: "Deadline ≤ 3 hari", kelas: mendesak > 0 ? "peringatan" : "" },
      { angka: `${persen}%`, label: "Progres" },
    ];

    this.el.statistik.innerHTML = kartu
      .map(
        ({ angka, label, kelas = "" }) => `
        <div class="stat ${kelas}">
          <p class="stat-angka">${angka}</p>
          <p class="stat-label">${label}</p>
        </div>`
      )
      .join("");
  }

  renderTugas() {
    const daftar = this.tugasTampil;

    if (daftar.length === 0) {
      const pesan = {
        semua: "Belum ada tugas. Tambahkan tugas pertamamu lewat form.",
        belum: "Semua tugas sudah selesai. Mantap!",
        selesai: "Belum ada tugas yang ditandai selesai.",
      };
      this.el.daftar.innerHTML = `<li class="kosong">${pesan[this.filter]}</li>`;
      return;
    }

    this.el.daftar.innerHTML = daftar.map((item) => this.templateTugas(item)).join("");
  }

  // Template literal untuk satu baris tugas
  templateTugas({ id, judul, matkul, deadline, prioritas, selesai, statusDeadline }) {
    const tanggal = formatTanggal(keTanggal(deadline), { weekday: "short", day: "numeric", month: "short" });

    return `
      <li class="tugas prioritas-${prioritas} ${selesai ? "selesai" : ""}">
        <input type="checkbox" data-aksi="selesai" data-id="${id}" ${selesai ? "checked" : ""}
          aria-label="Tandai ${amankanTeks(judul)} selesai">
        <div>
          <p class="tugas-judul">${amankanTeks(judul)}</p>
          <p class="tugas-matkul">${amankanTeks(matkul)}</p>
          <div class="label-baris">
            <span class="label ${statusDeadline.kelas}">${statusDeadline.teks}</span>
            <span class="label">${tanggal}</span>
            <span class="label">${NAMA_PRIORITAS[prioritas]}</span>
          </div>
        </div>
        <div class="tugas-aksi">
          <button type="button" class="btn-kecil" data-aksi="edit" data-id="${id}">Edit</button>
          <button type="button" class="btn-kecil hapus" data-aksi="hapus" data-id="${id}">Hapus</button>
        </div>
      </li>
    `;
  }
}

// ---------- Jalankan aplikasi ----------
const app = new DashboardApp();
app.init();
