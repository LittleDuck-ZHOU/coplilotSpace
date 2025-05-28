# Github Coplilotで簡単な日報管理アプリケーションを作る

## 概要
このアプリケーションは、日報（業務日誌）をWeb上で登録・編集・一覧・ダウンロードできるFlask製のシンプルな管理ツールです。

## 主な機能
- 日報の登録（1日1件）
- 当日の日報の編集・削除
- 週単位・日付指定での日報一覧表示
- 日報データのCSVダウンロード（日本語対応）

## インストール方法
1. 必要なパッケージをインストールします。
   ```bash
   pip install flask flask_sqlalchemy
   ```
2. プロジェクトディレクトリに移動します。
   ```bash
   cd /workspaces/coplilotSpace
   ```

## 実行方法
1. アプリケーションを起動します。
   ```bash
   python app.py
   ```
2. ブラウザで `http://localhost:8080` にアクセスします。

## ファイル構成
- `app.py` : メインアプリケーション
- `templates/` : HTMLテンプレート（index, list, edit, base）
- `instance/nippou.db` : SQLiteデータベース

## 注意事項
- 日報は1日1件のみ登録可能です。
- 編集・削除は当日分のみ可能です。
- CSVはBOM付きUTF-8で出力され、日本語も文字化けしません。

## ライセンス
MIT License
