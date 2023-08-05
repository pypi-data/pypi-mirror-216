from business.AndroidCrashPattern_translator import CrashPatternTranslator
from business.bluetooth_translator import BluetoothTranslator
from log_translator import SysLogTranslator

translators = [SysLogTranslator(tag_translators=[BluetoothTranslator(), CrashPatternTranslator()])]
