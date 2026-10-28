# 記録と参照資料

タスク・議事録・レビュー・KPTを関連するコードに対応付け、チームの担当作業・判断・改善内容を管理します。検証結果は実行日・対象・ログとともに管理します。

## 記録の出典と扱い

ここを資料区分と参照先の正本とする。日常のタスク・議事録・KPTには日付・担当を記載する。作業日、Gitコミット日時、テスト実行日はそれぞれの欄で管理する。

- Verified：現在のソースと実行ログで確認した事項。テストの実測は2026-10-25のCIとローカルログ。
- Provided：3名の役割、9/1開始、10/18のMVP基準、火水各5時間・木KPT30分、開発210人時という指定条件。
- Recorded：会議、担当作業、不具合、レビュー、KPT、タスクの記録。
- Assumed：開始時刻、作業枠の配分等の計画値。
- Unverified：対象日時点のコードや過去の実行結果について、追加確認が必要な事項。

Evidence Typeは資料の区分、Statusは作業の状態を管理する。日付の表示名は工程日とし、日付値・プロパティIDは維持する。テストの成功・失敗・未実行は、各テストの実行結果で管理する。

## コード・資料の集約と参照

コード集約時の参照元はzahin-dev/translate-chatのmain、48ファイル。取得時の識別子はa01d9ce7e260544cc56d9645600d3b8471968be0。ファイル構成とハッシュはsource-manifest.jsonで管理する。元リポジトリの履歴・PR・Issuesは現在の資料に取り込んでいない。44のアプリ・テスト・実行設定は取得版のバイト列を保持する。

このリポジトリへのコード・資料の集約日は2026-10-25。企画・環境・メモリ内試作・DB・翻訳・画面・テスト・実行設定に分類し、取得版から登録した段階別Git履歴と対応付けた。Gitの日時は集約時の登録日時、開発記録の日付は各作業の対象日として管理する。DB安全策と完成UIの一括統合の範囲は対応コミットに記載する。

初期13コミットの作者・コミッターはzahin-dev / 293001590+zahin-dev@users.noreply.github.comに統一する。日時と各時点のファイル内容を保持する。作者情報とコミットメッセージの修正に伴うIDの変更は、それぞれの対応表で管理する。member1、member2、zahin-devの担当作業は開発セッションに記載し、Git作者・承認者はコミットやレビューのメタデータで管理する。AI支援の提案は検討資料として管理する。

## 日付と参照の読み方

開発記録の対象期間は2026-09-01〜2026-10-18、コード・資料の集約日は2026-10-25。IDのYYYYMMDDは作業の対象日を表す。Gitコミット日時とテスト実行日はそれぞれの記録で管理する。開発14回・KPT7回とし、10/18はMVP基準日。関連IDの索引は資料整理時の追記を含む。

## 現在のアクセスと過去の公開記録

この管理環境はチーム開発のコード・設計・タスク・検証を管理するワークスペースです。GitHubはpublicで管理します。2026-10-25の非公開化監査時点では、GitHubはprivate、親ページのSitesは未公開、General accessはOnly people invitedでした。公開時のJSON・画像・実行報告は日付付きアーカイブとして内容を保全し、現在の設定とは区別する。既存の公開Forkは取得時点0件だが、第三者の複製や検索キャッシュの回収は保証できない。

## 管理資料

[アクセス設定](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/deployment/access-settings.md)

[対応コミット](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/verification/stage-map.md)

[出典区分台帳](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/admin/evidence-index.json)

[2026-10-25の非公開化監査記録](https://github.com/zahin-dev/talklear-development-simulation/blob/main/reports/private-workspace-audit.md)

[コミットID対応表](https://github.com/zahin-dev/Talklear/blob/main/docs/admin/commit-author-map.json)

[今回のコミット参照対応表](https://github.com/zahin-dev/Talklear/blob/main/docs/admin/commit-reference-map.json)
