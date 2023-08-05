from log_translate.data_struct import Log, Level
from log_translate.log_translator import *


class CrashPatternTranslator(TagPatternTranslator):
    def __init__(self):
        super().__init__({
            r"AndroidRuntime|FATAL.*|System.err.*": activity_task_translator
        })


def activity_task_translator(tag, msg):
    # todo 这里需要过滤包名
    return Log(translated=" ------ %s > %s----- " % (tag, msg), level=Level.e)


if __name__ == '__main__':
    print(re.compile(".*Task").match("aaTas8km"))
    print(CrashPatternTranslator().translate("FATAL EION", "你好"))
