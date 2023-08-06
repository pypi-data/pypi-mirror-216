import platform, os
import pdfixsdk.Pdfix
import pdfixsdk.OcrTesseract

# get the shared library name based on the platform
def getModuleName(module):
  proc = platform.processor()
  pltfm = platform.system()
  if pltfm == 'Darwin':
    if proc == "arm":
      return 'arm64/lib' + module + '.dylib'  
    else:
      return 'x64/lib' + module + '.dylib'
  elif pltfm == "Windows":
    return 'x64/' + module + '.dll'
  elif pltfm == "Linux":
      return 'x64/lib' + module + '.so'
  
# load pdfix library from the current folder
basePath = os.path.dirname(os.path.abspath(__file__))
pdfixsdk.Pdfix.Pdfix_init(basePath + "/bin/" + getModuleName('pdf'))
pdfixsdk.OcrTesseract.OcrTesseract_init(basePath + "/bin/" + getModuleName('ocr_tesseract'))