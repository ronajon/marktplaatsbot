import logging

def setup_logging(args, logfilename):
    handlers = []

    if args.logtoscreen or (not args.logtofile):
        handlers.append(logging.StreamHandler())

    if args.logtofile:
        handlers.append(logging.FileHandler(logfilename))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers
    )

    return logging.getLogger(__name__)