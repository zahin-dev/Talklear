# Talklear Development Workspace

## Talklear

日英の端末内翻訳を使うルームチャット。原文の送受信・保存、履歴・再入室、翻訳失敗時の原文表示に対応するMVPを管理します。

## 開発日程とチーム

開発期間：2026-09-01〜2026-10-18。開発14回、KPT7回。火水は各5時間、木は振り返り30分。10/18はMVP基準日です。コード・資料は2026-10-25にこのリポジトリへ集約しています。作業日とGitへの登録日時は各記録で管理します。

member1：リーダー・バックエンド、member2：フロントエンド、zahin-dev：基盤・QA。企画・設計・重要な判断は全員で検討します。

## 進捗と品質

タスクは31件が完了、1件が次期保留。MVP後の保存期限・招待失効・品質評価はバックログで管理します。

実測：2026-10-25の[CI](https://github.com/zahin-dev/talklear-development-simulation/actions/runs/40172458340)でJUnit17件・Node6件・Docker結合1件とビルド成功。実Chromeの手動確認2件は未実行です。

## 管理データベース

<database url="https://app.notion.com/p/77b550fa7d514c679beadb767ab4f61b" data-source-url="collection://a307eab5-4b2c-4590-a447-7fa67f3cd75c" inline="false">
Tasks
</database>

<database url="https://app.notion.com/p/eb7e6a108aa54d01add0d5f855165c4e" data-source-url="collection://8bc37445-771c-4561-98bc-52021de597f6" inline="false">
Development Sessions
</database>

<database url="https://app.notion.com/p/3a10a4aaff5b4919956db22c63d901b7" data-source-url="collection://64c1649f-f8d7-4012-869b-954fd290083f" inline="false">
Meetings
</database>

<database url="https://app.notion.com/p/0e305b0ce1344ba68309e424cc5d22c9" data-source-url="collection://83b73d3f-602a-4315-ba7e-13b09846f298" inline="false">
ADR
</database>

<database url="https://app.notion.com/p/2192efc364ef4d179d4fbc83cc577027" data-source-url="collection://1541f45b-b389-45ac-8e85-752c4ac4eaae" inline="false">
Bugs
</database>

<database url="https://app.notion.com/p/b72e32df6a1b42f8a9480da424116512" data-source-url="collection://b105aa31-2496-405e-8d56-f57a14a754a3" inline="false">
Code Reviews
</database>

<database url="https://app.notion.com/p/1387d51aff5542559d38ed9bdb9189ad" data-source-url="collection://3456e722-0e51-4fcd-8304-a40bc60417e3" inline="false">
Tests
</database>

<database url="https://app.notion.com/p/e8f9fb575690435a959f65fe7a689c6f" data-source-url="collection://09eb3b13-9603-4394-a2c8-b0c2f2cac114" inline="false">
KPT
</database>

<database url="https://app.notion.com/p/88de900f39954701af8f644edcd31a70" data-source-url="collection://cc3d9e8c-f4f4-42ea-a39e-e934329ff639" inline="false">
Milestones
</database>

## 技術資料

[GitHubリポジトリ](https://github.com/zahin-dev/talklear-development-simulation) / [アーキテクチャ](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/design/architecture.md) / [API](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/design/api.md) / [DB](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/design/database.md) / [テスト計画](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/testing/plan.md) / [全ID台帳](https://github.com/zahin-dev/talklear-development-simulation/blob/main/docs/project/id-ledger.json)

## 管理情報

Notionを管理正本、GitHubをコード・技術資料・バックアップの保存先とします。アクセスは招待者のみです。

<page url="https://app.notion.com/p/404bfd03219981ec88d6e7d85569e002">
マスタープラン・進捗・工数
</page>

<page url="https://app.notion.com/p/404bfd032199817b9d49f45740214eb0">
チームとプロジェクト概要
</page>

<page url="https://app.notion.com/p/404bfd03219981c7a9c3c776d5f6fc39">
管理用：記録の出典と作成方法
</page>
