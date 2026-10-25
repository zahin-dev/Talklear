# テスト計画と実行証拠

テスト期待値と実行結果の正本はNotion Tests。シミュレーション日と実際の実行日は別。元READMEのJUnit17・JS6・Docker1成功という記述は、過去の結果としてはUnverified。ソース上の@Test17個・Nodeテスト7個の存在と区別する。

今回ローカル実行：Node翻訳3件＋MessageFeed3件成功、全JS構文チェック成功。ログはverification。実Chromeのダウンロード・訳文品質・UI操作は未実行。Java/MavenはPATH上なし、Dockerエンジン停止のためJUnitとDocker統合はローカル未実行。GitHub Actionsの今回の結果を確認できれば別途記録する。

実行方法：`node --test tests/translator.test.mjs tests/message-feed.test.mjs`、準備済の独立DBで`mvn -B verify`。Dockerは元と同じCompose名を持つため、既存環境を使わず専用マシンまたはCIで確認する。


## 2026-10-25のCI実測追記（Verified）

[Run 40171548771](https://github.com/zahin-dev/talklear-development-simulation/actions/runs/40171548771) / head 201f1e83d0ca5065566dc1a8e2e19811583ef2b7。JUnit17件、Node6件、Docker結合1件、JS構文、コンテナビルドが成功。JUnit内訳はHTTP/DB10、SecurityHeaders4、RequestLimits1、CloudConfiguration2。元の過去結果を転記したものではない。実Chrome・新規クラウドアプリの操作は未実施。


最終コード7a577e7528d10f269891f9666c23f0541e47e6aeでも[CI 40172458340](https://github.com/zahin-dev/talklear-development-simulation/actions/runs/40172458340)が成功。取得ZIPのPowerShell改行を復元後の結果である。件数はJUnit17・Node6・Docker1、構文とビルドも成功。
