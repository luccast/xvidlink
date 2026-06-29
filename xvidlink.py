#!/usr/bin/env python3
"""xvidlink - extract a direct video URL from an X/Twitter post link."""

import re
import sys
import requests

SYNDICATION_URL = "https://cdn.syndication.twimg.com/tweet-result"


def extract_tweet_id(text: str) -> str:
    """Pull the numeric tweet ID out of a URL or raw ID string."""
    m = re.search(r"/status(?:es)?/(\d+)", text)
    if m:
        return m.group(1)
    m = re.match(r"^(\d{15,})$", text.strip())
    if m:
        return m.group(1)
    raise ValueError(f"could not find a tweet ID in: {text}")


def get_video_url(tweet_id: str) -> str:
    """Return the highest-bitrate direct mp4 URL for a tweet's video."""
    resp = requests.get(SYNDICATION_URL, params={"id": tweet_id, "token": "a"},
                        timeout=15)
    resp.raise_for_status()
    data = resp.json()

    best_url, best_br = None, -1
    for media in data.get("mediaDetails", []):
        for v in media.get("video_info", {}).get("variants", []):
            if v.get("content_type") == "video/mp4":
                br = v.get("bitrate", 0) or 0
                if br > best_br:
                    best_url, best_br = v["url"], br
    if not best_url:
        raise ValueError(f"no video found in tweet {tweet_id}")
    return best_url.split("?")[0]  # ponytail: strip ?tag query param, not needed for direct play


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <x-url-or-tweet-id>", file=sys.stderr)
        return 2
    try:
        tweet_id = extract_tweet_id(argv[1])
        print(get_video_url(tweet_id))
    except (ValueError, requests.RequestException) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        assert extract_tweet_id("https://x.com/JayGenXer/status/2071324615733874702?s=20") == "2071324615733874702"
        assert extract_tweet_id("https://twitter.com/u/status/123456789012345678") == "123456789012345678"
        assert extract_tweet_id("2071324615733874702") == "2071324615733874702"
        print("self-test ok")
    else:
        sys.exit(main(sys.argv))
