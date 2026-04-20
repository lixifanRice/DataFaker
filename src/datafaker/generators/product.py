from __future__ import annotations

import random
import string
from datetime import datetime

from datafaker.generators.base import BaseGenerator


class ProductGenerator(BaseGenerator):
    @staticmethod
    def _rand_token(length: int = 6) -> str:
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def build_payload(self, index: int) -> dict:
        now = datetime.now()
        date_mmdd = now.strftime("%m%d")
        name_suffix = self._rand_token(6)
        app_name = f"LittleFarmStory_{name_suffix}"
        top_name = f"{date_mmdd}_auto_{app_name}"

        return {
            "name": top_name,
            "app_url": "",
            "icon_url": "https://image.deepclick.com/uploads/660_20260320100532_647.jpg",
            "first_type": 1,
            "app_type": 9,
            "partner": 1,
            "is_verify": False,
            "rules": 0,
            "redirect_type": 0,
            "account_name": "",
            "redirect_url": "",
            "avatar": "",
            "description": "",
            "web_url": "",
            "attribution_url": "",
            "integration_type": 1,
            "page_id": "",
            "whatsapp_number_group": [{"code": 1, "number": ""}],
            "line_number_group": [{"number": ""}],
            "messenger_page_id_group": [{"page_id": ""}],
            "extra_assets": {
                "app_name": "",
                "company_name": "SayGames",
                "app_download": 500,
                "app_comments": 300,
                "app_desc": (
                    "A FUN-GI TO BE AROUND\n"
                    "Calling all entrepreneurial farmers: come dive into a fantastic arcade-style "
                    "simulator game where you can build and customize your own farm! Unlock an exciting "
                    "array of plants, tools, and lands that you can cultivate to your heart's content as "
                    "you progress through the story, all while improving your business skills. Download "
                    "Little Farm Story today and let your fantasies and garden blossom!"
                ),
                "pic_list": [
                    "https://image.deepclick.com/uploads/568_20260320100606_262.jpg",
                    "https://image.deepclick.com/uploads/644_20260320100609_678.jpg",
                    "https://image.deepclick.com/uploads/887_20260320100613_117.jpg",
                ],
                "app_labels": [
                    "Simulation",
                    "Management",
                    "Farming",
                    "Casual",
                    "Single player",
                    "Stylized",
                    "Offline",
                ],
                "app_score": "4.8",
                "app_score_detail": {"1": 0, "2": 0, "3": 0, "4": 2, "5": 10},
                "app_comment_list": [
                    {
                        "name": "Sarah Munn",
                        "avatar": "https://image.deepclick.com/uploads/018_20260320100818_122.JPG",
                        "score": 5,
                        "comment": (
                            "Great and terrible all at once. The positives, its a cute and colourful style "
                            "with story driven gameplay, but you can be fairly free in-between tasks. It can "
                            "be very relaxing to play at times. I haven't experienced any bugs or problems "
                            "and I've been playing for around 3 weeks. However, I don't think I've played a "
                            "game with such obscene pricing for upgrades and resources. I paid to remove the "
                            "ads but I've seen objects priced at GBP40/GBP50. Ludicrous. Less greed, less in "
                            "game pop ups to sell."
                        ),
                    },
                    {
                        "name": "Keith JustKeith",
                        "avatar": "https://image.deepclick.com/uploads/889_20260320100845_529.JPG",
                        "score": 5,
                        "comment": (
                            "this could be a fun time waster. but, it's constantly bombarded with ads. on "
                            "top of the regular ads, you need to watch more ads to do certain steps of the "
                            "game. or, you could always pay crazy prices, for upgrades. nothing more than an "
                            "ad based money grab game. Google Play Store needs to start cracking down on "
                            "these nonsense apps,that do this. I'm sure I'll get a generic reply from the app "
                            "provider. don't bother downloading it, it's a waste of time and energy."
                        ),
                    },
                ],
                "sdk_code": "96f9a112",
                "url_start_type": "PWA",
                "popup_desc": "",
                "popup_btn_desc": "",
                "popup_url": "",
                "start_url": "https://www.crazygames.com/game/helix-jump",
                "launch_url": "pwa01.qljtest6.xin",
            },
            "app_remark": "",
            "shopline_os_version": "3.0",
            "pre_app_id": None,
            "access_mode": "normal",
            "download_domain_id": 5000053,
            "download_path": "oss_upload/202603/20/QehHXev3/Infinity2048_ad.apk",
            "shop_url": "",
        }
