# 残作業と制約

GitHub Publicと[Notion公開](https://airy-mantis-6f3.notion.site/Talklear-Development-Simulation-404bfd032199810eac93f56f7cf89f99)は実施済み。Notionの検索エンジンインデックスはOff。公開手続きの手動残作業はない。

実Chromeのモデル取得・双方向翻訳・原文・失敗再試行、日英UI、狭い画面、幅操作は未実行。Testsの手動2件に従って確認し、実行日と結果を正本へ記録する。

JUnit17・Node6・Docker1とビルドは[今回のCI](https://github.com/zahin-dev/talklear-development-simulation/actions/runs/40172458340)で成功。ローカルJava/Mavenは未導入、Dockerエンジンは停止のまま。元と同じComposeプロジェクト名を保持するため、既存アプリ環境で再作成テストを実行しない。

復元は学習用の粗い段階。DB版の安全策と完成UIの細かな中間差分、模擬バグごとの旧実装は独立再現していない。これは元の実装履歴・担当・承認の証拠ではない。元履歴・PR・Issue・blameによる補完なし。

MVP後の保存期限・招待失効・訳文品質・無料枠運用は保留。最終KPTのTryを実施済みとしない。

Notion Freeの行クエリ枠に到達したため、Testsの最終再読込みはサポートされたビュー取得で完了した。公開・作成・Relationの残作業はない。
