import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# kelas monitor listrik
class MonitorListrik:
    def __init__(self):
        """Inisialisasi kelas monitoring listrik"""
        self.peralatan = []
        self.penggunaan_harian = []
        self.tarif_listrik = {
            'R-1': 1500,  # Tarif untuk golongan R-1 (per kWh)
            'R-2': 2000,  # Tarif untuk golongan R-2 (per kWh)
            'R-3': 2500,  # Tarif untuk golongan R-3 (per kWh)
        }
        self.tarif_terpilih = 'R-1'  # Golongan R-1 sebagai default

    # 1.Peralatan Elektronik
    def tambah_peralatan(self, nama, unit, watt, golongan, jam_per_hari):
        """Menambahkan peralatan elektronik dan golongan listrik"""
        self.peralatan.append({
            'nama': nama,
            'unit': unit,
            'watt': watt,
            'total_watt': watt * unit,
            'golongan': golongan,
            'jam_per_hari': jam_per_hari,
        })
        self.update_penggunaan_harian_dengan_peralatan_baru()

    def update_penggunaan_harian_dengan_peralatan_baru(self):
        """Mengupdate penggunaan harian dengan peralatan baru"""
        if not self.penggunaan_harian:
            self.generate_sample_data()
        else:
            new_usage = np.random.uniform(1, 5)
            self.penggunaan_harian.append({
                'hari': len(self.penggunaan_harian) + 1,
                'penggunaan': new_usage
            })

    def set_tarif_listrik(self, golongan):
        """Set golongan listrik yang dipilih"""
        self.tarif_terpilih = golongan

    # 2.Penggunaan Listrik
    def hitung_total_penggunaan(self):
        """Menghitung total penggunaan listrik dalam kWh per bulan"""
        total_penggunaan_per_bulan = 0
        for peralatan in self.peralatan:
            total_penggunaan_per_bulan += (peralatan['total_watt'] / 1000) * peralatan['jam_per_hari'] * 30
        return total_penggunaan_per_bulan

    # 3.Estimasi Biaya
    def hitung_estimasi_biaya(self):
        """Menghitung estimasi biaya listrik"""
        total_penggunaan_per_bulan = self.hitung_total_penggunaan()
        tarif = self.tarif_listrik.get(self.tarif_terpilih, 1500)
        return total_penggunaan_per_bulan * tarif

    def generate_sample_data(self, hari=30):
        """Menghasilkan data penggunaan listrik sampel"""
        np.random.seed(42)
        self.penggunaan_harian = []
        for hari in range(1, hari + 1):
            penggunaan = np.random.uniform(5, 15)
            self.penggunaan_harian.append({
                'hari': hari,
                'penggunaan': penggunaan
            })

    def konsumsi_energi_per_peralatan(self):
        """Menghitung konsumsi energi per peralatan"""
        return [
            {'peralatan': peralatan['nama'], 'konsumsi': (peralatan['total_watt'] / 1000) * peralatan['jam_per_hari'] * 30}
            for peralatan in self.peralatan
        ]

# Input data
def main():
    if 'monitor' not in st.session_state:
        monitor = MonitorListrik()

        # Menambahkan peralatan default
        peralatan_default = [
            ('Kulkas', 1, 800, 'R-1', 24),
            ('AC', 1, 2000, 'R-1', 8),
            ('Mesin Cuci', 1, 1500, 'R-1', 2),
            ('Lampu LED', 5, 20, 'R-1', 12),
            ('Kipas Angin', 2, 75, 'R-1', 8),
            ('Setrika', 1, 2000, 'R-1', 1),
            ('TV LED', 1, 200, 'R-1', 6),
            ('Rice Cooker', 1, 1000, 'R-1', 2),
            ('Laptop', 1, 300, 'R-1', 8),
            ('Microwave', 1, 1200, 'R-1', 0.5),
            ('Pemanas Air', 1, 3000, 'R-1', 1),
            ('Blender', 1, 700, 'R-1', 0.5),
            ('Hair Dryer', 1, 1800, 'R-1', 0.5),
            ('Kamera Pengawas', 2, 15, 'R-1', 24),
            ('PC', 1, 200, 'R-1', 6)
        ]

        for nama, unit, watt, golongan, jam in peralatan_default:
            monitor.tambah_peralatan(nama, unit, watt, golongan, jam)

        st.session_state.monitor = monitor

    monitor = st.session_state.monitor

# Pelajarin masing-masing 
# (yang beda baris 111)
# elif menu == 'Saran Penggunaan': ->  if 'Saran Penggunaan':
# 4. Saran Penggunaan 
    if 'Saran Penggunaan':
        st.title('Saran Penggunaan Listrik')

        col1, col2 = st.columns(2)

        saran_penggunaan = []
        total_penggunaan_saat_ini = 0
        total_penggunaan_saran = 0

        for peralatan in monitor.peralatan:
            penggunaan_saat_ini = (peralatan['total_watt'] / 1000) * peralatan['jam_per_hari'] * 30
            saran_jam = min(peralatan['jam_per_hari'], 4) if peralatan['nama'] not in ['Kulkas', 'Kamera Pengawas'] else peralatan['jam_per_hari']
            penggunaan_saran_peralatan = (peralatan['total_watt'] / 1000) * saran_jam * 30

            saran_penggunaan.append({
                'Nama Peralatan': peralatan['nama'],
                'Penggunaan Saat Ini (Jam)': peralatan['jam_per_hari'],
                'Saran Penggunaan (Jam)': saran_jam,
                'Listrik Saat Ini (kWh)': penggunaan_saat_ini,
                'Listrik Setelah Saran (kWh)': penggunaan_saran_peralatan
            })

            total_penggunaan_saat_ini += penggunaan_saat_ini
            total_penggunaan_saran += penggunaan_saran_peralatan

        with col1:
            st.metric(
                label="Penggunaan Listrik Saat Ini",
                value=f"{total_penggunaan_saat_ini:.2f} kWh"
            )

        with col2:
            st.metric(
                label="Penggunaan Setelah Saran",
                value=f"{total_penggunaan_saran:.2f} kWh"
            )

        potensi_penghematan = total_penggunaan_saat_ini - total_penggunaan_saran
        potensi_penghematan_biaya = potensi_penghematan * monitor.tarif_listrik[monitor.tarif_terpilih]
        
        st.metric(
            label="Potensi Penghematan per Bulan",
            value=f"{potensi_penghematan:.2f} kWh (Rp {potensi_penghematan_biaya:,.2f})"
        )

        saran_df = pd.DataFrame(saran_penggunaan)
        st.subheader("Rincian Saran Penggunaan Listrik")
        
        # Grafik perbandingan penggunaan listrik saat ini vs saran
        fig = px.bar(
            saran_df,
            x='Nama Peralatan',
            y=['Listrik Saat Ini (kWh)', 'Listrik Setelah Saran (kWh)'],
            title='Perbandingan Penggunaan Listrik: Saat Ini vs Saran',
            barmode='group'
        )
        st.plotly_chart(fig)
        
        # Kemudian tabel
        st.dataframe(saran_df)

if __name__ == '__main__':
    main()
