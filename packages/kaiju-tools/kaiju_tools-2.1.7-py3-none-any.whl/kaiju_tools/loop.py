"""Asyncio loop initialization."""

import asyncio
import os

if os.name != 'nt':
    import uvloop  # noqa: legacy

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

loop = asyncio.get_event_loop()
