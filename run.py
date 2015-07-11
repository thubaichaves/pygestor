try:

    import __init__

except Exception, e:
    import logging
    logging.exception(e)
    # import urwid
    # raise urwid.ExitMainLoop()
    pass