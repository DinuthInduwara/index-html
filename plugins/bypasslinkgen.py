import requests, re

class Bypass:
    def __init__(self):
        self.session = requests.Session()    
    def bypass_redirect(self, url):
        """
        regex: https?://bit\.ly/[^>]+
        regex: https?://(?:link\.zonawibu\.cc/redirect\.php\?go|player\.zafkiel\.net/blogger\.php\?yuzu)\=[^>]+
        """
        head = self.session.head(url)
        return head.headers.get("Location", url)
    
    
    def bypass_fembed(self, url):
        """
        regex: https?://(?:www\.naniplay|naniplay)(?:\.nanime\.(?:in|biz)|\.com)/file/[^>]+
        regex: https?://layarkacaxxi\.icu/[fv]/[^>]+
        regex: https?://fem(?:bed|ax20)\.com/[vf]/[^>]+
        """

        url = url.replace("/v/", "/f/")
        raw = self.session.get(url)
        api = re.search(r"(/api/source/[^\"']+)", raw.text)
        if api is not None:
            result = {}
            raw = self.session.post(
                "https://layarkacaxxi.icu" + api.group(1)).json()
            for d in raw["data"]:
                f = d["file"]
                direct = self.bypass_redirect(f)
                result[f"{d['label']}/{d['type']}"] = direct
            return result

    def bypass_streamtape(self, url):
        """
        regex: https?://streamtape\.com/v/[^/]+/[^>]+
        """

        raw = self.session.get(url)

        if (videolink := re.findall(r"document.*((?=id\=)[^\"']+)", raw.text)):
            nexturl = "https://streamtape.com/get_video?" + videolink[-1]
         
            if (redirect := self.bypass_redirect(nexturl)):
                return redirect

