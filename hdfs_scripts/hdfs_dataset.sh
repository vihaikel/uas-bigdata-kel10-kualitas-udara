#!/usr/bin/env bash
# Kelola dataset kualitas udara di HDFS. Dijalankan DI DALAM container namenode sebagai user hadoop
# (superuser HDFS; sebagai root, mkdir di / ditolak):
#   docker exec -u hadoop namenode bash /hdfs_scripts/hdfs_dataset.sh <perintah> [arg]
set -eu
export PATH=/opt/hadoop/bin:$PATH

HDFS_DIR=/kualitas-udara   # root dataset di HDFS
LOCAL_DIR=/data            # = folder ./data di host (lihat docker-compose.yml)

case "${1:-help}" in
  upload)    # salin data/raw & data/processed lokal ke HDFS (timpa jika sudah ada)
    hdfs dfsadmin -safemode wait
    hdfs dfs -mkdir -p "$HDFS_DIR/raw" "$HDFS_DIR/processed" "$HDFS_DIR/models"
    hdfs dfs -put -f "$LOCAL_DIR"/raw/* "$HDFS_DIR/raw/"
    hdfs dfs -put -f "$LOCAL_DIR"/processed/* "$HDFS_DIR/processed/"
    hdfs dfs -ls -R "$HDFS_DIR"
    ;;
  ls)        # daftar isi dataset beserta ukuran
    hdfs dfs -ls -R -h "$HDFS_DIR"
    ;;
  head)      # N baris pertama CSV hasil olahan (default 5)
    hdfs dfs -cat "$HDFS_DIR"/processed/*.csv 2>/dev/null | head -n "${2:-5}"
    ;;
  download)  # ambil file/folder dari HDFS ke ./data/download di host, mis: download models
    mkdir -p "$LOCAL_DIR/download"
    hdfs dfs -get -f "$HDFS_DIR/${2:?path relatif di $HDFS_DIR wajib diisi}" "$LOCAL_DIR/download/"
    ;;
  rm)        # hapus file/folder di dalam $HDFS_DIR, mis: rm processed/lama.csv
    hdfs dfs -rm -r "$HDFS_DIR/${2:?path relatif di $HDFS_DIR wajib diisi}"
    ;;
  report)    # status cluster: kapasitas, datanode aktif
    hdfs dfsadmin -report
    ;;
  *)
    echo "Perintah: upload | ls | head [N] | download <path> | rm <path> | report"
    ;;
esac
