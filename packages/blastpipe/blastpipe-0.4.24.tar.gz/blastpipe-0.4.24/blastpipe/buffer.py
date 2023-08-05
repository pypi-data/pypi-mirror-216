"""Utilities for writing and reading length-prefix framed messages.
Using length-prefixed framing makes it easier for the reader to determine the
boundaries of each message before passing it to msgspec to be decoded.
"""
# Copyright 2023 Ross J. Duff MSc
# The copyright holder licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import asyncio  # pragma: defer to asyncio

from . import public  # pragma: no cover


@public  # pragma: defer to python
async def prefixed_send(stream: asyncio.StreamWriter, buffer: bytes) -> None:
    """Write a length-prefixed buffer to the stream"""
    # Encode the message length as a 4 byte big-endian integer.
    prefix = len(buffer).to_bytes(4, "big")

    # Write the prefix and buffer to the stream.
    stream.write(prefix)
    await stream.drain()

    stream.write(buffer)
    await stream.drain()


@public  # pragma: defer to python
async def prefixed_recv(stream: asyncio.StreamReader) -> bytes:
    """Read a length-prefixed buffer from the stream"""
    # Read the next 4 byte prefix
    prefix = await stream.readexactly(4)

    # Convert the prefix back into an integer for the next message length
    # pylint: disable=invalid-name
    n = int.from_bytes(prefix, "big")

    # Read in the full message buffer
    return await stream.readexactly(n)
