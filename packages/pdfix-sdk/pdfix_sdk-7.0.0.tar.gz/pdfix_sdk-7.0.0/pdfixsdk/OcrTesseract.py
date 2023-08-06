################################################################################
# Copyright (c) 2023 PDFix (http://pdfix.net). All Rights Reserved.
# This file was generated automatically
################################################################################
from ctypes import Structure, c_int, c_bool, c_void_p, c_double, c_float, byref, POINTER, c_wchar_p, c_char_p, c_ubyte, create_unicode_buffer, cdll
from pdfixsdk.Pdfix import *

# Enumerators
# OcrTesseractPageSegType
(kOcrSegOSDOnly, kOcrSegAutoOSD, kOcrSegAutoOnly, kOcrSegAuto, kOcrSegSingleColumn, kOcrSegSingleBlockVertText, kOcrSegSingleBlock, kOcrSegSingleLine, kOcrSegSingleWord, kOcrSegCircleWord, kOcrSegSingleChar, kOcrSegSparseText, kOcrSegSparseTextOSD, kOcrSegRawLine) = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
# OcrTesseractEngineType
(kOcrTesseractOnly, kOcrTesseractLSTMOnlly, kOcrTesseractLSTMCombined, kOcrTesseractDefault) = (0, 1, 2, 3)

# Structures - Private
# Structures - Public
# Objects
class _OcrTesseractBase(object):
    def __init__(self, _obj):
        self.obj = _obj

# forward class declaration
class OcrTesseract: pass
class TesseractDoc: pass

# class definitions 
class OcrTesseract(PdfixPlugin):
    def __init__(self, _obj):
        super(OcrTesseract, self).__init__(_obj)

    def SetLanguage(self, _lang) -> bool: 
        global OcrTesseractLib
        ret = OcrTesseractLib.OcrTesseractSetLanguage(self.obj, _lang)
        return ret

    def SetDataPath(self, _path) -> bool: 
        global OcrTesseractLib
        ret = OcrTesseractLib.OcrTesseractSetDataPath(self.obj, _path)
        return ret

    def SetEngine(self, _engine: int) -> bool: 
        global OcrTesseractLib
        ret = OcrTesseractLib.OcrTesseractSetEngine(self.obj, _engine)
        return ret

    def OpenOcrDoc(self, _pdDoc: PdfDoc) -> TesseractDoc: 
        global OcrTesseractLib
        ret = OcrTesseractLib.OcrTesseractOpenOcrDoc(self.obj, _pdDoc.obj)
        if ret:
            return TesseractDoc(ret)
        else:
            return None

class TesseractDoc(_OcrTesseractBase):
    def __init__(self, _obj):
        super(TesseractDoc, self).__init__(_obj)

    def Close(self) -> bool: 
        global OcrTesseractLib
        ret = OcrTesseractLib.TesseractDocClose(self.obj)
        return ret

    def OcrImageToPage(self, _image: PsImage, _matrix: PdfMatrix, _page: PdfPage, _cancel_proc, _cancel_data: int) -> bool: 
        global OcrTesseractLib
        ret = OcrTesseractLib.TesseractDocOcrImageToPage(self.obj, _image.obj, _matrix.GetIntStruct(), _page.obj, _cancel_proc, _cancel_data)
        return ret

def GetOcrTesseract():
    global OcrTesseractLib
    obj = OcrTesseractLib.GetOcrTesseract()
    return OcrTesseract(obj)

OcrTesseractLib = None

def OcrTesseract_init(path):
    global OcrTesseractLib
    OcrTesseractLib = cdll.LoadLibrary(path)
    if OcrTesseractLib is None:
        raise Exception("LoadLibrary fail")
    OcrTesseractLib.OcrTesseractSetLanguage.restype = c_int
    OcrTesseractLib.OcrTesseractSetLanguage.argtypes = [c_void_p, c_wchar_p]
    OcrTesseractLib.OcrTesseractSetDataPath.restype = c_int
    OcrTesseractLib.OcrTesseractSetDataPath.argtypes = [c_void_p, c_wchar_p]
    OcrTesseractLib.OcrTesseractSetEngine.restype = c_int
    OcrTesseractLib.OcrTesseractSetEngine.argtypes = [c_void_p, c_int]
    OcrTesseractLib.OcrTesseractOpenOcrDoc.restype = c_void_p
    OcrTesseractLib.OcrTesseractOpenOcrDoc.argtypes = [c_void_p, c_void_p]
    OcrTesseractLib.TesseractDocClose.restype = c_int
    OcrTesseractLib.TesseractDocClose.argtypes = [c_void_p]
    OcrTesseractLib.TesseractDocOcrImageToPage.restype = c_int
    OcrTesseractLib.TesseractDocOcrImageToPage.argtypes = [c_void_p, c_void_p, POINTER(zz_PdfMatrix), c_void_p, c_int, c_void_p]
    OcrTesseractLib.GetOcrTesseract.restype = c_void_p

def OcrTesseract_destroy():
    global OcrTesseractLib
    del OcrTesseractLib
    OcrTesseractLib = None

