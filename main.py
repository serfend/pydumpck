import pydumpck
import pydumpck.configuration
pydumpck.logger.root.handlers.clear() # seems some package pollute it
pydumpck.run()