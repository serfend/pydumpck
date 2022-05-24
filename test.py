import pydumpck.tests.test_file_analysis
import pydumpck.tests.common.res_type
elf = pydumpck.tests.common.res_type.resources_arch['pyz']
pydumpck.tests.test_file_analysis.test_arch_file((elf, None))
# elf = pydumpck.tests.common.res_type.resources_arch['elf']
# pydumpck.tests.test_file_analysis.test_arch_file((elf, None))
