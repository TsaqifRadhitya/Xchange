import function as fn
from tabulate import tabulate
import os
from currency_symbols import CurrencySymbols
import pandas as pd
import datetime as dt
import time as ts
import requests

os.system("cls")
def Landing_page():
    Landing_page = True
    while Landing_page:
        print(f"{'='*240}\n{f'WELCOME TO XCHANGE'.center(240)}\n{'='*240}")
        print("[1] Login\n[2] Register\n[3] Exit")
        opsi = input("Pilihan : ")
        os.system("cls")
        match opsi:
            case "1":
                print(f"{'='*240}\n{f'LOGIN'.center(240)}\n{'='*240}")
                user = input("Username : ")
                pw = input("Password : ")
                os.system("cls")
                autentifikasi = fn.login(user,pw)
                if autentifikasi[0]:
                    main(autentifikasi[1],True)
                    break
                else:
                    print(f"{'='*240}\n{f'LOGIN GAGAL'.center(240)}\n{'='*240}")
                    input("Tekan Enter Untuk Kembali ")
                    os.system("cls")
            case "2":
                register = True
                while register:
                    print(f"{'='*240}\n{f'REGISTER'.center(240)}\n{'='*240}")
                    nama = input("Nama : ")
                    username = input("Username : ")
                    password = input("Password : ")
                    os.system("cls")
                    while True:
                        print(f"{'='*240}\n{f'REGISTER'.center(240)}\n{'='*240}")
                        print(f"Nama : {nama}\nUsername : {username}\nPassword : {password}")
                        print("[1] konfirmasi\n[2] Ulangi\n[3] Batalkan")
                        opsi = input("Pilihan : ")
                        os.system("cls")
                        match opsi:
                            case "1":
                                verifikasi = fn.register(username,password,nama)
                                if verifikasi[0]:
                                    print(f"{'='*240}\n{f'REGISTER BERHASIL'.center(240)}\n{'='*240}")
                                    input("Tekan Enter Untuk Kembali ")
                                    os.system("cls")
                                    register = False
                                    break
                                else:
                                    if verifikasi[1] == "Data Benar":
                                        print(f"{'='*240}\n{f'USERNAME SUDAH TERDAFTAR'.center(240)}\n{'='*240}")
                                        input("Tekan Enter Untuk Kembali ")
                                        os.system("cls")
                                        register = False
                                        break
                                    else:
                                        print(f"{'='*240}\n{f'REGISTER GAGAL'.center(240)}\n{'='*240}")
                                        input("Tekan Enter Untuk Kembali ")
                                        os.system("cls")
                                        register = False
                                        break
                            case "2":
                                break
                            case "3":
                                print(f"{'='*240}\n{f'REGISTER TELAH DIBATALKAN'.center(240)}\n{'='*240}")
                                input("Tekan Enter Untuk Kembali ")
                                os.system("cls")
                                register = False
                                break
            case "3":
                Landing_page = False
    else:
        print(f"{'='*240}\n{'TERIMA KASIH TELAH MENGGUNAKAN XCHANGE'.center(240)}\n{'='*240}")

def main(admin,acces):
    while acces:
        print(f"{'='*240}\n{'MAIN MENU'.center(240)}\n{'='*240}")
        print("[1] Transaksi Baru\n[2] Riwayat Transaksi\n[3] Kelola Mata Uang\n[4] Live Currency\n[5] Member XCHANGE\n[6] Exit")
        opsi = input("Pilihan : ").upper()
        os.system("cls")
        match opsi :
            case "1":
                member = True
                data_id_member = pd.read_csv("member.csv").iloc[:,:2].values.tolist()
                while member:
                    print(f"{'='*240}\n{'MASUKKAN NOMOR MEMBER'.center(240)}\n{'='*240}")
                    print("Tekan Enter Untuk Kembali")
                    id_member = input("Nomor Member : ").upper()
                    os.system("cls")
                    if id_member == "":
                        member = False
                    elif id_member in [x[0] for x in data_id_member]:
                        nama_pelanggan = [x[1] for x in data_id_member if x[0] == id_member][0]
                        mata_uang_asal_session = True
                        data_mata_uang = [x[:3] for x in fn.mata_uang_tersedia()]
                        while mata_uang_asal_session:
                            print(f"{'='*240}\n{'MATA UANG ASAL'.center(240)}\n{'='*240}")
                            print(tabulate(data_mata_uang,headers=["Nomor","Negara","Kode Mata Uang"],tablefmt="rounded_grid"))
                            print("Tekan Enter Untuk Kembali")
                            opsi = input("Nomor Mata Uang : ")
                            os.system("cls")
                            if opsi == "":
                                mata_uang_asal_session = False
                            elif opsi.isnumeric():
                                if int(opsi) in [x[0] for x in data_mata_uang]:
                                    kode_mata_uang_asal = [x[2] for x in data_mata_uang if int(opsi) == x[0]][0]
                                    nominal_session = True
                                    while nominal_session:
                                        print(f"{'='*240}\n{'NOMINAL PENUKARAN'.center(240)}\n{'='*240}")
                                        print("Tekan Enter Untuk Kembali")
                                        nominal = input("Nominal : ")
                                        os.system("cls")
                                        if nominal == "":
                                            nominal_session = False
                                        elif nominal.isnumeric():
                                            mata_uang_tujuan_session = True
                                            while mata_uang_tujuan_session:
                                                print(f"{'='*240}\n{'MATA UANG TUJUAN'.center(240)}\n{'='*240}")
                                                print(tabulate(data_mata_uang,headers=["Nomor","Negara","Kode Mata Uang"],tablefmt="rounded_grid"))
                                                print("Tekan Enter Untuk Kembali")
                                                opsi = input("Nomor Mata Uang : ")
                                                os.system("cls")
                                                if opsi == "":
                                                    mata_uang_tujuan_session = False
                                                elif opsi.isnumeric():
                                                    if int(opsi) in [x[0] for x in data_mata_uang]:
                                                        kode_mata_uang_tujuan = [x[2] for x in data_mata_uang if int(opsi) == x[0]][0]
                                                        data_knapsack = fn.cari_pecahan(kode_mata_uang_asal,kode_mata_uang_tujuan,int(nominal))
                                                        simbol_mata_uang_tujuan = CurrencySymbols.get_symbol(kode_mata_uang_tujuan)
                                                        pecahan_session = True
                                                        while pecahan_session:
                                                            print(f"{'='*240}\n{'PECAHAN MATA UANG'.center(240)}\n{f'{kode_mata_uang_asal} -----> {kode_mata_uang_tujuan}'.center(240)}\n{'='*240}")
                                                            for x in data_knapsack[0]:
                                                                print(f"{x[0]}{' '*(32-len(x[0]))} : {x[1]}")
                                                            print(f"Nominal Hasil Konversi Mata Uang : {simbol_mata_uang_tujuan}{fn.convert_number_format(str(data_knapsack[2]))}")
                                                            print(f"Total Nominal Pecahan            : {simbol_mata_uang_tujuan}{fn.convert_number_format(str(data_knapsack[1]))}")
                                                            print(f"Sisa Nominal Mata Uang           : {simbol_mata_uang_tujuan}{fn.convert_number_format(str(data_knapsack[3]))}")
                                                            print(" \n[1] Lanjutkan Transaksi\n[2] Batalkan Transaksi")
                                                            opsi = input("Pilihan : ")
                                                            os.system("cls")
                                                            match opsi:
                                                                case "1":
                                                                    metode_pembayaran_session = True
                                                                    while metode_pembayaran_session:
                                                                        print(f"{'='*240}\n{f'METODE PEMBAYARAN'.center(240)}\n{'='*240}")
                                                                        print("[1] Tunai\n[2] Transfer Bank\n[3] Kembali")
                                                                        opsi = input("Pilihan : ") 
                                                                        os.system("cls")
                                                                        match opsi:
                                                                            case "1":
                                                                                invoice_session = True
                                                                                while invoice_session:
                                                                                    invoice = fn.invoice(data_knapsack[0],nama_pelanggan,kode_mata_uang_asal,kode_mata_uang_tujuan,nominal,data_knapsack[2],data_knapsack[1],data_knapsack[3])
                                                                                    print("[1] Konfirmasi\n[2] Batalkan")
                                                                                    opsi = input("Pilihan : ")
                                                                                    os.system("cls")
                                                                                    match opsi:
                                                                                        case "1":
                                                                                            fn.tambah_transaksi(invoice[2],invoice[3],admin,nama_pelanggan,kode_mata_uang_asal,kode_mata_uang_tujuan,invoice[1],invoice[0])
                                                                                            print(f"{'='*240}\n{f'TRANSAKSI BERHASIL'.center(240)}\n{'='*240}")
                                                                                            input("Tekan Enter Untuk Kembali Ke Menu Utama")
                                                                                            os.system("cls")
                                                                                            member,mata_uang_asal_session,nominal_session,mata_uang_tujuan_session,pecahan_session,metode_pembayaran_session,invoice_session = False,False,False,False,False,False,False
                                                                                        case "2":
                                                                                            print(f"{'='*240}\n{f'TRANSAKSI DIBATALKAN'.center(240)}\n{'='*240}")
                                                                                            input("Tekan Enter Untuk Kembali Ke Menu Utama")
                                                                                            os.system("cls")
                                                                                            member,mata_uang_asal_session,nominal_session,mata_uang_tujuan_session,pecahan_session,metode_pembayaran_session,invoice_session = False,False,False,False,False,False,False
                                                                            case "2":
                                                                                bank_session = True
                                                                                while bank_session:
                                                                                    data_bank = fn.bank()
                                                                                    print(f"{'='*240}\n{f'BANK'.center(240)}\n{'='*240}")
                                                                                    print(tabulate(data_bank,headers=["Nomor","Bank"],tablefmt="rounded_grid"))
                                                                                    print("Tekan Enter Untuk Kembali")
                                                                                    opsi = input("Pilihan : ")
                                                                                    os.system("cls")
                                                                                    if opsi.isnumeric():
                                                                                        if int(opsi) in [x[0] for x in data_bank]:
                                                                                            nama_bank = [x[1] for x in data_bank if int(opsi) == x[0]][0]
                                                                                            rekening_session = True
                                                                                            while rekening_session:
                                                                                                print(f"{'='*240}\n{f'NOMOR REKENING'.center(240)}\n{'='*240}")
                                                                                                print("Tekan Enter Untuk Kembali")
                                                                                                rekening = input("Nomor Rekening : ")
                                                                                                os.system("cls")
                                                                                                if rekening.isnumeric():
                                                                                                    pemilik_session = True
                                                                                                    while pemilik_session:
                                                                                                        print(f"{'='*240}\n{f'PEMILIK REKENING'.center(240)}\n{'='*240}")
                                                                                                        print("Tekan Enter Untuk Kembali")
                                                                                                        nama_pemilik_rekening = input("Nama Pemiik Rekening : ")
                                                                                                        os.system("cls")
                                                                                                        if nama_pemilik_rekening == "":
                                                                                                            pemilik_session = False
                                                                                                        elif nama_pemilik_rekening.isnumeric() == False and nama_pemilik_rekening.count(" ") < len(nama_pemilik_rekening):
                                                                                                            invoice_session = True
                                                                                                            while invoice_session:
                                                                                                                data_invoice = fn.invoice(data_knapsack[0],nama_pelanggan,kode_mata_uang_asal,kode_mata_uang_tujuan,nominal,data_knapsack[2],data_knapsack[1],data_knapsack[3],"Transfer Bank",nama_bank,rekening,nama_pemilik_rekening)
                                                                                                                print("[1] Konfirmasi\n[2] Batalkan")
                                                                                                                opsi = input("Pilihan : ")
                                                                                                                os.system("cls")
                                                                                                                match opsi:
                                                                                                                    case "1":
                                                                                                                        fn.tambah_transaksi(data_invoice[2],data_invoice[3],admin,nama_pelanggan,kode_mata_uang_asal,kode_mata_uang_tujuan,data_invoice[1],data_invoice[0],"BANK",nama_bank,rekening,nama_pemilik_rekening)
                                                                                                                        print(f"{'='*240}\n{f'TRANSAKSI BERHASIL'.center(240)}\n{'='*240}")
                                                                                                                        input("Tekan Enter Untuk Kembali Ke Menu Utama")
                                                                                                                        os.system("cls")
                                                                                                                        member,mata_uang_asal_session,nominal_session,mata_uang_tujuan_session,pecahan_session,metode_pembayaran_session,bank_session,rekening_session,pemilik_session,invoice_session = False,False,False,False,False,False,False,False,False,False
                                                                                                                    case "2":
                                                                                                                        print(f"{'='*240}\n{f'TRANSAKSI DIBATALKAN'.center(240)}\n{'='*240}")
                                                                                                                        input("Tekan Enter Untuk Kembali Ke Menu Utama")
                                                                                                                        os.system("cls")
                                                                                                                        member,mata_uang_asal_session,nominal_session,mata_uang_tujuan_session,pecahan_session,metode_pembayaran_session,bank_session,rekening_session,pemilik_session,invoice_session = False,False,False,False,False,False,False,False,False,False
                                                                                                elif rekening == "":
                                                                                                    rekening_session = False
                                                                                    elif opsi == "":
                                                                                        bank_session = False

                                                                            case "3":
                                                                                metode_pembayaran_session = False
                                                                                
                                                                case "2":
                                                                    member,mata_uang_asal_session,nominal_session,mata_uang_tujuan_session,pecahan_session = False,False,False,False,False
                                                                    os.system("cls")
                                                        
            case "2":
                riwayat_session = True
                data_transaksi = fn.tampilkan_transaksi()
                while riwayat_session:
                    print(f"{'='*240}\n{'RIWAYAT TRANSAKSI'.center(240)}\n{'='*240}")
                    print(tabulate(fn.convert_format_raw_to_currency(data_transaksi),headers=["Tanggal","Jam","Nama Pelayan","Nama Pelanggan","Mata Uang Asal","Mata Uang Tujuan","Rate","Total Pembayaran","Metode Pembayaran","Nama Bank","Nomor Rekening/E-Wallet","Nama Pemilik Rekening/E-Wallet"],tablefmt="rounded_grid"))
                    print("[1] Pencarian\n[2] Urutkan\n[3] Kembali")
                    opsi =input("Pilihan : ")
                    os.system("cls")
                    match opsi:
                        case "1":
                            print(f"{'='*240}\n{'PENCARIAN'.center(240)}\n{'='*240}")
                            pencarian = input("Kata Kunci : ").upper()
                            os.system("cls")
                            data_pencarian = fn.string_matching(data_transaksi,pencarian)
                            pencarian_session = True
                            while pencarian_session:
                                if len(data_pencarian) == 0:
                                    print(f"{'='*240}\n{'TIDAK DITEMUKAN DATA YANG SESUAI'.center(240)}\n{'='*240}")
                                    print("[1] Pencarian Lain\n[2] Kembali")
                                    opsi = input("Pilihan : ")
                                    os.system("cls")
                                    match opsi:
                                        case "1":
                                            print(f"{'='*240}\n{'PENCARIAN'.center(240)}\n{'='*240}")
                                            pencarian = input("Kata Kunci : ").upper()
                                            os.system("cls")
                                            data_pencarian = fn.string_matching(data_transaksi,pencarian)
                                        case "2":
                                            break
                                else:
                                    if len(data_pencarian) > 1:
                                        print(f"{'='*240}\n{'HASIL PENCARIAN'.center(240)}\n{'='*240}")
                                        print(tabulate(fn.convert_format_raw_to_currency(data_pencarian),headers=["Tanggal","Jam","Nama Pelayan","Nama Pelanggan","Mata Uang Asal","Mata Uang Tujuan","Rate","Total Pembayaran","Metode Pembayaran","Nama Bank","Nomor Rekening/E-Wallet","Nama Pemilik Rekening/E-Wallet"],tablefmt="rounded_grid"))
                                        print("[1] Pencarian Lain\n[2] Urutkan\n[3] Kembali")
                                        opsi = input("Pilihan : ")
                                        os.system("cls")
                                        match opsi:
                                            case "1":
                                                print(f"{'='*240}\n{'PENCARIAN'.center(240)}\n{'='*240}")
                                                pencarian = input("Kata Kunci : ").upper()
                                                os.system("cls")
                                                data_pencarian = fn.string_matching(data_transaksi,pencarian)
                                                
                                            case "2":
                                                urutan_session = True
                                                while urutan_session:
                                                    print(f"{'='*240}\n{'KATEGORI PENGURUTAN'.center(240)}\n{'='*240}")
                                                    print("[1] Waktu Transaksi\n[2] Nama Admin\n[3] Nama Pelanggan\n[4] Mata Uang\n[5] Total Transaksi\n[6] Metode Pembayaran\n[7] Kembali")
                                                    opsi = input("Pilihan : ")
                                                    os.system("cls")
                                                    match opsi:
                                                        case "1":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending")
                                                                print("Tekan Enter Untuk Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_waktu_transaksi_asc(data_pencarian)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_waktu_transaksi_asc(data_pencarian)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "":
                                                                        sorting_type_session = False
                                                        case "2":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,2)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,2)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "3":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,3)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,3)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "4":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_2_index_asc(data_pencarian)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_2_index_asc(data_pencarian)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "5":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_total_transaksi_asc(data_pencarian)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_total_transaksi_asc(data_pencarian)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "6":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_3_index_desc(data_pencarian)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_3_index_desc(data_pencarian)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "7":
                                                            urutan_session = False
                                            case "3":
                                                data_transaksi = fn.tampilkan_transaksi()
                                                break
                                    else:
                                        print(f"{'='*240}\n{'HASIL PENCARIAN'.center(240)}\n{'='*240}")
                                        print(tabulate(data_pencarian,headers=["Tanggal","Jam","Nama Pelayan","Nama Pelanggan","Mata Uang Asal","Mata Uang Tujuan","Rate","Total Pembayaran","Metode Pembayaran","Nama Bank","Nomor Rekening/E-Wallet","Nama Pemilik Rekening/E-Wallet"],tablefmt="rounded_grid"))
                                        print("[1] Pencarian Lain\n[2] Kembali")
                                        opsi = input("Pilihan : ")
                                        os.system("cls")
                                        match opsi:
                                            case "1":
                                                print(f"{'='*240}\n{'PENCARIAN'.center(240)}\n{'='*240}")
                                                pencarian = input("Kata Kunci : ").upper()
                                                os.system("cls")
                                                data_pencarian = fn.string_matching(data_transaksi,pencarian)
                                            case "2":
                                                break
                        case "2":
                            urutan_session = True
                            while urutan_session:
                                print(f"{'='*240}\n{'KATEGORI PENGURUTAN'.center(240)}\n{'='*240}")
                                print("[1] Waktu Transaksi\n[2] Nama Admin\n[3] Nama Pelanggan\n[4] Mata Uang\n[5] Total Transaksi\n[6] Metode Pembayaran\n[7] Kembali")
                                opsi = input("Pilihan : ")
                                os.system("cls")
                                match opsi:
                                    case "1":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending")
                                            print("Tekan Enter Untuk Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_transaksi = fn.merge_sort_waktu_transaksi_asc(data_transaksi)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_transaksi = fn.merge_sort_waktu_transaksi_asc(data_transaksi)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "":
                                                    sorting_type_session = False
                                    case "2":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_transaksi = fn.merge_sort_asc(data_transaksi,2)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_transaksi = fn.merge_sort_asc(data_transaksi,2)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "3":
                                                    sorting_type_session = False
                                    case "3":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_transaksi = fn.merge_sort_asc(data_transaksi,3)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_transaksi = fn.merge_sort_asc(data_transaksi,3)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "3":
                                                    sorting_type_session = False
                                    case "4":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_transaksi = fn.merge_sort_2_index_asc(data_transaksi)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_transaksi = fn.merge_sort_2_index_asc(data_transaksi)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "3":
                                                    sorting_type_session = False
                                    case "5":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            rate = 'https://open.er-api.com/v6/latest/IDR'
                                            rate = requests.get(rate).json()['rates']
                                            match opsi:
                                                case "1":
                                                    data_transaksi = fn.merge_sort_total_transaksi_asc(data_transaksi,rate)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_transaksi = fn.merge_sort_total_transaksi_asc(data_transaksi,rate)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "3":
                                                    sorting_type_session = False
                                    case "6":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_transaksi = fn.merge_sort_3_index_desc(data_transaksi)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_transaksi = fn.merge_sort_3_index_desc(data_transaksi)
                                                    sorting_type_session,urutan_session = False,False
                                                case "3":
                                                    sorting_type_session = False
                                    case "7":
                                        urutan_session = False
                        case "3":
                            break
            case "3":
                mata_uang = True
                while mata_uang:
                    print(f"{'='*240}\n{'MATA UANG'.center(240)}\n{'='*240}")
                    data_mata_uang = fn.mata_uang_tersedia()
                    print(tabulate(data_mata_uang,headers=["Nomor","Negara","Mata Uang","Pecahan"],tablefmt="rounded_grid"))
                    print("[1] Tambah Mata Uang\n[2] Hapus Mata Uang\n[3] Ubah Pecahan Mata Uang\n[4] Exit")
                    opsi = input("Pilihan : ")
                    os.system("cls")
                    match opsi:
                        case "1":
                            negara = True
                            data_mata_uang_lain = fn.list_mata_uang_lain()
                            while negara:
                                print(f"{'='*240}\n{'MATA UANG'.center(240)}\n{'='*240}")
                                print(tabulate(data_mata_uang_lain,headers=["Nomor","Negara","Mata Uang"],tablefmt="rounded_grid"))
                                print("Tekan Enter Untuk Kembali")
                                opsi = input("Nomor : ")
                                os.system("cls")
                                if opsi.isnumeric():
                                    if int(opsi) in [x[0] for x in data_mata_uang_lain]:
                                        negara = [x[1] for x in data_mata_uang_lain if x[0] == int(opsi)][0]
                                        kode_mata_uang = [x[2] for x in data_mata_uang_lain if x[0] == int(opsi)][0]
                                        lambang = CurrencySymbols.get_symbol(kode_mata_uang)
                                        pecahan = True
                                        while pecahan:
                                            print(f"{'='*240}\n{'JUMLAH PECAHAN MATA UANG'.center(240)}\n{'='*240}")
                                            print("Tekan Enter Untuk Kembali")
                                            jumlah_pecahan = input("Jumlah Pecahan Mata Uang : ")
                                            os.system("cls")
                                            if jumlah_pecahan.isnumeric():
                                                cari_pecahan = True
                                                list_pecahan = []
                                                index = 1
                                                while cari_pecahan:
                                                    if len(list_pecahan) == int(jumlah_pecahan):
                                                        detail_mata_uang = True
                                                        while detail_mata_uang:
                                                            nilai_pecahan = [x[0] for x in fn.merge_sort_asc([[x] for x in list_pecahan],0)[::-1]]
                                                            string_pecahan = "".join([f"{lambang}{x}," for x in nilai_pecahan])[:-1]
                                                            string_pecahana_tampilan = "".join([f"{lambang}{fn.convert_number_format(str(x))}," for x in nilai_pecahan])[:-1]
                                                            print(f"{'='*240}\n{'DETAIL MATA UANG'.center(240)}\n{'='*240}")
                                                            print(f"Negara : {negara}")
                                                            print(f"Kode Mata Uang : {kode_mata_uang}")
                                                            print(f"Pecahan Mata Uang : {string_pecahana_tampilan}")
                                                            print("[1] Konfirmasi\n[2] Batalkan")
                                                            opsi = input("Pilihan : ")
                                                            os.system("cls")
                                                            match opsi:
                                                                case "1":
                                                                    print(f"{'='*240}\n{'BERHASIL MELAKUKAN PENAMBAHAN MATA UANG BARU'.center(240)}\n{'='*240}")
                                                                    input("Tekan Enter Untuk Kembali ke Menu Utama ")
                                                                    os.system("cls")
                                                                    negara,kode,pecahan,cari_pecahan,detail_mata_uang = False,False,False,False,False
                                                                        
                                                                case "2":
                                                                    print(f"{'='*240}\n{'PENAMBAHAN MATA UANG BARU TELAH DIBATALKAN'.center(240)}\n{'='*240}")
                                                                    input("Tekan Enter Untuk Kembali ke Menu Utama ")
                                                                    os.system("cls")
                                                                    negara,kode,pecahan,cari_pecahan,detail_mata_uang = False,False,False,False,False
                                                                    
                                                    else:
                                                        print(f"{'='*240}\n{f'PECAHAN MATA UANG KE - {index}'.center(240)}\n{'='*240}")
                                                        print("Tekan Enter Untuk Kembali")
                                                        nilai_pecahan = input("Pecahan Mata Uang : ")
                                                        os.system("cls")
                                                        if nilai_pecahan.isnumeric():
                                                            if int(nilai_pecahan) not in list_pecahan:
                                                                list_pecahan.append(int(nilai_pecahan))
                                                                index += 1
                                                        elif nilai_pecahan == "":
                                                            cari_pecahan = False

                                            elif jumlah_pecahan == "":
                                                pecahan = False
                                elif opsi == "":
                                    negara = False
                        case "2":
                            hapus = True
                            while hapus:
                                print(f"{'='*240}\n{'HAPUS MATA UANG'.center(240)}\n{'='*240}")
                                print(tabulate(data_mata_uang,headers=["Nomor","Negara","Mata Uang","Pecahan"],tablefmt="rounded_grid"))
                                print("Tekan Enter Untuk Kembali")
                                opsi = input("Nomor Mata Uang : ")
                                os.system("cls")
                                if opsi.isnumeric():
                                    if int(opsi) in [x[0] for x in data_mata_uang]:
                                        nama_mata_uang = [x[2] for x in data_mata_uang if x[0] == int(opsi)][0]
                                        konfirmasi = True
                                        while konfirmasi:
                                            print(f"{'='*240}\n{f'APAKAH ADA YAKIN AKAN MENGHAPUS MATA UANG {nama_mata_uang}'.center(240)}\n{'='*240}")
                                            print("[1] Yes\n[2] No")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    fn.hapus_mata_uang(nama_mata_uang)
                                                    print(f"{'='*240}\n{'PENGHAPUSAN MATA UANG BERHASIL'.center(240)}\n{'='*240}")
                                                    input("Tekan Enter Untuk Kembali ke Menu Utama ")
                                                    os.system("cls") 
                                                    hapus,konfirmasi = False,False
                                                case "2":
                                                    print(f"{'='*240}\n{'PENGHAPUSAN MATA UANG TELAH DIBATALKAN'.center(240)}\n{'='*240}")
                                                    input("Tekan Enter Untuk Kembali ke Menu Utama ")
                                                    os.system("cls")
                                                    hapus,konfirmasi = False,False
                                elif opsi == "":
                                    hapus = False
                        case "3":
                            edit = True
                            while edit:
                                print(f"{'='*240}\n{'UBAH PECAHAN MATA UANG'.center(240)}\n{'='*240}")
                                print(tabulate(data_mata_uang,headers=["Nomor","Negara","Mata Uang","Pecahan"],tablefmt="rounded_grid"))
                                print("Tekan Enter Untuk Kembali")
                                opsi = input("Nomor Mata Uang : ")
                                os.system("cls")
                                if opsi.isnumeric():
                                    if int(opsi) in [x[0] for x in data_mata_uang]:
                                        negara = [x[1] for x in data_mata_uang if x[0] == int(opsi)][0]
                                        nama_mata_uang = [x[2] for x in data_mata_uang if x[0] == int(opsi)][0]
                                        edit_pecahan = True
                                        while edit_pecahan:
                                            print(f"{'='*240}\n{f'UBAH PECAHAN MATA UANG {nama_mata_uang}'.center(240)}\n{'='*240}")
                                            print("Tekan Enter Untuk Kembali")
                                            opsi = input("Jumlah Pecahan Mata Uang : ")
                                            os.system("cls")
                                            if opsi.isnumeric():
                                                pecahan_mata_uang_baru =[]
                                                input_mata_uang_baru = True
                                                jumlah_pecahan = int(opsi)
                                                lambang = CurrencySymbols.get_symbol(nama_mata_uang)
                                                index = 1
                                                while input_mata_uang_baru:
                                                    if len(pecahan_mata_uang_baru) == jumlah_pecahan:
                                                        pecahan_mata_uang_baru =[x[0] for x in fn.merge_sort_asc([[x] for x in pecahan_mata_uang_baru],0)[::-1]]
                                                        string_pecahan ="".join([f"{lambang}{x}," for x in pecahan_mata_uang_baru])[:-1]
                                                        string_pecahan_tampilan = "".join([f"{lambang}{fn.convert_number_format(str(x))}," for x in pecahan_mata_uang_baru])[:-1]
                                                        konfirmasi = True
                                                        while konfirmasi:
                                                            print(f"{'='*240}\n{'DETAIL PERUBAHAN MATA UANG'.center(240)}\n{'='*240}")
                                                            print(f"Negara : {negara}")
                                                            print(f"Kode Mata Uang : {nama_mata_uang}")
                                                            print(f"Pecahan Mata Uang : {string_pecahan_tampilan}")
                                                            print("[1] Konfirmasi\n[2] Batalkan")
                                                            opsi = input("Pilihan : ")
                                                            os.system("cls")
                                                            match opsi:
                                                                case "1":
                                                                    fn.edit_pecahan_mata_uang(nama_mata_uang,string_pecahan)
                                                                    print(f"{'='*240}\n{f'PEMBAHARUAN PECAHAN MATA UANG {nama_mata_uang} BERHASIL'.center(240)}\n{'='*240}")
                                                                    input("Tekan Enter Untuk Kembali")
                                                                case "2":
                                                                    print(f"{'='*240}\n{f'PEMBAHARUAN PECAHAN MATA UANG {nama_mata_uang} DIBATALKAN'.center(240)}\n{'='*240}")
                                                                    input("Tekan Enter Untuk Kembali")
                                                            os.system("cls")
                                                            edit,edit_pecahan,input_mata_uang_baru,konfirmasi = False,False,False,False
                                                    else:
                                                        print(f"{'='*240}\n{f'PECAHAN MATA UANG KE - {index}'.center(240)}\n{'='*240}")
                                                        print("Tekan Enter Untuk Kembali")
                                                        nilai_pecahan = input("Pecahan Mata Uang : ")
                                                        os.system("cls")
                                                        if nilai_pecahan.isnumeric():
                                                            if int(nilai_pecahan) not in pecahan_mata_uang_baru:
                                                                pecahan_mata_uang_baru.append(int(nilai_pecahan))
                                                                index += 1
                                                        elif nilai_pecahan == "":
                                                            input_mata_uang_baru = False
                                                        
                                            elif opsi == "":
                                                edit_pecahan = False
                                elif opsi == "":
                                    edit = False

                        case "4":
                            mata_uang = False
                    
            case "4":
                data_mata_uang = fn.mata_uang_tersedia() 
                data_mata_uang = [x[:3] for x in data_mata_uang]
                mata_uang = True 
                while mata_uang:
                    print(f"{'='*240}\n{'PILIH NILAI KONVERSI MATA UANG'.center(240)}\n{'='*240}") 
                    print(tabulate(data_mata_uang,headers=["Nomer","Kode Mata Uang","Negara"],tablefmt="rounded_grid")) 
                    print("Tekan Enter Untuk Kembali") 
                    opsi = input("Nomor Mata Uang : ") 
                    os.system("cls") 
                    if opsi.isnumeric(): 
                        if int(opsi) in [x[0] for x in data_mata_uang]: 
                            kode_mata_uang = [x[2] for x in data_mata_uang if x[0] == int(opsi)][0]
                            tanggal = str(dt.date.today()).split('-')[::-1]
                            tanggal = tanggal = f"{tanggal[0]}-{tanggal[1]}-{tanggal[2]}"
                            print(f"{'='*240}\n{f'Nilai Mata Uang dalam {kode_mata_uang}'.center(240)}\n{f'{tanggal} {ts.ctime(ts.time()).split()[-2:-1][0]}'.center(240)}\n{'='*240}") 
                            hasil = fn.nilai_mata_uang(kode_mata_uang)
                            print(tabulate(hasil,headers=["Mata Uang Asal","Rate","Mata Uang Tujuan","Rate"],tablefmt="rounded_grid")) 
                            input("Tekan Enter Untuk Kembali ") 
                            os.system("cls") 
                            mata_uang = False 

                    elif opsi == "": 
                        mata_uang = False 
            case "5":
                data_member_session = True
                data_member = fn.tampilkan_member()
                while data_member_session:
                    print(tabulate(data_member,headers=["ID Member","Nama","Tanggal Lahir","Nomor HP","Jenis Kelamin","Alamat"],tablefmt="rounded_grid"))
                    print("[1] Tambah Member Baru\n[2] Edit Member\n[3] Pencarian\n[4] Urutkan\n[5] Kembali")
                    opsi = input("Pilihan : ")
                    os.system("cls")
                    match opsi:
                        case "1":
                            add_data_member = True
                            while add_data_member:
                                print(f"{'='*240}\n{'NAMA'.center(240)}\n{'='*240}")
                                print("Tekan Enter Untuk Kembali")
                                nama = input("Nama : ").upper()
                                os.system("cls")
                                if nama == "":
                                    add_data_member = False
                                elif nama.count(" ") < len(nama):
                                    tanggal_lahir_session = True
                                    while tanggal_lahir_session:
                                        print(f"{'='*240}\n{'TANGGAL LAHIR'.center(240)}\n{'='*240}")
                                        print("Tekan Enter Untuk Kembali")
                                        tanggal = input("Tanggal Lahir (dd-mm-yyyy) : ").upper()
                                        os.system("cls")
                                        if "-" in tanggal and "".join(tanggal.split("-")).isnumeric() and tanggal.count("-") == 2 and len("".join(tanggal.split("-"))) == 8 and len([x for x in tanggal.split('-')][0]) == 2 and len([x for x in tanggal.split('-')][1]) == 2 and len([x for x in tanggal.split('-')][2]) == 4:
                                            nomer_hp_session = True
                                            while nomer_hp_session:
                                                print(f"{'='*240}\n{'NOMOR HP'.center(240)}\n{'='*240}")
                                                print("Tekan Enter Untuk Kembali")
                                                nomor_hp = input("Nomor HP : ")
                                                os.system("cls")
                                                if nomor_hp.isnumeric() and nomor_hp[0] == '0':
                                                    jenis_kelamin_session = True
                                                    while jenis_kelamin_session:
                                                        print(f"{'='*240}\n{'JENIS KELAMIN'.center(240)}\n{'='*240}")
                                                        print("[1] Pria\n[2] Wanita")
                                                        print("Tekan Enter Untuk Kembali")
                                                        jenis_kelamin = input("Pilihan : ")
                                                        os.system("cls")
                                                        dictionary = {
                                                            '1' : 'PRIA',
                                                            '2' : 'WANITA'
                                                        }
                                                        if jenis_kelamin.isnumeric() and jenis_kelamin in dictionary.keys():
                                                            jenis_kelamin = dictionary[jenis_kelamin]
                                                            alamat_session = True
                                                            while alamat_session:
                                                                print(f"{'='*240}\n{'ALAMAT'.center(240)}\n{'='*240}")
                                                                print("Tekan Enter Untuk Kembali")
                                                                alamat = input("Alamat : ").upper()
                                                                os.system("cls")
                                                                if alamat == "":
                                                                    alamat_session = False
                                                                elif alamat.count(' ') < len(alamat):
                                                                    konfirmasi = True
                                                                    data_member_csv = pd.read_csv('member.csv')
                                                                    data_id = data_member_csv['id member'].tolist()
                                                                    id_teakhir = data_id[-1]
                                                                    numeric_id_terakhir = "".join([x for x in id_teakhir if x.isnumeric()])
                                                                    id_member = f"EX{'0'*(5-len(f'{int(numeric_id_terakhir)+1}'))}{int(numeric_id_terakhir)+1}CHG"
                                                                    while konfirmasi:
                                                                        print(f"{'='*240}\n{'BIODATA MEMBER'.center(240)}\n{'='*240}")
                                                                        print(f"Nomor Member : {id_member}")
                                                                        print(f"Nama : {nama}")
                                                                        print(f"Tanggal Lahir : {tanggal}")
                                                                        print(f"Nomor HP : {nomor_hp}")
                                                                        print(f"Jenis Kelamin : {jenis_kelamin}")
                                                                        print(f"Alamat : {alamat}")
                                                                        print("[1] Konfirmasi\n[2] Batalkan")
                                                                        opsi = input("Pilihan : ")
                                                                        os.system("cls")
                                                                        match opsi:
                                                                            case "1":
                                                                                if fn.tambah_member(id_member,nama,tanggal,nomor_hp,jenis_kelamin,alamat):
                                                                                    print(f"{'='*240}\n{'UPLOAD DATA MEMBER BARU BERHASIL'.center(240)}\n{'='*240}")
                                                                                    input("Tekan Enter Untuk Kembali")
                                                                                    os.system("cls")
                                                                                    data_member = fn.tampilkan_member()
                                                                                    add_data_member,tanggal_lahir_session,nomer_hp_session,jenis_kelamin_session,alamat_session,konfirmasi = False,False,False,False,False,False
                                                                                else:
                                                                                    print(f"{'='*240}\n{'UPLOAD DATA MEMBER BARU GAGAL'.center(240)}\n{'='*240}")
                                                                                    input("Tekan Enter Untuk Kembali")
                                                                                    os.system("cls")
                                                                                    add_data_member,tanggal_lahir_session,nomer_hp_session,jenis_kelamin_session,alamat_session,konfirmasi = False,False,False,False,False,False
                                                                            case "2":
                                                                                print(f"{'='*240}\n{'UPLOAD DATA MEMBER BARU DIBATALKAN'.center(240)}\n{'='*240}")
                                                                                input("Tekan Enter Untuk Kembali")
                                                                                os.system("cls")
                                                                                add_data_member,tanggal_lahir_session,nomer_hp_session,jenis_kelamin_session,alamat_session,konfirmasi = False,False,False,False,False,False

                                                        elif jenis_kelamin == "":
                                                            jenis_kelamin_session = False
                                                elif nomor_hp == "":
                                                    nomer_hp_session = False

                                        elif tanggal == "":
                                            tanggal_lahir_session = False
                        case "2":
                            id_member_session = True
                            while id_member_session:
                                print(f"{'='*240}\n{'MASUKKAN ID MEMBER'.center(240)}\n{'='*240}")
                                print("Tekan Enter Untuk Kembali")
                                id_member = input("ID Member : ").upper()
                                os.system("cls")
                                if id_member == "":
                                    id_member_session = False
                                else:
                                    cari_data_member = [x for x in data_member if x[0] == id_member]
                                    if cari_data_member == []:
                                        while True:
                                            print(f"{'='*240}\n{'DATA MEMBER TIDAK TERSEDIA'.center(240)}\n{'='*240}")
                                            print("[1] Ulangi\n[2] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    break
                                                case "2":
                                                    id_member_session = False
                                                    break
                                    else:
                                        cari_data_member = cari_data_member[0]
                                        data_diri_session = True
                                        while data_diri_session:
                                            print(f"{'='*240}\n{'BIODATA MEMBER'.center(240)}\n{'='*240}")
                                            print(f"ID Member     : {cari_data_member[0]}")
                                            print(f"Nama          : {cari_data_member[1]}")
                                            print(f"Tanggal Lahir : {cari_data_member[2]}")
                                            print(f"Nomor HP      : {cari_data_member[3]}")
                                            print(f"Jenis Kelamin : {cari_data_member[4]}")
                                            print(f"Alamat        : {cari_data_member[5]}\n ")
                                            print("[1] Ubah Nomer Hp\n[2] Ubah Alamat\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    update_nomer_hp_session = True
                                                    while update_nomer_hp_session:
                                                        print(f"{'='*240}\n{'MASUKKAN NOMOR HP'.center(240)}\n{'='*240}")
                                                        print("Tekan Enter Untuk Kembali")
                                                        nomor_hp = input("Nomor Hp : ")
                                                        os.system("cls")
                                                        if nomor_hp == "":
                                                            update_nomer_hp_session = False
                                                        else:
                                                            if nomor_hp.isnumeric() == False or nomor_hp[0] != "0":
                                                                print(f"{'='*240}\n{'MASUKKAN NOMOR HP DENGAN BENAR'.center(240)}\n{'='*240}")
                                                                input("Tekan Enter Untuk Kembali")
                                                                os.system("cls")
                                                            elif nomor_hp == cari_data_member[3]:
                                                                print(f"{'='*240}\n{'MASUKKAN DATA YANG BERBEDA DARI NOMOR HP LAMA'.center(240)}\n{'='*240}")
                                                                input("Tekan Enter Untuk Kembali")
                                                                os.system("cls")
                                                            else:
                                                                konfirmasi_session = True
                                                                while konfirmasi_session:
                                                                    print(f"{'='*240}\n{'BIODATA MEMBER'.center(240)}\n{'='*240}")
                                                                    print(f"ID Member     : {cari_data_member[0]}")
                                                                    print(f"Nama          : {cari_data_member[1]}")
                                                                    print(f"Tanggal Lahir : {cari_data_member[2]}")
                                                                    print(f"Nomor HP      : {nomor_hp}")
                                                                    print(f"Jenis Kelamin : {cari_data_member[4]}")
                                                                    print(f"Alamat        : {cari_data_member[5]}\n ")
                                                                    print("[1] Konfirmasi\n[2] Batalkan")
                                                                    opsi = input("Pilihan : ")
                                                                    os.system("cls")
                                                                    match opsi:
                                                                        case "1":
                                                                            fn.edit_member(cari_data_member[0],nomor_hp,3)
                                                                            print(f"{'='*240}\n{'PEMBARUAN BIODATA MEMBER BERHASIL'.center(240)}\n{'='*240}")
                                                                            input("Tekan Enter Untuk Kembali")
                                                                            data_member = fn.tampilkan_member()
                                                                            os.system("cls")
                                                                            data_diri_session,id_member_session,update_nomer_hp_session,konfirmasi_session = False,False,False,False
                                                                        case "2":
                                                                            print(f"{'='*240}\n{'PEMBARUAN BIODATA MEMBER DIBATALKAN'.center(240)}\n{'='*240}")
                                                                            input("Tekan Enter Untuk Kembali")
                                                                            os.system("cls")
                                                                            data_diri_session,id_member_session,update_nomer_hp_session,konfirmasi_session = False,False,False,False
                                                                
                                                case "2":
                                                    update_alamat_session = True
                                                    while update_alamat_session:
                                                        print(f"{'='*240}\n{'MASUKKAN ALAMAT'.center(240)}\n{'='*240}")
                                                        print("Tekan Enter Untuk Kembali")
                                                        Alamat = input("Alamat : ").upper()
                                                        os.system("cls")
                                                        if Alamat == "":
                                                            update_alamat_session = False
                                                        else:
                                                            if Alamat.isnumeric() or Alamat.count(" ") == len(Alamat):
                                                                print(f"{'='*240}\n{'MASUKKAN ALAMAT DENGAN BENAR'.center(240)}\n{'='*240}")
                                                                input("Tekan Enter Untuk Kembali")
                                                                os.system("cls")
                                                            elif Alamat == cari_data_member[-1]:
                                                                print(f"{'='*240}\n{'MASUKKAN DATA YANG BERBEDA DARI ALAMAT LAMA'.center(240)}\n{'='*240}")
                                                                input("Tekan Enter Untuk Kembali")
                                                                os.system("cls")
                                                            else:
                                                                konfirmasi_session = True
                                                                while konfirmasi_session:
                                                                    print(f"{'='*240}\n{'BIODATA MEMBER'.center(240)}\n{'='*240}")
                                                                    print(f"ID Member     : {cari_data_member[0]}")
                                                                    print(f"Nama          : {cari_data_member[1]}")
                                                                    print(f"Tanggal Lahir : {cari_data_member[2]}")
                                                                    print(f"Nomor HP      : {cari_data_member[3]}")
                                                                    print(f"Jenis Kelamin : {cari_data_member[4]}")
                                                                    print(f"Alamat        : {Alamat}\n ")
                                                                    print("[1] Konfirmasi\n[2] Batalkan")
                                                                    opsi = input("Pilihan : ")
                                                                    os.system("cls")
                                                                    match opsi:
                                                                        case "1":
                                                                            fn.edit_member(cari_data_member[0],Alamat,-1)
                                                                            print(f"{'='*240}\n{'PEMBARUAN BIODATA MEMBER BERHASIL'.center(240)}\n{'='*240}")
                                                                            input("Tekan Enter Untuk Kembali")
                                                                            data_member = fn.tampilkan_member()
                                                                            os.system("cls")
                                                                            data_diri_session,id_member_session,update_alamat_session,konfirmasi_session = False,False,False,False
                                                                        case "2":
                                                                            print(f"{'='*240}\n{'PEMBARUAN BIODATA MEMBER DIBATALKAN'.center(240)}\n{'='*240}")
                                                                            input("Tekan Enter Untuk Kembali")
                                                                            os.system("cls")
                                                                            data_diri_session,id_member_session,update_alamat_session,konfirmasi_session = False,False,False,False
                                                case "3":
                                                    data_diri_session,id_member_session = False,False

                                
                        case "3":
                            print(f"{'='*240}\n{'PENCARIAN'.center(240)}\n{'='*240}")
                            pencarian = input("Kata Kunci : ").upper()
                            os.system("cls")
                            data_pencarian = fn.string_matching(data_member,pencarian)
                            pencarian_session = True
                            while pencarian_session:
                                if len(data_pencarian) == 0:
                                    print(f"{'='*240}\n{'TIDAK DITEMUKAN DATA YANG SESUAI'.center(240)}\n{'='*240}")
                                    print("[1] Pencarian Lain\n[2] Kembali")
                                    opsi = input("Pilihan : ").upper()
                                    os.system("cls")
                                    match opsi:
                                        case "1":
                                            print(f"{'='*240}\n{'PENCARIAN'.center(240)}\n{'='*240}")
                                            pencarian = input("Kata Kunci : ").upper()
                                            os.system("cls")
                                            data_pencarian = fn.string_matching(data_member,pencarian)
                                        case "2":
                                            break 
                                else:
                                    if len(data_pencarian) > 1:
                                        print(f"{'='*240}\n{'HASIL PENCARIAN'.center(240)}\n{'='*240}")
                                        print(tabulate(data_pencarian,headers=["ID Member","Nama","Tanggal Lahir","Nomor HP","Jenis Kelamin","Alamat"],tablefmt="rounded_grid"))
                                        print("[1] Pencarian Lain\n[2] Urutkan\n[3] Kembali")
                                        opsi = input("Pilihan : ").upper()
                                        os.system("cls")
                                        match opsi:
                                            case "1":
                                                print(f"{'='*240}\n{'PENCARIAN'.center(240)}\n{'='*240}")
                                                pencarian = input("Kata Kunci : ").upper()
                                                os.system("cls")
                                                data_pencarian = fn.string_matching(data_member,pencarian)
                                            case "2":
                                                urutan_session = True
                                                while urutan_session:
                                                    print(f"{'='*240}\n{'KATEGORI PENGURUTAN'.center(240)}\n{'='*240}")
                                                    print("[1] ID Member\n[2] Nama\n[3] Tanggal Lahir\n[4] Jenis Kelamin\n[5] Kembali")
                                                    opsi = input("Pilihan : ")
                                                    os.system("cls")
                                                    match opsi:
                                                        case "1":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,0)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,0)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "2":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,1)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,1)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "3":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_date_asc(data_pencarian,2)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_date_asc(data_pencarian,2)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "4":
                                                            sorting_type_session = True
                                                            while sorting_type_session:
                                                                print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                                                print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                                                opsi = input("Pilihan : ")
                                                                os.system("cls")
                                                                match opsi:
                                                                    case "1":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,4)
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "2":
                                                                        data_pencarian = fn.merge_sort_asc(data_pencarian,4)[::-1]
                                                                        sorting_type_session,urutan_session = False,False
                                                                    case "3":
                                                                        sorting_type_session = False
                                                        case "5":
                                                            urutan_session = False
                                            case "3":
                                                break 
                                    else:
                                        print(f"{'='*240}\n{'HASIL PENCARIAN'.center(240)}\n{'='*240}")
                                        print(tabulate(data_pencarian,headers=["ID Member","Nama","Tanggal Lahir","Nomor HP","Jenis Kelamin","Alamat"],tablefmt="rounded_grid"))
                                        print("[1] Pencarian Lain\n[2] Kembali")
                                        opsi = input("Pilihan : ").upper()
                                        os.system("cls")
                                        match opsi:
                                            case "1":
                                                print(f"{'='*240}\n{'PENCARIAN'.center(240)}\n{'='*240}")
                                                pencarian = input("Kata Kunci : ").upper()
                                                os.system("cls")
                                                data_pencarian = fn.string_matching(data_member,pencarian)
                                            case "2":
                                                break 
                        case "4":
                            urutan_session = True
                            while urutan_session:
                                print(f"{'='*240}\n{'KATEGORI PENGURUTAN'.center(240)}\n{'='*240}")
                                print("[1] ID Member\n[2] Nama\n[3] Tanggal Lahir\n[4] Jenis Kelamin\n[5] Kembali")
                                opsi = input("Pilihan : ")
                                os.system("cls")
                                match opsi:
                                    case "1":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending")
                                            print("Tekan Enter Untuk Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_member = fn.merge_sort_asc(data_member,0)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_member = fn.merge_sort_asc(data_member,0)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "":
                                                    sorting_type_session = False
                                    case "2":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_member = fn.merge_sort_asc(data_member,1)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_member = fn.merge_sort_asc(data_member,1)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "3":
                                                    sorting_type_session = False
                                    case "3":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_member = fn.merge_sort_date_asc(data_member,2)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_member = fn.merge_sort_date_asc(data_member,2)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "3":
                                                    sorting_type_session = False
                                    case "4":
                                        sorting_type_session = True
                                        while sorting_type_session:
                                            print(f"{'='*240}\n{'JENIS PENGURUTAN'.center(240)}\n{'='*240}")
                                            print("[1] Ascending\n[2] Descending\n[3] Kembali")
                                            opsi = input("Pilihan : ")
                                            os.system("cls")
                                            match opsi:
                                                case "1":
                                                    data_member = fn.merge_sort_asc(data_member,4)
                                                    sorting_type_session,urutan_session = False,False
                                                case "2":
                                                    data_member = fn.merge_sort_asc(data_member,4)[::-1]
                                                    sorting_type_session,urutan_session = False,False
                                                case "3":
                                                    sorting_type_session = False
                                    case "5":
                                        urutan_session = False
                        case "5":
                            data_member_session = False
            case "6":
                acces = False
    else:
        print(f"{'='*240}\n{'TERIMA KASIH TELAH MENGGUNAKAN XCHANGE'.center(240)}\n{'='*240}")
koneksi = fn.check_connection()

while koneksi == False:
    print(f"{'='*240}\n{'PERIKSA KONEKSI INTERNET ANDA'.center(240)}\n{'='*240}")
    print(f"[1] Retry\n[2] Exit")
    opsi = input("Pilihan : ")
    os.system("cls")
    match opsi:
        case "1":
            koneksi = fn.check_connection()
        case "2":
            break
else:
    Landing_page()