from typing import Dict, List


thread_count: int = 0
thread_timeout: int = 10  # timeout for single dump work
progress_session_timeout: int = 60  # timeout for huge work
process_timeout: int = 600  # timeout for total run
thread_output_directory: str = None

plugin_decompiler_enable_pycdc = False
plugin_decompiler_enable_uncompyle6 = False

decompile_file:Dict = None # only decompile_file in this filename , if set to `None` ,all fit files will be decompile



############# DEBUG
DEBUG_TestPycDump = False
