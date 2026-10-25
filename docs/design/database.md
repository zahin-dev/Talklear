# DBと整合性（Verified）

|テーブル|識別・制約|
|---|---|
|chat_rooms|UUID主キー、invite_code12文字一意、created_at|
|chat_participants|UUID、room_id外部キー、表示名、ja/en、token_hash一意、last_seen、left_at|
|chat_messages|BIGINT identity、room/participant外部キー、client_id UUID、原文、ja/en/und、created_at|

`UNIQUE(room_id,participant_id,client_id)`で再送を識別する。token_hashはSHA-256。メッセージ索引(room_id,id)、参加中索引(room_id,last_seen)。訳文テーブル・ユーザーアカウント表・自動削除ジョブは存在しない。

sendはトランザクション内で部屋行を`FOR NO KEY UPDATE`し、採番前に同室送信を直列化する。IDは全室共通だが取得は必ず部屋で絞る。表示側はpoll応答のみcursorを進める。SQLの保存順序対策と画面のカーソル対策の両方が必要。
