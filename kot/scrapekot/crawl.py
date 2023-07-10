from dataclasses import dataclass

from tenacity import retry, stop_after_attempt, wait_fixed

from kot.common.crawl import BaseCrawler

TOP_URL = "https://s3.kingtime.jp/admin"


@dataclass
class CrawlerParams:
    account_id: str
    account_password: str


@dataclass
class CrawledData:
    page_source: str


class Crawler(BaseCrawler):
    def run(self, params: CrawlerParams) -> CrawledData:
        try:
            page_source = self._get_page_source(params)
        finally:
            # ウェブドライバーのプロセスを消す
            self.browser.quit()
        return CrawledData(page_source=page_source)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    def _get_page_source(self, params: CrawlerParams) -> str:
        # トップページ
        self.browser.get(TOP_URL)
        # ID/PASS 入力
        self.browser.send('//*[@id="login_id"]', params.account_id)
        self.browser.send('//*[@id="login_password"]', params.account_password)
        # ログイン
        self.browser.click('//*[@id="login_button"]')
        # ログイン成功したか確認
        url = self.browser.current_url
        if url == TOP_URL:
            raise Exception("login failed")
        # ソースを取得
        page_source = self.browser.page_source
        return page_source
