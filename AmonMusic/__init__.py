from AmonMusic.core.bot import AmonBot
from AmonMusic.core.dir import dirr
from AmonMusic.core.cookies import save_cookies
from AmonMusic.core.git import git
from AmonMusic.core.userbot import Userbot
from AmonMusic.misc import dbb, heroku

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Cookies
save_cookies()

# Bot Client
app = AlexaBot()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
