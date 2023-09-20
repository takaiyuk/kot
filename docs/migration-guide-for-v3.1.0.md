# v3.1.0 以降への移行ガイド

v3.0.0 以前のバージョンを利用していたユーザーが v3.1.0 以降のバージョンを使う場合の注意点について説明する

## config.yaml の修正

v3.0.0 以前は以下のような config.yaml だった

```yaml
    account:
        id: id
        password: passaword
    scrapekot:
        slack:
            webhook_url: url
            channel: channel
            icon_emoji: icon
            username: username
    myrecorder:
        slack:
            webhook_url: url
            channel: channel
            icon_emoji: icon
            username: username
```

v3.1.0 以降は以下のような config.yaml の形式を想定する

- scrapekot.slack と myrecorder.slack が持つフィールドの名前が channel -> channels に変更
- scrapekot.slack と myrecorder.slack が持つフィールドのデータ型が str -> list[str] に変更

```yaml
    account:
        id: id
        password: passaword
    scrapekot:
        slack:
            webhook_url: url
            channels:
              - channel_a
            icon_emoji: icon
            username: username
    myrecorder:
        slack:
            webhook_url: url
            channels:
              - channel_a
              - channel_b
            icon_emoji: icon
            username: username
```
