const API = "/api/barang";

// 1. Memuat dan Menampilkan Data
async function loadBarang() {
    const res = await fetch(API);
    const data = await res.json();

    const tbody = document.getElementById("tabelBarang");
    tbody.innerHTML = "";

    data.forEach(b => {
        tbody.innerHTML += `
            <tr>
                <td>${b.id}</td>
                <td>${b.nama}</td>
                <td>${b.stok}</td>
                <td>${b.harga}</td>
                <td>
                    <button class="btn-edit" onclick="setEditForm(${b.id}, '${b.nama}', ${b.stok}, ${b.harga})">Edit</button>
                    <button class="btn-delete" onclick="hapusBarang(${b.id})">Hapus</button>
                </td>
            </tr>
        `;
    });
}

// 2. Tambah Barang (POST)
document.getElementById("formTambah").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nama = document.getElementById("nama").value;
    const stok = parseInt(document.getElementById("stok").value);
    const harga = parseFloat(document.getElementById("harga").value);

    await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nama, stok, harga })
    });

    document.getElementById("formTambah").reset();
    loadBarang();
});

// 3. Mengisi Form Edit
function setEditForm(id, nama, stok, harga) {
    document.getElementById("uid").value = id;
    document.getElementById("unama").value = nama;
    document.getElementById("ustok").value = stok;
    document.getElementById("uharga").value = harga;
}

// 4. Update Barang (PUT)
document.getElementById("formEdit").addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = parseInt(document.getElementById("uid").value);
    const nama = document.getElementById("unama").value;
    const stok = parseInt(document.getElementById("ustok").value);
    const harga = parseFloat(document.getElementById("uharga").value);

    await fetch(`${API}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nama, stok, harga })
    });

    document.getElementById("formEdit").reset();
    loadBarang();
});

// 5. Hapus Barang (DELETE)
async function hapusBarang(id) {
    if(confirm(`Yakin ingin menghapus barang dengan ID ${id}?`)) {
        await fetch(`${API}/${id}`, { method: "DELETE" });
        loadBarang();
    }
}

// Muat data saat halaman pertama kali dibuka
loadBarang();