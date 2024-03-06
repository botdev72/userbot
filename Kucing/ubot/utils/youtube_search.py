from json import dumps, loads
from urllib.parse import quote_plus

from requests import get


class YouTubeSearch:
    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self._search()

    def _search(self):
        encoded_search = quote_plus(self.search_terms)
        url = f"https://www.youtube.com/results?search_query={encoded_search}"
        response = get(url).text
        while "ytInitialData" not in response:
            response = get(url).text
        results = self._parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    @staticmethod
    def _parse_html(response):
        results = []
        start = response.index("ytInitialData") + len("ytInitialData") + 3
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = loads(json_str)

        for contents in data["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"]:
            for video in contents["itemSectionRenderer"]["contents"]:
                res = {}
                if "videoRenderer" in video.keys():
                    video_data = video.get("videoRenderer", {})
                    res["id"] = video_data.get("videoId", None)
                    res["title"] = (
                        video_data.get("title", {})
                        .get("runs", [[{}]])[0]
                        .get("text", None)
                    )
                    res["duration"] = video_data.get("lengthText", {}).get(
                        "simpleText", 0
                    )
                    res["views"] = video_data.get("viewCountText", {}).get(
                        "simpleText", 0
                    )
                    res["link"] = "https://www.youtube.com" + (
                        video_data.get("navigationEndpoint", {})
                        .get("commandMetadata", {})
                        .get("webCommandMetadata", {})
                        .get("url", None)
                    )
                    if (
                        res["duration"] != 0
                        and res["views"] != 0
                        and sum(
                            int(x) * 60**i
                            for i, x in enumerate(
                                reversed(str(res["duration"]).split(":"))
                            )
                        )
                        < 7200
                    ):
                        results.append(res)

            if results:
                return results
        return results

    def to_dict(self, clear_cache=True):
        result = self.videos
        if clear_cache:
            self.videos = ""
        return result

    def to_json(self, clear_cache=True):
        result = dumps({"videos": self.videos})
        if clear_cache:
            self.videos = ""
        return result
