# nicolive-ffmpeg-py

**このプロジェクトは更新されません**: ライブ配信の自動通知機能などを備えたCLIツール [shinosaki/namagent](https://github.com/shinosaki/namagent) をご利用ください。

This Python script is a wrapper for processing NicoNicoLive streams using ffmpeg.

## Download

[Releases Page](https://github.com/shinosaki/nicolive-ffmpeg-py/releases)

## Usage

You need to specify an **output path** that includes the **program ID** (e.g., lv123456).

```
cli.exe rec/lv123456.mp4
```

## Usage as a Recording Engine for "guest-nico/nicoNewStreamRecorderKakkoKari"

- [guest-nico/nicoNewStreamRecorderKakkoKari](https://github.com/guest-nico/nicoNewStreamRecorderKakkoKari)
- [ニコ生新配信録画ツール（仮）](https://guest-nico.github.io/pages/rec_readme.html)

- **Version Requirements**:
  - Ensure you are using version **[0.89.14](https://github.com/guest-nico/nicoNewStreamRecorderKakkoKari/releases/download/releases/ver0.89.14.0.1.3.11.4.zip)**
  - Starting from version **0.89.15**, the program will terminate without attempting to record streams from `dlive`.

1. Execute `ニコ生新配信録画ツール（仮）.exe`
2. Open `ツール` -> `オプション`
3. Open `録画方法` tab:
4. Select `外部のHLS録画エンジンを使う` option
5. Input `コマンド` field
   - Enter the following:
     - `<path to cli.exe> {o}`
   - or Using specify extension:
     - `<path to cli.exe> {o}.mp4`

## Feature

- (2025/02/13): Currently supports processing from the new streaming server (`dlive`).

## Author
shinosaki

## LICENSE
[MIT](./LICENSE)
