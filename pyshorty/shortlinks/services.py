import random
import string

from redis.asyncio.client import StrictRedis


_PATTERN_SHORT_ID_2_DESTINATION_URL = "shortlink:short_id:{}:destination_url"
_PATTERN_SHORT_ID_2_HITS = "shortlink:short_id:{}:hits"


def _generate_short_id(length: int) -> str:
    characters = string.ascii_letters + string.digits + "-_"
    similar_characters = "O0I1l"

    # Remove similar looking characters
    for char in similar_characters:
        characters = characters.replace(char, "")

    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


class CreateShortlinkError(Exception):
    pass


async def create_shortlink(r_con: StrictRedis, destination_url: str) -> str:
    for _ in range(10):
        short_id = _generate_short_id(length=6)
        was_set = await r_con.set(
            _PATTERN_SHORT_ID_2_DESTINATION_URL.format(short_id), destination_url
        )
        if was_set:
            return short_id

    raise CreateShortlinkError(
        "Exceeded tries to create short id which wasn't used earlier"
    )


async def increase_hits(r_con: StrictRedis, short_id: str) -> None:
    await r_con.incr(_PATTERN_SHORT_ID_2_HITS.format(short_id))


async def get_destination_url_by_short_id(
    r_con: StrictRedis, short_id: str
) -> str | None:
    destination_url = await r_con.get(
        _PATTERN_SHORT_ID_2_DESTINATION_URL.format(short_id)
    )
    return destination_url
