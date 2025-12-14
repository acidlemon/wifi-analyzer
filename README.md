# WiFi Analyzer

Mac の airportコマンドを利用せず、macOS 14.4以降も利用可能な Wi-Fi ネットワーク分析ツール

## 機能

- 📡 周辺の Wi-Fi ネットワークをスキャン
- 📊 信号強度の視覚化（グラフ表示）
- 🔍 BSSID、チャンネル、セキュリティ情報の表示
- 📈 チャンネル使用状況の分析

## セットアップ

1. **依存関係のインストール**

python3からObjectiveC呼ぶライブラリを標準Python3に追加

```bash
/usr/bin/python3 -m pip install pyobjc-framework-CoreWLAN pyobjc-framework-CoreLocation
```

npm installする

```bash
npm install
```

2. **サーバーの起動**

```bash
npm start
```

3. **ブラウザで開く**

http://localhost:3000 にアクセス

## 使い方

1. ブラウザで「🔍 スキャン開始」ボタンをクリック
2. 周辺のWi-Fiネットワークが一覧表示されます
3. グラフで信号強度とチャンネル使用状況を確認できます

## 画面の見方

### 統計情報
- **検出ネットワーク**: スキャンで見つかったネットワークの総数
- **強い信号**: -60dBm 以上の良好な信号のネットワーク数
- **使用チャンネル数**: 使用されているチャンネルの種類

### 信号強度の目安
- 🟢 **Excellent** (-50dBm以上): 非常に良好
- 🔵 **Good** (-60dBm以上): 良好
- 🟠 **Fair** (-70dBm以上): まあまあ
- 🔴 **Poor** (-70dBm未満): 弱い

### テーブルカラム
- **SSID**: ネットワーク名
- **BSSID**: アクセスポイントのMACアドレス
- **信号強度**: 視覚的な強度バー
- **RSSI**: 信号強度の数値（dBm）
- **チャンネル**: 使用チャンネル
- **セキュリティ**: 暗号化方式

## カスタマイズ

### 自動更新を有効にする

`public/index.html` の最後のコメントアウトを解除：

```javascript
// 自動スキャン（オプション）
setInterval(scanNetworks, 10000); // 10秒ごと
```

### ポート番号を変更

`server.js` の `PORT` 変数を変更：

```javascript
const PORT = 3000; // お好みのポート番号に変更
```

## 技術スタック

- **Backend**: Node.js + Express
- **Frontend**: HTML5 + Vanilla JavaScript
- **Charts**: Chart.js

## ライセンス

MIT
