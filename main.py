from XClientTransaction.x_client_transaction.utils import get_ondemand_file_url
from XClientTransaction.x_client_transaction import ClientTransaction
import requests
import bs4
import random
import os
import pprint

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
AUTH_TOKEN = os.environ["auth_token"]

home_page = requests.get(
    "https://x.com",
    headers={
        "Authority": "x.com",
        "Referer": "https://x.com",
        "User-Agent": UA,
    },
)
home_page_response = bs4.BeautifulSoup(home_page.content, "html.parser")
ondemand_url = get_ondemand_file_url(home_page_response)
if ondemand_url is None:
    print("Failed to fetch ondemand_url")
    exit(1)
ondemand_file = requests.get(ondemand_url)
ondemand_file_response = bs4.BeautifulSoup(ondemand_file.text, "html.parser")
ct = ClientTransaction(home_page_response, ondemand_file_response)

r = requests.get(b"https://x.com/home", cookies={"auth_token": AUTH_TOKEN})

endpoint = "/i/api/graphql/LBFRMJBLzXkI-zdK3fCj1Q/CreateTweet"
headers = {
    "User-Agent": UA,
    "authorization": f"Bearer {BEARER_TOKEN}",
    "x-client-transaction-id": ct.generate_transaction_id("GET", endpoint),
    "x-csrf-token": r.cookies.get_dict()["ct0"],
}


json_data = {
    "variables": {
        "tweet_text": "".join(random.choices("ABCDEFG0123456789", k=3)),
        "dark_request": False,
        "media": {
            "media_entities": [],
            "possibly_sensitive": False,
        },
        "semantic_annotation_ids": [],
        "disallowed_reply_options": None,
    },
    "features": {
        "premium_content_api_read_enabled": False,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
        "responsive_web_grok_analyze_post_followups_enabled": True,
        "responsive_web_jetfuel_frame": False,
        "responsive_web_grok_share_attachment_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "responsive_web_grok_show_grok_translated_post": False,
        "responsive_web_grok_analysis_button_from_backend": True,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "payments_enabled": False,
        "profile_label_improvements_pcf_label_in_post_enabled": True,
        "rweb_tipjar_consumption_enabled": True,
        "verified_phone_label_enabled": False,
        "articles_preview_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "responsive_web_grok_image_annotation_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_enhance_cards_enabled": False,
    },
    "queryId": "LBFRMJBLzXkI-zdK3fCj1Q",
}

cookies = {
    "auth_token": AUTH_TOKEN,
    "ct0": r.cookies.get_dict()["ct0"],
    "_twitter_sess": "BAh7CCIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADofbGFzdF9wYXNzd29yZF9jb25maXJtYXRpb24i%250AFTE3MzgxNTM3Njg5MTcwMDA6HnBhc3N3b3JkX2NvbmZpcm1hdGlvbl91aWQi%250ADjM2NTYyNTg1NA%253D%253D--b75005749ed224f74638c1879699353f497feed6",
}

s = requests.session()
for i in range(2):
    r = s.post(
        f"https://x.com/{endpoint}",
        headers=headers,
        json=json_data,
        cookies=cookies,
    )
    pprint.pp(r.cookies.get_dict())
    pprint.pp(r.json())
