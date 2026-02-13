---
name: setup
description: "WiFi Analyzerプロジェクトのセットアップ手順。macOS環境でのPython依存関係（CoreWLAN/CoreLocation）とNode.js依存関係のインストール、動作確認までをガイドする。ユーザーが「セットアップ」「環境構築」「インストール」「setup」と言ったときに使用。"
---

# WiFi Analyzer セットアップ

macOS の CoreWLAN API を利用した WiFi ネットワーク分析ツールのセットアップ手順。

## 前提条件

- macOS 14.4 以降
- Node.js (v18+)
- macOS 標準の `/usr/bin/python3` が存在すること

## セットアップ手順

### 1. Python 依存パッケージのインストール

**必ず `/usr/bin/python3` を使うこと。** CoreWLAN フレームワークは macOS 標準の Python からしかアクセスできない。asdf / Homebrew / pyenv 等で入れた Python では `import CoreWLAN` が失敗する。

```bash
/usr/bin/python3 -m pip install pyobjc-framework-CoreWLAN pyobjc-framework-CoreLocation
```

インストール後に確認:

```bash
/usr/bin/python3 -c "import CoreWLAN; import CoreLocation; print('OK')"
```

`OK` が出れば成功。

### 2. Node.js 依存パッケージのインストール

```bash
npm install
```

### 3. 動作確認

```bash
npm start
```

ブラウザで http://localhost:3000 を開き、「スキャン開始」ボタンを押す。WiFi ネットワーク一覧が表示されれば成功。

## トラブルシューティング

### `ModuleNotFoundError: No module named 'CoreWLAN'`

`server.js` は `/usr/bin/python3` で `scan_wifi.py` を呼び出す。このエラーが出る場合:

1. `/usr/bin/python3` にパッケージがインストールされているか確認:
   ```bash
   /usr/bin/python3 -c "import CoreWLAN; print('OK')"
   ```
2. 失敗するなら手順1を再実行

### `Location authorization failed`

CoreWLAN の WiFi スキャンには位置情報の権限が必要。ターミナルアプリ（Terminal.app / iTerm2 等）に「位置情報サービス」の権限を付与する:

macOS の「システム設定 > プライバシーとセキュリティ > 位置情報サービス」で、使用しているターミナルアプリを許可する。

### ポート 3000 が使用中

`server.js` の `PORT` 変数を変更する。
