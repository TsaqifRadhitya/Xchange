import pandas as pd
import datetime as dt
from currency_symbols import CurrencySymbols
import socket
import requests
from tabulate import tabulate
import time as ts

# untuk mengecek koneksi internet
def check_connection():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except :
        return False
    
# untuk melakukan request login
def login(user,password):
    data = pd.read_csv('admin.csv')
    lokasi_user = [x for x in range(len(data['Username'].tolist())) if user == data['Username'].tolist()[x]]
    if len(lokasi_user) > 0:
        if password == data['Password'].tolist()[lokasi_user[0]]:
            nama_admin = data['Nama'].tolist()[lokasi_user[0]]
            return True,nama_admin
        else:
            return False,None
    else:
        return False,None
    
# untuk melakukan register akun
def register(user,pw,nama):
    data_lama = pd.read_csv('admin.csv')
    if user != "" and user.count(" ") < len(user) and pw != "" and pw.count(" ") < len(pw) and nama != "" and nama.count(" ") < len(nama):
        if user not in data_lama['Username'].tolist():
            data = {
                "Username" : [user],
                "Password" : [pw],
                "Nama" : [nama]
            }
            data = pd.DataFrame(data)
            data_baru = pd.concat([data_lama,data])
            data_baru.to_csv('admin.csv',index=False)
            return True,"Data Benar"
        else:
            return False,"Data Benar"
    else:
        return False,"Data Salah"

# Untuk Konversi Mata Uang
def konversi_mata_uang(mata_uang_asal,mata_uang_tujuan,nominal):
    url = f'https://open.er-api.com/v6/latest/{mata_uang_asal}'
    response = requests.get(url)
    data = response.json()
    rate_mata_uang= data['rates'][mata_uang_tujuan]
    Hasil_konversi = nominal * rate_mata_uang
    if 'e' in str(Hasil_konversi):
        desimal = str(Hasil_konversi).split('e-')
        desimal[0] = ''.join([x for x in desimal[0] if x != '.'])
        Hasil_konversi = f"0.{'0' *(int(desimal[1])-1)}{desimal[0]}"
    return (f"{Hasil_konversi} {mata_uang_tujuan}",Hasil_konversi)

# Fitur 1 
def cari_pecahan(mata_uang_asal,mata_uang_tujuan,nominal):
    hasil = konversi_mata_uang(mata_uang_asal,mata_uang_tujuan,nominal)
    simbol = CurrencySymbols.get_symbol(mata_uang_tujuan)
    data_knapsack = pd.read_csv('mata_uang.csv',dtype=str)
    lokasi_index = [x for x in range(len(data_knapsack['kode_mata_uang'].tolist())) if data_knapsack['kode_mata_uang'].tolist()[x] == mata_uang_tujuan][0]
    parameter_knapsack ={
        "items" : data_knapsack.iloc[lokasi_index,2].split(","),
        "values" : [int("".join([x for x in x if x.isnumeric()])) for x in data_knapsack.iloc[lokasi_index,2].split(",")]
    }
    hasil_konversi =int(hasil[1])
    pecahan,max_value = greedy_knapsack(parameter_knapsack['values'],parameter_knapsack['items'],hasil_konversi)
    kumpulan_pecahan = []
    
    for x in parameter_knapsack['items']:
        jumlah = 0
        for y in pecahan:
            if x == y:
                jumlah += 1
        if jumlah != 0:
            x = convert_number_format("".join([x for x in x if x.isnumeric()]))
            kumpulan_pecahan.append([f"{simbol}{x}",f"{jumlah} Lembar"])
    return kumpulan_pecahan,max_value,hasil[1],float(hasil[1])-max_value

def invoice(pecahan,nama_customer,mata_uang_asal,mata_uang_tujuan,Nominal_mata_uang_awal,Nominal_mata_uang_tujuan,total_nominal_pecahan,sisa_nominal,metode_pembayaran = 'Tunai',nama_bank = '-',Nomor_rekening = '-',nama_pemilik = '-'):
    print(f"{'='*240}'\n{'DETAIL TRANSAKSI'.center(240)}\n{'='*240}")
    rate = konversi_mata_uang(mata_uang_tujuan,mata_uang_asal,1)[1]
    simbol_asal = CurrencySymbols.get_symbol(mata_uang_asal)
    simbol_tujuan = CurrencySymbols.get_symbol(mata_uang_tujuan)
    tanggal = str(dt.date.today()).split('-')[::-1]
    tanggal = f"{tanggal[0]}-{tanggal[1]}-{tanggal[2]}"
    jam = ts.ctime(ts.time()).split()[-2:-1][0]
    for x in pecahan:
        print(f"{x[0]}{' '*(41-len(x[0]))} : {x[1]}")
    print('-'*240)
    print(f"Tanggal Transaksi                         : {tanggal}")
    print(f"Jam Transaksi                             : {jam}")
    print(f"Nama Customer                             : {nama_customer}")
    print(f"Metode Pembayaran                         : {metode_pembayaran}")
    if metode_pembayaran != 'Tunai':
        print(f"Nama Bank                                 : {nama_bank}")
        print(f"Nomor Rekening                            : {Nomor_rekening}")
        print(f"Nama Pemilik Rekening                     : {nama_pemilik}")
    print(f"Mata Uang Asal                            : {mata_uang_asal}")
    print(f"Mata Uang Tujuan                          : {mata_uang_tujuan}")
    print(f"Nominal Mata Uang Awal                    : {simbol_asal}{convert_number_format(str(Nominal_mata_uang_awal))}")
    print(f"Nominal Mata Uang Tujuan                  : {simbol_tujuan}{(convert_number_format(str(Nominal_mata_uang_tujuan)))}")
    print(f"Rate Mata Uang                            : {simbol_asal}{convert_number_format(str(rate))}")
    print(f"Total Nominal Pecahan                     : {simbol_tujuan}{convert_number_format(str(total_nominal_pecahan))}")
    sisa = konversi_mata_uang(mata_uang_tujuan,mata_uang_asal,sisa_nominal)[1]
    print(f"Sisa Nominal Pecahan                      : {simbol_asal}{convert_number_format(str(sisa))}")
    print(f"Biaya Admin                               : {simbol_asal}{convert_number_format(str((int(Nominal_mata_uang_awal)-sisa)*0.05))}")
    print(f"Total                                     : {simbol_asal}{convert_number_format(str((int(Nominal_mata_uang_awal)-sisa)*1.05))}")
    return f"{(int(Nominal_mata_uang_awal)-sisa)*1.05} {mata_uang_asal}" ,rate,tanggal,jam

def tambah_transaksi(tanggal,jam,pegawai,pelanggan,mata_uang_asal,mata_uang_tujuan,rate,Nominal,metode='TUNAI',nama_bank = '-',no_rek='-',pemilik='-'):
    data = {
        "Tanggal" : [tanggal],
        "Jam" : [jam],
        "Pegawai" : [pegawai.upper()],
        "Pelanggan" : [pelanggan.upper()],
        "Mata Uang Asal" : [mata_uang_asal.upper()],
        "Mata Uang Tujuan" : [mata_uang_tujuan.upper()],
        "rate" : [f'{rate} {mata_uang_asal}'],
        "Nominal Pembayaran" : [Nominal],
        "Metode Pembayaran" : [metode],
        "nama_bank" : [nama_bank.upper()],
        "Nomor Rekening" : [no_rek],
        "Pemilik Rekening" : [pemilik.upper()]
    }
    data = pd.DataFrame(data)
    data_lama = pd.read_csv('transaksi.csv')
    data_baru = pd.concat([data_lama,data])
    data_baru.to_csv('transaksi.csv',index=False)

def bank():
    data = pd.read_csv('bank.csv')
    data = data.values.tolist()
    for x in range(len(data)):
        data[x].insert(0,x+1)
    return data

# Fitur 2

def tampilkan_transaksi():
    data = pd.read_csv('transaksi.csv',dtype=str)
    data = data.values.tolist()
    return data

def convert_format_raw_to_currency(data):
    hasil = []
    for x in data:
        temporal = []
        for y in range(len(x)):
            data_raw_index_6 = x[6].split(" ")
            data_raw_index_6[0] = convert_number_format(data_raw_index_6[0])
            data_raw_index_7 = x[7].split(" ")
            data_raw_index_7[0] = convert_number_format(data_raw_index_7[0])
            if y == 6:
                temporal.append(f"{CurrencySymbols.get_symbol(data_raw_index_6[1])}{data_raw_index_6[0]}")
            elif y == 7:
                temporal.append(f"{CurrencySymbols.get_symbol(data_raw_index_7[1])}{data_raw_index_7[0]}")
            else:
                temporal.append(x[y])
        hasil.append(temporal)
    return hasil

# Fitur 3

def tambah_mata_uang(negara,kode,pecahan):
    data_lama = pd.read_csv('mata_uang.csv')
    data = {
           "Negara" : [negara.upper()],
            "kode_mata_uang" : [kode.upper()],
            "pecahan" : [pecahan]
        }
    data = pd.DataFrame(data)
    data_baru = pd.concat([data_lama,data])
    data_baru.to_csv('mata_uang.csv',index=False)
    
def list_mata_uang_lain():
    data_mata_uang = pd.read_csv('mata_uang.csv')['kode_mata_uang'].tolist()
    data_mata_uang_API = pd.read_csv('Mata Uang Support API.csv').values.tolist()
    output = []

    for x in data_mata_uang_API:
        if x[1] not in data_mata_uang:
            output.append(x)
    output = merge_sort_asc(output,0)

    for x in range(len(output)):
        output[x].insert(0,x+1)
    return output

def hapus_mata_uang(kode):
    data = pd.read_csv('mata_uang.csv')
    lokasi = [x for x in range(len(data['kode_mata_uang'].tolist())) if data['kode_mata_uang'].tolist()[x] == kode ][0]
    data = data.drop(data.index[lokasi])
    data.to_csv('mata_uang.csv',index=False)

def edit_pecahan_mata_uang(kode,pecahan):
    data = pd.read_csv('mata_uang.csv')
    lokasi = [x for x in range(len(data['kode_mata_uang'].tolist())) if data['kode_mata_uang'].tolist()[x] == kode ][0]
    data.iloc[[lokasi],[2]] = pecahan
    data.to_csv('mata_uang.csv',index=False)

# Fitur 4
def mata_uang_tersedia():
    data = pd.read_csv('mata_uang.csv')
    data = data.values.tolist()
    data = merge_sort_asc(data,0)
    for x in range(len(data)):
        data[x].insert(0,x+1)
    for x in range(len(data)):
        lambang_mata_uang = CurrencySymbols.get_symbol(data[x][2])
        data_raw =  data[x][3].split(",")
        data_modification = ["".join([x for x in x if x.isnumeric()]) for x in data_raw]
        data_modification = [f"{lambang_mata_uang}{convert_number_format(x)}," for x in data_modification]
        data[x][3] = "".join(data_modification)[:-1]
    return data

def nilai_mata_uang(mata_uang_tujuan):
    rate = f'https://open.er-api.com/v6/latest/{mata_uang_tujuan}'
    rate = requests.get(rate).json()['rates']
    data_mata_uang = pd.read_csv('mata_uang.csv')
    data_mata_uang = data_mata_uang['kode_mata_uang'].tolist()
    data_mata_uang = merge_sort_asc([[x] for x in data_mata_uang],0)
    data_mata_uang = [x[0] for x in data_mata_uang]
    hasil = []
    for x in data_mata_uang:
        if x != mata_uang_tujuan:
            hasil_konversi = 1/float(rate[x])
            if 'e' in str(hasil_konversi):
                desimal = str(hasil_konversi).split('e-')
                desimal[0] = ''.join([x for x in desimal[0] if x != '.'])
                hasil_konversi = f"0.{'0' *(int(desimal[1])-1)}{desimal[0]}"
            hasil.append([x,f"{CurrencySymbols.get_symbol(x)}1,00",mata_uang_tujuan,f"{CurrencySymbols.get_symbol(mata_uang_tujuan)}{convert_number_format(str(hasil_konversi))}"])
    return hasil

# Fitur 5

def tampilkan_member():
    data = pd.read_csv('member.csv',dtype=str)
    data = data.values.tolist()
    return data

def tambah_member(id_member,nama,tanggal_lahir,nomer_hp,jenis_kelamin,alamat):
    data_lama = pd.read_csv('member.csv',dtype=str)
    data_nama = data_lama['nama'].tolist()
    data_nomer_hp = data_lama['nomer hp'].tolist()
    if nama in data_nama or nomer_hp in data_nomer_hp:
        return False
    else:
        data = {
            'id member' : [id_member],
            'nama' : [nama],
            'tanggal lahir' : [tanggal_lahir],
            'nomer hp' : [nomer_hp],
            'jenis kelamin' : [jenis_kelamin],
            'alamat' : [alamat]
        }
        data_baru = pd.concat([data_lama,pd.DataFrame(data)])
        data_baru.to_csv('member.csv',index=False)
        return True

def edit_member(id_member,data_baru,lokasi_index_shell):
    data = pd.read_csv('member.csv').values.tolist()
    index = [x for x in range(len(data)) if data[x][0] == id_member][0]
    data[index][lokasi_index_shell] = data_baru
    data = pd.DataFrame(data,columns=["id member","nama","tanggal lahir","nomer hp","jenis kelamin","alamat"])
    data.to_csv('member.csv',index=False)

# algoritma

def string_matching(data,pecaharian):
    if len(pecaharian) >0:
        lokasi_index = []
        for list_2_dimensi in range(len(data)):
                found = False
                for value in data[list_2_dimensi]:
                    if found:
                        break
                    elif len(value) >= len(pecaharian):
                        for z in range(len(value)+1-len(pecaharian)):
                            if value[z] == pecaharian[0]:
                                for c in range(1,len(pecaharian)):
                                    if pecaharian[c] != value[z+c]:
                                        break
                                else:
                                    lokasi_index.append(list_2_dimensi)
                                    found = True
                                    break
        hasil_pencarian = []
        for x in lokasi_index:
            hasil_pencarian.append(data[x])
        return hasil_pencarian
    else:
        return []


# knapack
def greedy_knapsack(values,item,nominal):
    sisa_nominal = nominal
    hasil = []
    for x in range(len(values)):
        while values[x] <= sisa_nominal:
            hasil.append(item[x])
            sisa_nominal -= values[x]
    return(hasil,nominal-sisa_nominal)

# Merger Sort
    
def merge_sort_asc(arr,index):
    if len(arr) == 1:
        return arr
    else:
        kiri = merge_sort_asc(arr[:len(arr)//2],index)
        kanan = merge_sort_asc(arr[len(arr)//2:],index)
        hasil = []
        while len(kiri) > 0 and len(kanan)>0:
            if kiri[0][index] < kanan[0][index]:
                hasil.append(kiri.pop(0))
            else:
                hasil.append(kanan.pop(0))

        while len(kiri) >0:
            hasil.append(kiri.pop(0))

        while len(kanan) > 0 :
            hasil.append(kanan.pop(0))

        return hasil
    
def merge_sort_date_asc(arr,index):
    if len(arr) == 1:
        return arr
    else:
        kiri = merge_sort_date_asc(arr[:len(arr)//2],index)
        kanan = merge_sort_date_asc(arr[len(arr)//2:],index)
        hasil = []
        while len(kiri) > 0 and len(kanan)>0:
            tanggal_kanan = kanan[0][index].split("-")
            tanggal_kiri = kiri[0][index].split("-")
            if int(tanggal_kiri[2]) < int(tanggal_kanan[2]):
                hasil.append(kiri.pop(0))
            elif int(tanggal_kiri[2]) == int(tanggal_kanan[2]):
                if int(tanggal_kiri[1]) < int(tanggal_kanan[1]):
                    hasil.append(kiri.pop(0))
                elif int(tanggal_kiri[1]) == int(tanggal_kanan[1]):
                    if int(tanggal_kiri[0]) < int(tanggal_kanan[0]):
                        hasil.append(kiri.pop(0))
                    else:
                        hasil.append(kanan.pop(0))
                else:
                    hasil.append(kanan.pop(0))
            else:
                hasil.append(kanan.pop(0))

        while len(kiri) > 0:
            hasil.append(kiri.pop(0))

        while len(kanan)>0 :
            hasil.append(kanan.pop(0))

        return hasil
    
def merge_sort_waktu_transaksi_asc(arr):
    if len(arr) == 1:
        return arr
    else:
        kiri = merge_sort_waktu_transaksi_asc(arr[:len(arr)//2])
        kanan = merge_sort_waktu_transaksi_asc(arr[len(arr)//2:])
        hasil = []
        
        while len(kiri) > 0 and len(kanan) > 0:
            tanggal_kanan = kanan[0][0].split("-")
            tanggal_kiri = kiri[0][0].split("-")
            if int(tanggal_kiri[2]) < int(tanggal_kanan[2]):
                hasil.append(kiri.pop(0))
            elif int(tanggal_kiri[2]) == int(tanggal_kanan[2]):
                if int(tanggal_kiri[1]) < int(tanggal_kanan[1]):
                    hasil.append(kiri.pop(0))
                elif int(tanggal_kiri[1]) == int(tanggal_kanan[1]):
                    if int(tanggal_kiri[0]) < int(tanggal_kanan[0]):
                        hasil.append(kiri.pop(0))
                    elif int(tanggal_kiri[0]) == int(tanggal_kanan[0]):
                        if kiri[0][1] < kanan[0][1]:
                            hasil.append(kiri.pop(0))
                        else:
                            hasil.append(kanan.pop(0))
                    else:
                        hasil.append(kanan.pop(0))
                else:
                    hasil.append(kanan.pop(0))
            else:
                hasil.append(kanan.pop(0))
            
        while len(kiri) > 0:
            hasil.append(kiri.pop(0))

        while len(kanan) > 0:
            hasil.append(kanan.pop(0))

        return hasil
    
def merge_sort_2_index_asc(arr):
    if len(arr) == 1:
        return arr
    else:
        kiri = merge_sort_2_index_asc(arr[:len(arr)//2])
        kanan = merge_sort_2_index_asc(arr[len(arr)//2:])
        hasil = []
        while len(kiri) > 0 and len(kanan) > 0:
            if kiri[0][4] < kanan[0][4]:
                hasil.append(kiri.pop(0))
            elif kiri[0][4] == kanan[0][4]:
                if kiri[0][5] < kanan[0][5]:
                    hasil.append(kiri.pop(0))
                else:
                    hasil.append(kanan.pop(0))
            else:
                hasil.append(kanan.pop(0))

        while len(kiri) > 0:
            hasil.append(kiri.pop(0))

        while len(kanan) > 0:
            hasil.append(kanan.pop(0))

        return hasil

def merge_sort_3_index_desc(arr):
    if len(arr) == 1:
        return arr
    else:
        kiri = merge_sort_3_index_desc(arr[:len(arr)//2])
        kanan = merge_sort_3_index_desc(arr[len(arr)//2:])
        hasil = []
        while len(kiri) > 0 and len(kanan) > 0:
            if kiri[0][8] > kanan[0][8]:
                hasil.append(kiri.pop(0))
            elif kiri[0][8] == kanan[0][8]:
                if kiri[0][9] > kanan[0][9]:
                    hasil.append(kiri.pop(0))
                elif kiri[0][9] == kanan[0][9]:
                    if kiri[0][11] > kanan[0][11]:
                        hasil.append(kiri.pop(0))
                    else:
                        hasil.append(kanan.pop(0))
                else:
                    hasil.append(kanan.pop(0))
            else:
                hasil.append(kanan.pop(0))

        while len(kiri) > 0:
            hasil.append(kiri.pop(0))

        while len(kanan) > 0:
            hasil.append(kanan.pop(0))

        return hasil
    
def merge_sort_total_transaksi_asc(arr,data_rate):
    if len(arr) == 1:
        return arr
    else:
        kiri = merge_sort_total_transaksi_asc(arr[:len(arr)//2],data_rate)
        kanan = merge_sort_total_transaksi_asc(arr[len(arr)//2:],data_rate)
        hasil = []
        while len(kiri) > 0 and len(kanan)>0:
            nominal_kiri = kiri[0][7].split(" ")
            nominal_kanan = kanan[0][7].split(" ")
            if float(nominal_kiri[0]) / float(data_rate[nominal_kiri[1]]) < float(nominal_kanan[0]) / float(data_rate[nominal_kanan[1]]):
                hasil.append(kiri.pop(0))
            else:
                hasil.append(kanan.pop(0))
        while len(kiri) >0:
            hasil.append(kiri.pop(0))

        while len(kanan) > 0 :
            hasil.append(kanan.pop(0))

        return hasil

def convert_number_format(number):
    number = str(number)
    if "." in number:
        bilangan_bulat, desimal = str(number).split(".")
        integer = "{:,}".format(int(bilangan_bulat)).replace(",", ".")
        if len(desimal) < 2:
            Hasil = f"{integer},{desimal}0"
        else:
            Hasil = f"{integer},{desimal}"
    else:
        bilangan_bulat = "{:,}".format(int(number)).replace(",", ".")
        Hasil = f"{bilangan_bulat},00"

    return Hasil