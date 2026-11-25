# uas-bigdata-kel10-kualitas-udara

Analisis kualitas udara Benowo, Surabaya (2019–2025) dengan HDFS, Spark, dan MLlib.

## Struktur

```
config/*-site.xml          konfigurasi Hadoop (core, hdfs, mapred, yarn)
data/raw/                  dataset asli (xlsx)
data/processed/            CSV seragam hasil src/prepare_data.py
hdfs_scripts/              script kelola dataset di HDFS
src/                       script Python (persiapan data, Spark/MLlib)
docker-compose.yml         cluster Hadoop: namenode, datanode1-2, resourcemanager, nodemanager1-2
```

## Menjalankan

Prasyarat: Docker Desktop menyala, Python 3 + `pip install -r requirements.txt`.
Nama container sama dengan proyek praktikum `C:\bigdata\mapreduce`, jadi matikan dulu cluster itu (`docker compose down`).

```powershell
python src/prepare_data.py                 # 1. xlsx -> data/processed/*.csv
docker compose up -d                       # 2. nyalakan cluster
docker exec -u hadoop namenode bash /hdfs_scripts/hdfs_dataset.sh upload   # 3. upload ke HDFS
```

Dari Git Bash (bukan PowerShell), jalankan `export MSYS_NO_PATHCONV=1` dulu supaya path `/hdfs_scripts/...` tidak diubah jadi path Windows.

Web UI: HDFS http://localhost:9870 · YARN http://localhost:8088 · NodeManager http://localhost:8042, :8043

Perintah kelola dataset (`docker exec -u hadoop namenode bash /hdfs_scripts/hdfs_dataset.sh <perintah>`):

| Perintah | Fungsi |
|---|---|
| `upload` | salin `data/raw` dan `data/processed` ke `/kualitas-udara/` di HDFS |
| `ls` | daftar file dataset di HDFS |
| `head [N]` | tampilkan N baris pertama CSV |
| `download <path>` | ambil dari HDFS ke `data/download/` |
| `rm <path>` | hapus file/folder di `/kualitas-udara/` |
| `report` | status cluster dan datanode |

Path dataset di HDFS: `hdfs://namenode:8020/kualitas-udara/processed/airquality_benowo_clean.csv`

Matikan: `docker compose down` (data HDFS tetap tersimpan) · hapus total: `docker compose down -v`
