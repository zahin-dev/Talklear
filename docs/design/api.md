# 現行API（現在の実装で確認）

共通prefix `/api`。参加資格は`X-Participant-Token`で指定。

|方法|経路|主な入力・応答|
|---|---|---|
|POST|/rooms|displayName,language → Membership、201|
|POST|/rooms/{code}/join|同上、201|
|GET|/rooms/{code}/state?after=0|self,participants,messages,hasMoreHistory|
|GET|/rooms/{code}/messages?before=ID|messages,hasMoreHistory|
|POST|/rooms/{code}/messages|clientId UUID,text,sourceLanguage → Message、200|
|POST|/rooms/{code}/leave|204|

Joinはja/en、送信sourceLanguageはja/en/und。表示名はstrip後30コードポイント、本文2000コードポイント。トークン不足・不一致・退出済は401 SESSION_EXPIRED。部屋コード不正は404 ROOM_NOT_FOUND。同送信IDの本文・言語変更は409 SEND_CONFLICT。頻度超過429 RATE_LIMIT。

初回stateは最近100件を昇順へ反転。beforeは境界未満を最大100件。afterは境界超過をID昇順で最大100件。stateアクセスでlast_seenを更新し、45秒以内の参加者を表示する。退室後の再入室は新トークン。仕様根拠：ChatController.java / ChatService.java。