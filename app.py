import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# kelas monitor listrik?
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

# Sidebar
    st.sidebar.title('⚡Aplikasi Monitor Listrik')
    menu = st.sidebar.radio('Pilih Halaman', [
        'Dashboard',
        'Peralatan Elektronik',
        'Penggunaan Listrik',
        'Estimasi Biaya',
        'Saran Penggunaan'
    ])

# 0.Dashboard / APP  
    if menu == 'Dashboard':
        st.title('Dashboard Penggunaan Listrik')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Total Penggunaan (kWh/bulan)",
                value=f"{monitor.hitung_total_penggunaan():.2f}"
            )
        
        with col2:
            st.metric(
                label="Jumlah Peralatan",
                value=len(monitor.peralatan)
            )
            
        with col3:
            st.metric(
                label="Estimasi Biaya (Rp/bulan)",
                value=f"{monitor.hitung_estimasi_biaya():,.2f}"
            )
        
        # Grafik penggunaan harian
        penggunaan_df = pd.DataFrame(monitor.penggunaan_harian)
        fig_line = px.line(
            penggunaan_df,
            x='hari',
            y='penggunaan',
            title='Penggunaan Listrik Harian'
        )
        st.plotly_chart(fig_line)
        
        # Grafik konsumsi per peralatan
        konsumsi_peralatan = monitor.konsumsi_energi_per_peralatan()
        peralatan_df = pd.DataFrame(konsumsi_peralatan)
        fig_pie = px.pie(
            peralatan_df,
            values='konsumsi',
            names='peralatan',
            title='Distribusi Konsumsi Energi per Peralatan'
        )
        st.plotly_chart(fig_pie)

# Pelajarin masing-masing
# 1.Peralatan elektronik
    elif menu == 'Peralatan Elektronik':
        st.title('Peralatan Elektronik')

        tab1, tab2 = st.tabs(["Daftar Elektronik", "Tambah Elektronik"])

        with tab1:
            if monitor.peralatan:
                data_peralatan = [{
                    'Nama Peralatan': peralatan['nama'],
                    'Golongan Listrik': peralatan['golongan'],
                    'Jumlah Unit': peralatan['unit'],
                    'Daya per Unit (Watt)': peralatan['watt'],
                    'Total Daya (Watt)': peralatan['total_watt'],
                    'Jam Penggunaan per Hari': peralatan['jam_per_hari']
                } for peralatan in monitor.peralatan]

                peralatan_df = pd.DataFrame(data_peralatan)
                st.subheader("Daftar Peralatan Elektronik")
                # Menampilkan grafik terlebih dahulu
                fig_pie = px.pie(
                    peralatan_df,
                    values='Total Daya (Watt)',
                    names='Nama Peralatan',
                    title='Distribusi Daya per Peralatan'
                )
                st.plotly_chart(fig_pie)
                # Kemudian tabel
                st.dataframe(peralatan_df)
            
        with tab2:
           with st.form('Tambah Peralatan', clear_on_submit=True):
                st.subheader("Formulir Tambah Peralatan Elektronik")
                
                col1, col2 = st.columns(2)

                with col1:
                    golongan = st.selectbox('Golongan Listrik', ['R-1', 'R-2', 'R-3'])
                    nama = st.text_input('Nama Peralatan')
                    unit = st.number_input('Jumlah Unit', min_value=1, value=1)

                with col2:
                    jam_per_hari = st.number_input('Waktu Penggunaan per Hari (Jam)', min_value=0.1, value=1.0)
                    watt = st.number_input('Daya per Unit (Watt)', min_value=1)

                submit = st.form_submit_button('Tambah')

                if submit:
                    monitor.tambah_peralatan(nama, unit, watt, golongan, jam_per_hari)
                    st.success(f'Peralatan {nama} berhasil ditambahkan!')

# 2.Penggunaan listrik
    elif menu == 'Penggunaan Listrik':
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
        
        # Kemudian tabel
        st.dataframe(peralatan_df)

# 3.Estimasi Biaya
    elif menu == 'Estimasi Biaya':
        st.title('Estimasi Biaya Listrik')

        total_biaya = monitor.hitung_estimasi_biaya()
        st.metric(
            label="Estimasi Total Biaya selama Sebulan",
            value=f"Rp {total_biaya:,.2f}"
        )

        data_peralatan = []
        for peralatan in monitor.peralatan:
            konsumsi = (peralatan['total_watt'] / 1000) * peralatan['jam_per_hari'] * 30
            biaya_per_peralatan = konsumsi * monitor.tarif_listrik[peralatan['golongan']]
            data_peralatan.append({
                'Nama Peralatan': peralatan['nama'],
                'Listrik Sebulan (kWh)': konsumsi,
                'Biaya Listrik (Rp)': biaya_per_peralatan
            })

        peralatan_df = pd.DataFrame(data_peralatan)
        st.subheader("Rincian Biaya Listrik per Peralatan")

        # Grafik distribusi biaya listrik
        fig = px.bar(
            peralatan_df,
            x='Nama Peralatan',
            y='Biaya Listrik (Rp)',
            title='Distribusi Biaya Listrik per Peralatan',
            color='Biaya Listrik (Rp)',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig)

        # Kemudian tabel
        st.dataframe(peralatan_df)

# 4.Saran Penggunaan
    elif menu == 'Saran Penggunaan':
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

if __name__ == "__main__":
    main()