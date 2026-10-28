# 記録と参照資料

本プロジェクトの開発過程・会議・役割別の作業・レビュー・KPT・タスクは、完成版のソースと関連資料を参照して工程ごとに整理しています。検証結果は実行日・対象・ログとともに管理します。

## 記録の出典と扱い

ここを資料区分と参照先の正本とする。日常のタスク・議事録・KPTには日付・担当を記載する。作業日、Gitコミット日時、テスト実行日はそれぞれの欄で管理する。

- Verified：現在のソースと実行ログで確認した事項。テストの実測は2026-10-25のCIとローカルログ。
- Provided：3名の役割、9/1開始、10/18のMVP基準、火水各5時間・木KPT30分、開発210人時という指定条件。
- Recorded：会議、担当作業、不具合、レビュー、KPT、タスクの記録。
- Assumed：開始時刻、作業枠の配分等の計画値。
- Unverified：実際の10/18のファイル内容と元資料にある過去の検証・公開成功の主張。

Evidence Typeは資料の区分、Statusは作業の状態を管理する。日付の表示名は工程日とし、日付値・プロパティIDは維持する。テストの成功・失敗・未実行は、各テストの実行結果で管理する。

## 取得・作成方法

元ソースはzahin-dev/translate-chat既定mainのZIP48ファイルのみ。SHA a01d9ce7e260544cc56d9645600d3b8471968be0。元の履歴・PR・Issues・blameを開発経緯の根拠にしていない。44のアプリ・テスト・実行設定は取得版のバイト列を保持する。

取得版のコードをもとに、企画・環境・メモリ内試作・DB・翻訳・画面・テスト・実行設定の段階別Git履歴を整理した。DB安全策と完成UIの細かな途中差分は一括統合として記載する。各段階の変更範囲は対応コミットを参照する。

元の13コミットは保持する。作者Talklear Simulation Builder / simulation@talklear.invalid、当時の説明、SHA、実行日時はそのまま残る。member1、member2、zahin-devの担当作業は開発セッションに記載し、Git作者・承認者はコミットやレビューのメタデータで管理する。AI支援の提案は検討資料として管理する。

## 日付と参照の読み方

IDのYYYYMMDDは工程日。実際のファイル生成・Gitコミット・検証日は別に管理する。14回の開発と7回のKPTを維持し、10/18に追加の開発枠を作らない。横断IDの索引は整理時の追記を含む。

## 現在のアクセスと過去の公開記録

この管理環境はチーム開発のコード・設計・タスク・検証を管理する非公開のワークスペースです。GitHubはprivate、親ページのSitesは未公開、General accessはOnly people invited。公開時のJSON・画像・実行報告は日付付きアーカイブとして内容を保全し、現在の設定とは区別する。既存の公開Forkは取得時点0件だが、第三者の複製や検索キャッシュの回収は保証できない。

## 管理資料

[アクセス設定](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/deployment/access-settings.md)

[対応コミット](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/verification/stage-map.md)

[出典区分台帳](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/admin/evidence-index.json)

[現行の監査結果](https://github.com/zahin-dev/talklear-development-simulation/blob/main/reports/private-workspace-audit.md)
