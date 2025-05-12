import logging
import sys
import wandb

class WandbHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        wandb.log({record.levelname.lower(): log_entry})

def get_logger(name: str = __name__, project_name: str = __name__) -> logging.Logger:

    wandb.init(project=project_name, reinit=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) 

    fmt = logging.Formatter(
        '[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(fmt)
    logger.addHandler(info_handler)

    debug_handler = logging.StreamHandler(sys.stderr)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(fmt)
    logger.addHandler(debug_handler)

    wandb_handler = WandbHandler()
    wandb_handler.setLevel(logging.INFO)
    wandb_handler.setFormatter(fmt)
    logger.addHandler(wandb_handler)

    return logger
