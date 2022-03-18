from dataclasses import dataclass

from kot.common.crawl import BaseCrawler
from kot.common.logger import logger
from kot.myrecorder import MyRecorderOptions

TOP_URL = "https://s3.kingtime.jp/independent/recorder/personal/"


@dataclass
class CrawlerParams:
    account_id: str
    account_password: str
    command: str
    message: str
    yes: bool
    is_debug: bool


class Crawler(BaseCrawler):
    def run(self, params: CrawlerParams) -> None:
        return self._punch(params)

    def _punch(self, params: CrawlerParams) -> None:
        try:
            # トップページ
            self.browser.get(TOP_URL)
            # ID/PASS 入力
            self.browser.send('//*[@id="id"]', params.account_id)
            self.browser.send('//*[@id="password"]', params.account_password)
            # ログイン
            self.browser.click('//*[@id="modal_window"]/div/div/div[3]/div/div')
            """
            # TODO: ログイン成功したか確認
            # 成功時もURLの遷移なし・失敗時もモーダルが出るだけなのでseleniumでのログインの成否判断が難しい
            """
            myrecoder_option = getattr(MyRecorderOptions, params.command)
            # 確認する
            if params.yes:
                val = "y"
                self.browser.sleep()
            else:
                val = input(f"{myrecoder_option.name}ボタンを押していいですか？[y/n]: ")
            # 実行する
            if val != "y":
                logger.info(f"{myrecoder_option.name}ボタンはスキップしました")
            else:
                assert params.command in MyRecorderOptions.__annotations__.keys()
                xpath = myrecoder_option.xpath
                if not params.is_debug:
                    raise ValueError  # FIXME: 開発中に誤ってボタンを押してしまわないように例外を発生させている
                    self.browser.click(xpath)
                    logger.info(f"{myrecoder_option.name}ボタンが押されました（多分）")
                else:
                    logger.info(f"{myrecoder_option.name}ボタンは押されない")
        finally:
            # プロセス消す
            self.browser.quit()
