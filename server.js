const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3000;
const PYTHON3 = process.env.PYTHON3_PATH || '/usr/bin/python3';

// 静的ファイルの提供
app.use(express.static('public'));

// Wi-Fiスキャンエンドポイント
app.get('/api/scan', (req, res) => {
  // Pythonスクリプトを使用してWi-Fi情報を取得（CoreWLAN APIを使用）
  const scriptPath = path.join(__dirname, 'scan_wifi.py');

  exec(`${PYTHON3} "${scriptPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error('Error executing scan_wifi.py:', error);
      console.error('stderr:', stderr);
      return res.status(500).json({
        error: 'Failed to scan WiFi networks',
        message: error.message
      });
    }

    try {
      // Pythonスクリプトの出力をパース
      const data = JSON.parse(stdout);

      console.log('Python script metadata:', data.metadata);

      // エラーチェック
      if (data.metadata && data.metadata.error) {
        return res.status(500).json({
          error: data.metadata.error,
          networks: []
        });
      }

      // レスポンス形式を既存のフロントエンドに合わせて変換
      const networks = data.networks.map(network => ({
        ssid: network.SSID || '(hidden)',
        bssid: network.BSSID || '',
        rssi: network.RSSI,
        channel: network.Channel ? network.Channel.toString() : '',
        band: network.Band,
        bandwidth: network.Bandwidth,
        security: network.Security,
        // 互換性のために古いフィールドも保持
        ht: network.Bandwidth,
        cc: ''
      }));

      res.json({
        networks,
        timestamp: data.metadata.timestamp,
        count: networks.length,
        connectedBssid: data.metadata.connected_bssid
      });
    } catch (parseError) {
      console.error('Error parsing Python script output:', parseError);
      console.error('stdout:', stdout);
      res.status(500).json({
        error: 'Failed to parse WiFi data',
        message: parseError.message
      });
    }
  });
});

app.listen(PORT, () => {
  console.log(`🛜  WiFi Analyzer running at http://localhost:${PORT}`);
  console.log('Press Ctrl+C to stop');
});
