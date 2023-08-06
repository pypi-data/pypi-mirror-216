import pyroherd


def dice(ctx, message):
    return hasattr(message, 'dice') and message.dice


pyroherd.filters.dice = dice