
def select_function(updater,func):
    update_queue = updater.update_queue
    update_queue.put_nowait("/{}".format(func))