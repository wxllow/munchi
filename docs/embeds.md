# Embeds format

```json
{
    "title": str,
    "description": str,
    "url": str,
    "color": hex,
    "timestamp": datetime,
    "footer": {
        "text": str,
        "icon_url": url
    },
    "thumbnail": {
        "url": url
    },
    "image": {
        "url": url
    },
    "author": {
        "name": str,
        "url": url,
        "icon_url": url
    },
    "fields": [
        {
        "name": str,
        "value": str,
        "inline": bool
        }
    ]
}
```
