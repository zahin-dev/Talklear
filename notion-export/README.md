# Notionバックアップ・インポート・再実行

管理正本：https://app.notion.com/p/404bfd032199810eac93f56f7cf89f99。notion-map.jsonに既存ページ・DB・各レコードの実IDを保存済み。新規作成前にはそのDBをfetchし、Record IDで全件を照合し、既存IDがあれば更新対象として扱う。タイトル検索だけで重複判定しない。曖昧なタイムアウト後は再読込みしてから不足分だけ作る。現在のNotion正本を古いJSONで無条件に上書きしない。

CSVはUTF-8 BOM、9DB分。復旧順序：親ページ・説明ページ → Tasks → Development Sessions → 他DB → Relation → ビュー。CSVのContent列は長文のバックアップであり、ページ本文へ自動展開されると仮定しない。docs配下のMarkdownを本文として使う。CSVだけではRelationは完成しない。

型：Title=title、Record ID/Phase/Related IDs/Summary=rich text、Simulation Date=date、Owner/Priority/Status/Evidence Type=select、GitHub Reference=URL、Last Updated=自動更新。匿名役割はPeople型で実在アカウントに紐付けない。

Tasks.DependenciesはTasksへのRelation、Tasks.SessionsはDevelopment SessionsへのRelation、他8DBのTasksはTasksへのRelation。KPTは改善タスクにRelationを張る。残りの横断参照は共通IDとページ本文リンクで扱い、不要なRelationを増やさない。

日付昇順、工程別、担当別のビューを使う。Freeで高度なSQL・有料認証バッジを前提にせず、通常のDBとビューで管理する。公開は親の共有→公開→公開URLを取得し、ログアウト状態で親・DB・レコードを確認。検索エンジンのインデックスを有効にしない。公開操作と公開済みの検証は別に記録する。

チェック：99件・9DB、ID重複なし、14セッション・7KPT、相互リンク、Relation、無関係ページなし、個人情報・秘密なし。
