# Notionバックアップと同期

[ダッシュボード](https://app.notion.com/p/404bfd032199810eac93f56f7cf89f99)を管理正本とする。`notion-map.json`のページIDとRecord IDを照合し、既存ページを更新する。重複作成・正本の無条件上書きを行わない。

CSVは9DB分のUTF-8 BOM。Content列は本文のバックアップであり、CSVインポートだけでページ本文やRelationが完成するとはみなさない。復旧順は親→Tasks→Sessions→他DB→Relation→ビュー。Record ID/本文/Status/Owner/工程日とRelationを照合する。

型：Title=title、Record ID/Phase/Related IDs=rich text、工程日=date、Owner/Status/Priority/Evidence Type=select、GitHub Reference=URL。匿名役割名は実在アカウントへ紐付けない。Evidence Typeは管理用メタデータとして通常ビューから隠す。

Tasks.DependenciesはTasks、Tasks.SessionsはDevelopment Sessions、他DB.TasksはTasksへのRelationを維持する。KPTのTryは改善タスクへつなぐ。原本の状態や値を一括置換しない。

公開手順は日常運用に含めない。アクセスは招待者のみとし、[アクセス設定](../docs/deployment/access-settings.md)と[記録の出典](../docs/admin/record-sources.md)を参照する。
