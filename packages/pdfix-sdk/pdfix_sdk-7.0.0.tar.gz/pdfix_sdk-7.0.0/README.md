# PDFix SDK Package

## PDFix SDK - High Performace PDF library

`keywords: pdf, accessibility, remediation, extraction, html, conversion, render, watermark, redact, sign, forms`

PDFix SDK analyses the key components of the PDF and makes it easily available for you to manipulate. It’s a high-performance library that helps software developers and end-users integrate PDF functionality into their workflows.

## Features
- Automated PDF Remediation (PDF/UA)
- Automated Data Extraction (JSON, XML)
- PDF to HTML Conversion (Original, Responsive, by Tags)
- Standard PDF Editing Features (render, watermark, redact, sign, forms, and more)

## Installation 

```
pip install pdfix-sdk
```

## Example

```
from pdfixsdk.Pdfix import *

pdfix = GetPdfix()
doc = pdfix.OpenDoc("path/to/your.pdf", "")
print(doc.GetNumPages())
doc.Close()
```

