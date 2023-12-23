import logging

from kesha.kesha.main import main

logging.basicConfig(
    level=logging.INFO,
    filename="bot.log"
)

main()
