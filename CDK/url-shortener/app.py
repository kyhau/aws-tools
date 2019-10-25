#!/usr/bin/env python3
from aws_cdk.core import App

from url_shortener.url_shortener_stack import UrlShortenerStack, TrafficStack


app = App()

UrlShortenerStack(app, "url-shortener", env={
    "region": "ap-southeast-2",
    "account": "todo",
})

TrafficStack(app, "url-shortener-load-test", env={
    "region": "ap-southeast-2",
    "account": "todo",
})

app.synth()
