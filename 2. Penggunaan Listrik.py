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
# (yang beda baris 113)
# elif menu == 'Penggunaan Listrik': -> if 'Penggunaan Listrik':
# 2. Penggunaan Listrik
    if 'Penggunaan Listrik':
        st.title('Penggunaan Listrik')

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Total Penggunaan selama Sebulan",
                value=f"{monitor.hitung_total_penggunaan():.2f} kWh"
            )

        with col2:
            st.metric(
                label="Rata-rata Penggunaan per Hari",
                value=f"{monitor.hitung_total_penggunaan()/30:.2f} kWh"
            )

        data_peralatan = []
        for peralatan in monitor.peralatan:
            konsumsi_per_jam = peralatan['total_watt'] / 1000
            konsumsi_per_bulan = konsumsi_per_jam * peralatan['jam_per_hari'] * 30
            data_peralatan.append({
                'Nama Peralatan': peralatan['nama'],
                'Jam Penggunaan per Hari': peralatan['jam_per_hari'],
                'Listrik per Jam (kWh)': konsumsi_per_jam,
                'Listrik selama Sebulan (kWh)': konsumsi_per_bulan,
            })

        peralatan_df = pd.DataFrame(data_peralatan)
        st.subheader("Rincian Penggunaan Listrik per Peralatan")

        # Grafik penggunaan listrik per peralatan
        fig = px.bar(
            peralatan_df,
            x='Nama Peralatan',
            y='Listrik selama Sebulan (kWh)',
            title='Penggunaan Listrik per Peralatan selama Sebulan',
            color='Listrik selama Sebulan (kWh)',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig)

        # Tabel rincian peralatan
        st.dataframe(peralatan_df)

if __name__ == '__main__':
    main()
