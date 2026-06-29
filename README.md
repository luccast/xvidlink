# xvidlink

Extract a direct video URL from an X/Twitter post link.

## Install

```sh
./install.sh
```

Symlinks `xvidlink` into `~/.local/bin` (must be on your PATH).

## Usage

```sh
xvidlink "https://x.com/JayGenXer/status/2071324615733874702?s=20"
```

Accepts full `x.com` or `twitter.com` URLs (with or without query params) or a bare tweet ID.

Output:

```
https://video.twimg.com/amplify_video/2071324541498892288/vid/avc1/576x1024/C2MQNoZuyFu_VlXF.mp4
```

## How it works

Parses the tweet ID from the input, queries Twitter's unauthenticated syndication API, and selects the highest-bitrate MP4 variant.
