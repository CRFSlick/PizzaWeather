from App.modules.log.log import Log

log = Log()
log.clear()
log.out('This thing happened')
log.out('Oops, something went wrong here!', level='error')