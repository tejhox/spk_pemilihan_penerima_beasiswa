from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from .models import datamhs, kriteria, result
from .forms import FormMhs
import pymysql

def index_view(request):
    daftar = datamhs.objects.all()
    context = {
        'daftar':daftar  
    }
    return render(request, 'index.html', context)

def kriteria_view(request):
    bobot = kriteria.objects.all()
    context = {
        'bobot':bobot
    }
    return render(request, 'kriteria.html', context)


def add_view(request):
    if request.method == 'POST':
        task = FormMhs(request.POST)
        if task.is_valid():
            mydb=pymysql.connect(db = 'spk_project', user = 'root', passwd = '', host = 'localhost', port = 3306, autocommit = True)
            cur=mydb.cursor()
            sql = """INSERT INTO spk_datamhs (nim, nama, ipk, penghasilan, sertifikat , tanggungan, semester)
                      VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cur.execute(sql, (task.cleaned_data['nim'], 
                              task.cleaned_data['nama'], 
                              task.cleaned_data['ipk'], 
                              task.cleaned_data['penghasilan'], 
                              task.cleaned_data['sertifikat'],
                              task.cleaned_data['tanggungan'],
                              task.cleaned_data['semester'],))
            cur.execute("""INSERT INTO spk_kriteria (nim, nama, C1, C2, C3, C4, C5) SELECT nim, nama,
		              IF(spk_datamhs.ipk < 2.75 , 0,
                      IF(spk_datamhs.ipk > 2.75 AND spk_datamhs.ipk <= 3.00, 0.25,
                      IF(spk_datamhs.ipk > 3.0 AND spk_datamhs.ipk <= 3.25, 0.5,
                      IF(spk_datamhs.ipk > 3.25 AND spk_datamhs.ipk <= 3.5, 0.75,
                      IF(spk_datamhs.ipk > 3.5, 1, NULL))))),
                          IF(spk_datamhs.penghasilan <= 1000000 , 0.25,
                          IF(spk_datamhs.penghasilan > 1000000 AND spk_datamhs.penghasilan <= 2000000, 0.5,
                          IF(spk_datamhs.penghasilan > 2000000 AND spk_datamhs.penghasilan <= 4000000, 0.75,
                          IF(spk_datamhs.penghasilan > 4000000, 0.5, NULL)))),
                              IF(spk_datamhs.sertifikat = 1, 0,
                              IF(spk_datamhs.sertifikat = 2, 0.25,
                              IF(spk_datamhs.sertifikat = 3, 0.5,
                              IF(spk_datamhs.sertifikat = 4, 0.75,
                              IF(spk_datamhs.sertifikat >= 5, 1, NULL))))),
                                  IF(spk_datamhs.tanggungan = 1, 0,
                              	  IF(spk_datamhs.tanggungan = 2, 0.25,
                              	  IF(spk_datamhs.tanggungan = 3, 0.5,
                              	  IF(spk_datamhs.tanggungan = 4, 0.75,
                              	  IF(spk_datamhs.tanggungan >= 5, 1, NULL))))),
                                  	  IF(spk_datamhs.semester <= 2, 0,
                              	  	  IF(spk_datamhs.semester = 3, 0.25,
                              	  	  IF(spk_datamhs.semester = 4, 0.5,
                              	   	  IF(spk_datamhs.semester >= 5 AND spk_datamhs.semester <=7, 0.75,
                              	  	  IF(spk_datamhs.semester >= 7, 1, NULL)))))                                     
                      FROM spk_datamhs ON DUPLICATE KEY UPDATE 
                      nim = VALUES(nim), nama = VALUES(nama), C1 = VALUES(C1), C2 = VALUES(C2), 
                                         C3 = VALUES(C3), C4 = VALUES(C4), C5 = VALUES(C5)""")
            cur.execute("""INSERT INTO spk_normalisasi (nim, nama, W1, W2, W3, W4, W5)
                    SELECT nim, nama, 
            		       C1 / (SELECT max(C1) FROM spk_kriteria),
                          (SELECT min(C2) FROM spk_kriteria) / C2,
                           C3 / (SELECT max(C3) FROM spk_kriteria),
                           C4 / (SELECT max(C4) FROM spk_kriteria),
                           C5 / (SELECT max(C5) FROM spk_kriteria) 
                    FROM spk_kriteria ON DUPLICATE KEY UPDATE 
                    nim=VALUES(nim), nama=VALUES(nama), 
                    W1=VALUES(W1), W2=VALUES(W2), W3=VALUES(W3), W4=VALUES(W4), W5=VALUES(W5)""")
            cur.execute("""INSERT INTO spk_result (nim, nama, maxresult)
                   SELECT nim, nama,
                          (1 * W1) + (0.25 * W2) + (1 * W3) + (1 * W4) + (1 * W5)
                          FROM spk_normalisasi ON DUPLICATE KEY UPDATE 
                          nim=VALUES(nim), nama=VALUES(nama), maxresult=VALUES(maxresult)""")
            messages.success(request, 'Sukses ')
            return redirect('SPK:index')
        else:
            form = FormMhs()
            return render(request, 'form.html', {'form': form})
    else:
        form = FormMhs()
        return render(request, 'form.html', {'form': form})

def update_view(request, daftar_nim):
    task = datamhs.objects.get(pk=daftar_nim)
    if request.method == 'POST':
        form = FormMhs(request.POST, instance=task)
        if form.is_valid():
            form.save()
            mydb=pymysql.connect(db = 'spk_project', user = 'root', passwd = '', host = 'localhost', port = 3306, autocommit = True)
            cur=mydb.cursor()
            cur.execute("""INSERT INTO spk_kriteria (nim, nama, C1, C2, C3, C4, C5) SELECT nim, nama,
		              IF(spk_datamhs.ipk < 2.75 , 0,
                      IF(spk_datamhs.ipk > 2.75 AND spk_datamhs.ipk <= 3.00, 0.25,
                      IF(spk_datamhs.ipk > 3.0 AND spk_datamhs.ipk <= 3.25, 0.5,
                      IF(spk_datamhs.ipk > 3.25 AND spk_datamhs.ipk <= 3.5, 0.75,
                      IF(spk_datamhs.ipk > 3.5, 1, NULL))))),
                          IF(spk_datamhs.penghasilan < 1000000 , 0.25,
                          IF(spk_datamhs.penghasilan > 1000000 AND spk_datamhs.penghasilan <= 2000000, 0.5,
                          IF(spk_datamhs.penghasilan > 2000000 AND spk_datamhs.penghasilan <= 4000000, 0.75,
                          IF(spk_datamhs.penghasilan > 4000000, 0.5, NULL)))),
                              IF(spk_datamhs.sertifikat = 1, 0,
                              IF(spk_datamhs.sertifikat = 2, 0.25,
                              IF(spk_datamhs.sertifikat = 3, 0.5,
                              IF(spk_datamhs.sertifikat = 4, 0.75,
                              IF(spk_datamhs.sertifikat >= 5, 1, NULL))))),
                                  IF(spk_datamhs.tanggungan = 1, 0,
                              	  IF(spk_datamhs.tanggungan = 2, 0.25,
                              	  IF(spk_datamhs.tanggungan = 3, 0.5,
                              	  IF(spk_datamhs.tanggungan = 4, 0.75,
                              	  IF(spk_datamhs.tanggungan >= 5, 1, NULL))))),
                                  	  IF(spk_datamhs.semester <= 2, 0,
                              	  	  IF(spk_datamhs.semester = 3, 0.25,
                              	  	  IF(spk_datamhs.semester = 4, 0.5,
                              	   	  IF(spk_datamhs.semester >= 5 AND spk_datamhs.semester <=7, 0.75,
                              	  	  IF(spk_datamhs.semester >= 7, 1, NULL)))))                                     
                      FROM spk_datamhs ON DUPLICATE KEY UPDATE 
                      nim = VALUES(nim), nama = VALUES(nama), C1 = VALUES(C1), C2 = VALUES(C2), 
                                         C3 = VALUES(C3), C4 = VALUES(C4), C5 = VALUES(C5)""")
            cur.execute("""INSERT INTO spk_normalisasi (nim, nama, W1, W2, W3, W4, W5)
                    SELECT nim, nama, 
            		       C1 / (SELECT max(C1) FROM spk_kriteria),
                          (SELECT min(C2) FROM spk_kriteria) / C2,
                           C3 / (SELECT max(C3) FROM spk_kriteria),
                           C4 / (SELECT max(C4) FROM spk_kriteria),
                           C5 / (SELECT max(C5) FROM spk_kriteria)
                    FROM spk_kriteria ON DUPLICATE KEY UPDATE 
                    nim=VALUES(nim), nama=VALUES(nama), 
                    W1=VALUES(W1), W2=VALUES(W2), W3=VALUES(W3), W4=VALUES(W4), W5=VALUES(W5)""")
            cur.execute("""INSERT INTO spk_result (nim, nama, maxresult)
                          SELECT nim, nama,
                          (1 * W1) + (0.25 * W2) + (1 * W3) + (1 * W4) + (1 * W5)
                          FROM spk_normalisasi ON DUPLICATE KEY UPDATE 
                          nim=VALUES(nim), nama=VALUES(nama), maxresult=VALUES(maxresult)""")
            messages.success(request, 'Sukses')
            return redirect('SPK:index')
    else:
        form = FormMhs(instance=task)
    return render(request, 'form.html', {'form': form})
    
def delete_view(request, daftar_nim):
     try:   
        hapus = datamhs.objects.get(pk=daftar_nim)
        mydb=pymysql.connect(db = 'spk_project', user = 'root', passwd = '', host = 'localhost', port = 3306, autocommit = True)
        cur=mydb.cursor()
        sql = """DELETE spk_datamhs, spk_kriteria, spk_normalisasi 
                 FROM spk_datamhs INNER JOIN spk_kriteria 
                 ON spk_datamhs.nim = spk_kriteria.nim INNER JOIN spk_normalisasi 
                 ON spk_kriteria.nim = spk_normalisasi.nim INNER JOIN spk_result 
                 ON spk_normalisasi.nim = spk_result.nim
                 WHERE spk_datamhs.nim = '%s'"""
        cur.execute(sql, (hapus.nim))
        messages.success(request, 'Sukses')
        return redirect('SPK:index')
     except datamhs.DoesNotExist:
        raise Http404("Tidak ditemukan.")

def deleteAll(request):
    try:
        mydb = pymysql.connect(db = 'spk_project', user = 'root', passwd = '', host = 'localhost', port = 3306, autocommit = True)
        cur = mydb.cursor()
        cur.execute("DELETE FROM spk_datamhs")
        cur.execute("DELETE FROM spk_kriteria")
        cur.execute("DELETE FROM spk_normalisasi")
        cur.execute("DELETE FROM spk_result")
        messages.success(request, 'Sukses')
        return redirect('SPK:index')
    except datamhs.DoesNotExist:
        raise Http404("Tidak ditemukan.")

def tentukan_view(request):
    mydb = pymysql.connect(db = 'spk_project', user = 'root', passwd = '', host = 'localhost', port = 3306, autocommit = True)
    cur = mydb.cursor()    
    cur.execute("SELECT nim, nama, maxresult FROM spk_result ORDER BY maxresult DESC LIMIT 1")     
    result = cur.fetchone()
    context = {
        'nim': result[0],
        'nama': result[1],
        'maxresult': result[2],
    }
    return render(request, 'hasil.html', context)




    
    
    
    
    
    
    



    





    


    
    
    



