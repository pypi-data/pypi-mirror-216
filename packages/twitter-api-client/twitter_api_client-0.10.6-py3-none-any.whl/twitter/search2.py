import platform
from pathlib import Path

import orjson
from httpx import Client

from twitter.util import find_key, build_params

reset = '\u001b[0m'
colors = [f'\u001b[{i}m' for i in range(30, 38)]

try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        import nest_asyncio

        nest_asyncio.apply()
except:
    ...

if platform.system() != 'Windows':
    try:
        import uvloop

        uvloop.install()
    except ImportError as e:
        ...


def search(query: str, category: str):
    client = Client(
        cookies={
            'guest_id': 'v1%3A168737090373758410',
            '_twitter_sess': 'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCBW9JN%252BIAToMY3NyZl9p%250AZCIlMWZiZjAzOTVlMDBkM2NjMjkwNGExNzkwMTY1ZmEwOTU6B2lkIiVmMDU4%250AZTIzMDRmYmVlZGM2NTFjMDQ5MmZhYjgxZDRiNg%253D%253D--073922813a1212231868089e884aa84d2f4c7b22',
            'kdt': 'ycSfUFF5bwCeeCU6wXJV4vxTIDEiSLW8gWakzmdS',
            'auth_token': 'dca933479b2548ca4c6c584846477457fa918f04',
            'ct0': 'e5b6c8f2ca01f8a4f7d4b8fe500e2dda3ed799259240db9e99bf50a2e2536346a312572f590c233c77485f535fb16cd1622fd06913d04182e79e05401c926c5f9f11901943cb01a385d7d11da246702d',
            'lang': 'en',
            'twid': 'u%3D1669836662040596482',
            'att': '1-EVXkPtTWBCgeNidIyutFxMDuRNvVQI662kOiG0UD',
            'guest_id_marketing': 'v1%3A168737090373758410',
            'guest_id_ads': 'v1%3A168737090373758410',
            'personalization_id': '"v1_pG5lxI/le/P8Lr44IRjXZA=="',
        },
        headers={
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            # 'cookie': 'guest_id=v1%3A168737090373758410; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCBW9JN%252BIAToMY3NyZl9p%250AZCIlMWZiZjAzOTVlMDBkM2NjMjkwNGExNzkwMTY1ZmEwOTU6B2lkIiVmMDU4%250AZTIzMDRmYmVlZGM2NTFjMDQ5MmZhYjgxZDRiNg%253D%253D--073922813a1212231868089e884aa84d2f4c7b22; kdt=ycSfUFF5bwCeeCU6wXJV4vxTIDEiSLW8gWakzmdS; auth_token=dca933479b2548ca4c6c584846477457fa918f04; ct0=e5b6c8f2ca01f8a4f7d4b8fe500e2dda3ed799259240db9e99bf50a2e2536346a312572f590c233c77485f535fb16cd1622fd06913d04182e79e05401c926c5f9f11901943cb01a385d7d11da246702d; lang=en; twid=u%3D1669836662040596482; att=1-EVXkPtTWBCgeNidIyutFxMDuRNvVQI662kOiG0UD; guest_id_marketing=v1%3A168737090373758410; guest_id_ads=v1%3A168737090373758410; personalization_id="v1_pG5lxI/le/P8Lr44IRjXZA=="',
            'pragma': 'no-cache',
            'referer': 'https://twitter.com/search?q=argentina&src=typed_query',
            'sec-ch-ua': '"Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-client-uuid': '995285a0-0781-498c-a4d5-c33897872736',
            'x-csrf-token': 'e5b6c8f2ca01f8a4f7d4b8fe500e2dda3ed799259240db9e99bf50a2e2536346a312572f590c233c77485f535fb16cd1622fd06913d04182e79e05401c926c5f9f11901943cb01a385d7d11da246702d',
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
        }
    )

    params = {
        'features': {
            'rweb_lists_timeline_redesign_enabled': True,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': False,
            'creator_subscriptions_tweet_preview_api_enabled': True,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'tweetypie_unmention_optimization_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'tweet_awards_web_tipping_enabled': False,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': False,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'responsive_web_enhance_cards_enabled': False
        },
        'variables': {
            'rawQuery': query,
            'count': 20,
            'querySource': 'typed_query',
            'product': category  # Top Latest People Photos Videos
        }
    }

    _id, op = 'GcjM7tlxA-EAM98COHsYwg', 'SearchTimeline'
    r = client.get(
        f'https://twitter.com/i/api/graphql/{_id}/{op}',
        params=build_params(params),
    )
    data = r.json()
    entries = [y for x in find_key(data, 'entries') for y in x]
    for e in entries:
        if e.get('entryId') == 'cursor-bottom-0':
            prev_cursor = e['content']['value']

    cursor = prev_cursor
    total = set()
    while True:
        if cursor:
            params['variables']['cursor'] = cursor

        _id, op = 'GcjM7tlxA-EAM98COHsYwg', 'SearchTimeline'
        r = client.get(
            f'https://twitter.com/i/api/graphql/{_id}/{op}',
            params=build_params(params),
        )
        data = r.json()
        entries = [y for x in find_key(data, 'entries') for y in x]
        Path('r.json').write_bytes(orjson.dumps(entries, option=orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2))

        for e in entries:
            if e.get('entryId') == 'cursor-bottom-0': # and prev_cursor != e['content']['value']:
                cursor = e['content']['value']
            # elif e.get('entryId').startswith('cursor-top'):
            #     cursor = e['content']['value']

        unq = {x for x in find_key(entries, 'entryId') if 'user' in x or 'tweet' in x}
        # print(f'{len(unq) = }')
        # print(f'{cursor = }')
        total |= unq
        print(f'{len(total) = }')


def main():
    search('argentina', 'Top')


if __name__ == '__main__':
    main()
