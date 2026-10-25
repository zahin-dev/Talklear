# テスト計画と実行証拠

テスト期待値と実行結果の正本はNotion Tests。シミュレーション日と実際の実行日は別。元READMEのJUnit17・JS6・Docker1成功という記述は、過去の結果としてはUnverified。ソース上の@Test17個・Nodeテスト7個の存在と区別する。

今回ローカル実行：Node翻訳3件＋MessageFeed3件成功、全JS構文チェック成功。ログはverification。実Chromeのダウンロード・訳文品質・UI操作は未実行。Java/MavenはPATH上なし、Dockerエンジン停止のためJUnitとDocker統合はローカル未実行。GitHub Actionsの今回の結果を確認できれば別途記録する。

実行方法：`node --test tests/translator.test.mjs tests/message-feed.test.mjs`、準備済の独立DBで`mvn -B verify`。Dockerは元と同じCompose名を持つため、既存環境を使わず専用マシンまたはCIで確認する。
