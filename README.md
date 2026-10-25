# Talklear Development Workspace

Talklearの日英翻訳チャットのコード、設計、タスク、検証を管理する個人用ワークスペースです。

[Notionダッシュボード](https://airy-mantis-6f3.notion.site/Talklear-Development-Workspace-404bfd032199810eac93f56f7cf89f99) / [計画](docs/project/master-plan.md) / [技術設計](docs/design/architecture.md) / [監査結果](reports/private-workspace-audit.md)

## MVPと技術構成

部屋作成・参加、原文チャット、PostgreSQLへの保存と履歴、日英の端末内翻訳、原文表示に対応します。Java 21 / Spring Boot 3.5.16 / Spring JDBC、HTML/CSS/JavaScript、PostgreSQL、Chrome Translator / LanguageDetectorを使用します。

## ローカル起動

Docker DesktopとPowerShellを用意し、`./Start-Docker.ps1`を実行します。停止は`./Stop-Docker.ps1`。非Docker版は`./Setup.ps1`、`./Start-App.ps1`を使用します。パスワードや実データはGit管理外の`.local/`へ保存します。元アプリとCompose名が同じため、既存の環境と同時に再作成テストを行わないでください。

## ドキュメント

- [要件](docs/requirements.md)、[API](docs/design/api.md)、[DB](docs/design/database.md)、[アプリ公開設定](docs/deployment.md)
- [開発日程](docs/project/timeline.md)、[チーム](docs/project/team.md)、[ID台帳](docs/project/id-ledger.json)
- [テスト計画](docs/testing/plan.md)、[アクセス設定](docs/deployment/access-settings.md)、[記録の出典](docs/admin/record-sources.md)

## 検証

`python scripts/verify_records.py`でID・日程・参照・出典・アクセス証拠・ソースハッシュを照合します。`node --test tests/translator.test.mjs tests/message-feed.test.mjs`でブラウザロジックを検証できます。Java/DBは準備済みのテスト環境で`./Test-App.ps1`、Docker結合は独立環境で`./Test-Docker.ps1`を使用します。実測の結果と未実行項目はテスト記録を参照してください。

GitHubはPublic、Notionはリンクを知っている人がログインなしで閲覧できるWeb公開設定です。Notionの検索エンジンへの掲載はオフです。開発記録は工程モデルとして整理しており、出典と実測の区分は管理用資料に集約しています。
