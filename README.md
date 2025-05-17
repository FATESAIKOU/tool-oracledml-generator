# Oracle 12c 測試環境使用說明

## 1. 啟動 Oracle DB

在 `testdb-env/` 目錄下執行以下指令：

```sh
docker-compose up -d
```

這會啟動一個 Oracle 12c 測試資料庫，並自動載入 `ddl/` 與 `dml/` 目錄下的所有 SQL 檔案。

---

## 2. 測試 Oracle DB 載入狀況

執行以下指令來確認資料表與資料是否正確建立：

```sh
chmod +x testdb-env/test-scripts/test_esample_ddl_dml.sh
./testdb-env/test-scripts/test_esample_ddl_dml.sh
```

此腳本會自動連線資料庫並查詢 `test_table`，顯示目前資料內容。

---

如需新增 DDL 或 DML，請將 SQL 檔案分別放入 `testdb-env/ddl/` 或 `testdb-env/dml/` 目錄，重啟容器即可自動載入。
