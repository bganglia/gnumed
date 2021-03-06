; Script generated by the HM NIS Edit Script Wizard.

; Find a way to automagically detect python location
; hardcode path and version for now - 2.3(23), 2.4(24)
;!define PYTHON_VERSION "24"
VAR PYTHON_PATH
Var /GLOBAL LANGGETTEXT

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "GNUmed-client"
!define PRODUCT_VERSION "0.2"
!define PRODUCT_SUBREV "8.3"
!define PRODUCT_PUBLISHER "GNUmed Systemhaus"
!define PRODUCT_WEB_SITE "http://wiki.gnumed.de"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "gnumed_util_checkprerequisites_client.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!define MUI_LICENSEPAGE_CHECKBOX
!insertmacro MUI_PAGE_LICENSE $(MUILicense)
; check prerequisites
Page custom SetPrerequisites ValidatePrerequisites
; Components page
!insertmacro MUI_PAGE_COMPONENTS
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "Albanian"
!insertmacro MUI_LANGUAGE "Arabic"
!insertmacro MUI_LANGUAGE "Belarusian"
!insertmacro MUI_LANGUAGE "Breton"
!insertmacro MUI_LANGUAGE "Bulgarian"
!insertmacro MUI_LANGUAGE "Catalan"
!insertmacro MUI_LANGUAGE "Croatian"
!insertmacro MUI_LANGUAGE "Czech"
!insertmacro MUI_LANGUAGE "Danish"
!insertmacro MUI_LANGUAGE "Dutch"
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Estonian"
!insertmacro MUI_LANGUAGE "Farsi"
!insertmacro MUI_LANGUAGE "Finnish"
!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "German"
!insertmacro MUI_LANGUAGE "Greek"
!insertmacro MUI_LANGUAGE "Hebrew"
!insertmacro MUI_LANGUAGE "Hungarian"
!insertmacro MUI_LANGUAGE "Icelandic"
!insertmacro MUI_LANGUAGE "Indonesian"
!insertmacro MUI_LANGUAGE "Italian"
!insertmacro MUI_LANGUAGE "Japanese"
!insertmacro MUI_LANGUAGE "Korean"
!insertmacro MUI_LANGUAGE "Latvian"
!insertmacro MUI_LANGUAGE "Lithuanian"
!insertmacro MUI_LANGUAGE "Luxembourgish"
!insertmacro MUI_LANGUAGE "Macedonian"
!insertmacro MUI_LANGUAGE "Mongolian"
!insertmacro MUI_LANGUAGE "Norwegian"
!insertmacro MUI_LANGUAGE "Polish"
!insertmacro MUI_LANGUAGE "Portuguese"
!insertmacro MUI_LANGUAGE "PortugueseBR"
!insertmacro MUI_LANGUAGE "Romanian"
!insertmacro MUI_LANGUAGE "Russian"
!insertmacro MUI_LANGUAGE "Serbian"
!insertmacro MUI_LANGUAGE "SerbianLatin"
!insertmacro MUI_LANGUAGE "SimpChinese"
!insertmacro MUI_LANGUAGE "Slovak"
!insertmacro MUI_LANGUAGE "Slovenian"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "Swedish"
!insertmacro MUI_LANGUAGE "Thai"
!insertmacro MUI_LANGUAGE "TradChinese"
!insertmacro MUI_LANGUAGE "Turkish"
!insertmacro MUI_LANGUAGE "Ukrainian"

!include "gnumed_mui_license.nsh"

; Section names
; A LangString for the section name
LangString Sec1Name ${LANG_ENGLISH} "GNUmed base files"
LangString Sec1Name ${LANG_DUTCH} "GNUmed base files"
LangString Sec1Name ${LANG_FRENCH} "GNUmed base files"
LangString Sec1Name ${LANG_GERMAN} "GNUmed Basisdateien"
LangString Sec1Name ${LANG_SPANISH} "GNUmed base files"
LangString Sec1Name ${LANG_ALBANIAN} "GNUmed base files"
LangString Sec1Name ${LANG_ARABIC} "GNUmed base files"
LangString Sec1Name ${LANG_BELARUSIAN} "GNUmed base files"
LangString Sec1Name ${LANG_BRETON} "GNUmed base files"
LangString Sec1Name ${LANG_BULGARIAN} "GNUmed base files"
LangString Sec1Name ${LANG_CATALAN} "GNUmed base files"
LangString Sec1Name ${LANG_CROATIAN} "GNUmed base files"
LangString Sec1Name ${LANG_CZECH} "GNUmed base files"
LangString Sec1Name ${LANG_DANISH} "GNUmed base files"
LangString Sec1Name ${LANG_ESTONIAN} "GNUmed base files"
LangString Sec1Name ${LANG_FARSI} "GNUmed base files"
LangString Sec1Name ${LANG_FINNISH} "GNUmed base files"
LangString Sec1Name ${LANG_GREEK} "GNUmed base files"
LangString Sec1Name ${LANG_HEBREW} "GNUmed base files"
LangString Sec1Name ${LANG_HUNGARIAN} "GNUmed base files"
LangString Sec1Name ${LANG_ICELANDIC} "GNUmed base files"
LangString Sec1Name ${LANG_INDONESIAN} "GNUmed base files"
LangString Sec1Name ${LANG_ITALIAN} "GNUmed base files"
LangString Sec1Name ${LANG_JAPANESE} "GNUmed base files"
LangString Sec1Name ${LANG_KOREAN} "GNUmed base files"
LangString Sec1Name ${LANG_LATVIAN} "GNUmed base files"
LangString Sec1Name ${LANG_LITHUANIAN} "GNUmed base files"
LangString Sec1Name ${LANG_LUXEMBOURGISH} "GNUmed base files"
LangString Sec1Name ${LANG_MACEDONIAN} "GNUmed base files"
LangString Sec1Name ${LANG_MONGOLIAN} "GNUmed base files"
LangString Sec1Name ${LANG_NORWEGIAN} "GNUmed base files"
LangString Sec1Name ${LANG_POLISH} "GNUmed base files"
LangString Sec1Name ${LANG_PORTUGUESE} "GNUmed base files"
LangString Sec1Name ${LANG_PORTUGUESEBR} "GNUmed base files"
LangString Sec1Name ${LANG_ROMANIAN} "GNUmed base files"
LangString Sec1Name ${LANG_RUSSIAN} "GNUmed base files"
LangString Sec1Name ${LANG_SERBIAN} "GNUmed base files"
LangString Sec1Name ${LANG_SERBIANLATIN} "GNUmed base files"
LangString Sec1Name ${LANG_SIMPCHINESE} "GNUmed base files"
LangString Sec1Name ${LANG_SLOVAK} "GNUmed base files"
LangString Sec1Name ${LANG_SLOVENIAN} "GNUmed base files"
LangString Sec1Name ${LANG_SWEDISH} "GNUmed base files"
LangString Sec1Name ${LANG_THAI} "GNUmed base files"
LangString Sec1Name ${LANG_TRADCHINESE} "GNUmed base files"
LangString Sec1Name ${LANG_TURKISH} "GNUmed base files"
LangString Sec1Name ${LANG_UKRAINIAN} "GNUmed base files"


LangString Sec2Name ${LANG_ENGLISH} "GNUmed language files"
LangString Sec2Name ${LANG_DUTCH} "GNUmed language files"
LangString Sec2Name ${LANG_FRENCH} "GNUmed language files"
LangString Sec2Name ${LANG_GERMAN} "GNUmed Sprachdateien"
LangString Sec2Name ${LANG_SPANISH} "GNUmed language files"
LangString Sec2Name ${LANG_ALBANIAN} "GNUmed language files"
LangString Sec2Name ${LANG_ARABIC} "GNUmed language files"
LangString Sec2Name ${LANG_BELARUSIAN} "GNUmed language files"
LangString Sec2Name ${LANG_BRETON} "GNUmed language files"
LangString Sec2Name ${LANG_BULGARIAN} "GNUmed language files"
LangString Sec2Name ${LANG_CATALAN} "GNUmed language files"
LangString Sec2Name ${LANG_CROATIAN} "GNUmed language files"
LangString Sec2Name ${LANG_CZECH} "GNUmed language files"
LangString Sec2Name ${LANG_DANISH} "GNUmed language files"
LangString Sec2Name ${LANG_ESTONIAN} "GNUmed language files"
LangString Sec2Name ${LANG_FARSI} "GNUmed language files"
LangString Sec2Name ${LANG_FINNISH} "GNUmed language files"
LangString Sec2Name ${LANG_GREEK} "GNUmed language files"
LangString Sec2Name ${LANG_HEBREW} "GNUmed language files"
LangString Sec2Name ${LANG_HUNGARIAN} "GNUmed language files"
LangString Sec2Name ${LANG_ICELANDIC} "GNUmed language files"
LangString Sec2Name ${LANG_INDONESIAN} "GNUmed language files"
LangString Sec2Name ${LANG_ITALIAN} "GNUmed language files"
LangString Sec2Name ${LANG_JAPANESE} "GNUmed language files"
LangString Sec2Name ${LANG_KOREAN} "GNUmed language files"
LangString Sec2Name ${LANG_LATVIAN} "GNUmed language files"
LangString Sec2Name ${LANG_LITHUANIAN} "GNUmed language files"
LangString Sec2Name ${LANG_LUXEMBOURGISH} "GNUmed language files"
LangString Sec2Name ${LANG_MACEDONIAN} "GNUmed language files"
LangString Sec2Name ${LANG_MONGOLIAN} "GNUmed language files"
LangString Sec2Name ${LANG_NORWEGIAN} "GNUmed language files"
LangString Sec2Name ${LANG_POLISH} "GNUmed language files"
LangString Sec2Name ${LANG_PORTUGUESE} "GNUmed language files"
LangString Sec2Name ${LANG_PORTUGUESEBR} "GNUmed language files"
LangString Sec2Name ${LANG_ROMANIAN} "GNUmed language files"
LangString Sec2Name ${LANG_RUSSIAN} "GNUmed language files"
LangString Sec2Name ${LANG_SERBIAN} "GNUmed language files"
LangString Sec2Name ${LANG_SERBIANLATIN} "GNUmed language files"
LangString Sec2Name ${LANG_SIMPCHINESE} "GNUmed language files"
LangString Sec2Name ${LANG_SLOVAK} "GNUmed language files"
LangString Sec2Name ${LANG_SLOVENIAN} "GNUmed language files"
LangString Sec2Name ${LANG_SWEDISH} "GNUmed language files"
LangString Sec2Name ${LANG_THAI} "GNUmed language files"
LangString Sec2Name ${LANG_TRADCHINESE} "GNUmed language files"
LangString Sec2Name ${LANG_TURKISH} "GNUmed language files"
LangString Sec2Name ${LANG_UKRAINIAN} "GNUmed language files"

LangString Sec3Name ${LANG_ENGLISH} "GNUmed documentation"
LangString Sec3Name ${LANG_DUTCH} "GNUmed documentation"
LangString Sec3Name ${LANG_FRENCH} "GNUmed documentation"
LangString Sec3Name ${LANG_GERMAN} "GNUmed Dokumentation"
LangString Sec3Name ${LANG_SPANISH} "GNUmed documentation"
LangString Sec3Name ${LANG_ALBANIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_ARABIC} "GNUmed documentation"
LangString Sec3Name ${LANG_BELARUSIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_BRETON} "GNUmed documentation"
LangString Sec3Name ${LANG_BULGARIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_CATALAN} "GNUmed documentation"
LangString Sec3Name ${LANG_CROATIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_CZECH} "GNUmed documentation"
LangString Sec3Name ${LANG_DANISH} "GNUmed documentation"
LangString Sec3Name ${LANG_ESTONIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_FARSI} "GNUmed documentation"
LangString Sec3Name ${LANG_FINNISH} "GNUmed documentation"
LangString Sec3Name ${LANG_GREEK} "GNUmed documentation"
LangString Sec3Name ${LANG_HEBREW} "GNUmed documentation"
LangString Sec3Name ${LANG_HUNGARIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_ICELANDIC} "GNUmed documentation"
LangString Sec3Name ${LANG_INDONESIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_ITALIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_JAPANESE} "GNUmed documentation"
LangString Sec3Name ${LANG_KOREAN} "GNUmed documentation"
LangString Sec3Name ${LANG_LATVIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_LITHUANIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_LUXEMBOURGISH} "GNUmed documentation"
LangString Sec3Name ${LANG_MACEDONIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_MONGOLIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_NORWEGIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_POLISH} "GNUmed documentation"
LangString Sec3Name ${LANG_PORTUGUESE} "GNUmed documentation"
LangString Sec3Name ${LANG_PORTUGUESEBR} "GNUmed documentation"
LangString Sec3Name ${LANG_ROMANIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_RUSSIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_SERBIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_SERBIANLATIN} "GNUmed documentation"
LangString Sec3Name ${LANG_SIMPCHINESE} "GNUmed documentation"
LangString Sec3Name ${LANG_SLOVAK} "GNUmed documentation"
LangString Sec3Name ${LANG_SLOVENIAN} "GNUmed documentation"
LangString Sec3Name ${LANG_SWEDISH} "GNUmed documentation"
LangString Sec3Name ${LANG_THAI} "GNUmed documentation"
LangString Sec3Name ${LANG_TRADCHINESE} "GNUmed documentation"
LangString Sec3Name ${LANG_TURKISH} "GNUmed documentation"
LangString Sec3Name ${LANG_UKRAINIAN} "GNUmed documentation"

LangString Sec4Name ${LANG_ENGLISH} "GNUmed connectors"
LangString Sec4Name ${LANG_DUTCH} "GNUmed connectors"
LangString Sec4Name ${LANG_FRENCH} "GNUmed connectors"
LangString Sec4Name ${LANG_GERMAN} "GNUmed Schnittstellen"
LangString Sec4Name ${LANG_SPANISH} "GNUmed connectors"
LangString Sec4Name ${LANG_ALBANIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_ARABIC} "GNUmed connectors"
LangString Sec4Name ${LANG_BELARUSIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_BRETON} "GNUmed connectors"
LangString Sec4Name ${LANG_BULGARIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_CATALAN} "GNUmed connectors"
LangString Sec4Name ${LANG_CROATIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_CZECH} "GNUmed connectors"
LangString Sec4Name ${LANG_DANISH} "GNUmed connectors"
LangString Sec4Name ${LANG_ESTONIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_FARSI} "GNUmed connectors"
LangString Sec4Name ${LANG_FINNISH} "GNUmed connectors"
LangString Sec4Name ${LANG_GREEK} "GNUmed connectors"
LangString Sec4Name ${LANG_HEBREW} "GNUmed connectors"
LangString Sec4Name ${LANG_HUNGARIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_ICELANDIC} "GNUmed connectors"
LangString Sec4Name ${LANG_INDONESIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_ITALIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_JAPANESE} "GNUmed connectors"
LangString Sec4Name ${LANG_KOREAN} "GNUmed connectors"
LangString Sec4Name ${LANG_LATVIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_LITHUANIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_LUXEMBOURGISH} "GNUmed connectors"
LangString Sec4Name ${LANG_MACEDONIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_MONGOLIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_NORWEGIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_POLISH} "GNUmed connectors"
LangString Sec4Name ${LANG_PORTUGUESE} "GNUmed connectors"
LangString Sec4Name ${LANG_PORTUGUESEBR} "GNUmed connectors"
LangString Sec4Name ${LANG_ROMANIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_RUSSIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_SERBIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_SERBIANLATIN} "GNUmed connectors"
LangString Sec4Name ${LANG_SIMPCHINESE} "GNUmed connectors"
LangString Sec4Name ${LANG_SLOVAK} "GNUmed connectors"
LangString Sec4Name ${LANG_SLOVENIAN} "GNUmed connectors"
LangString Sec4Name ${LANG_SWEDISH} "GNUmed connectors"
LangString Sec4Name ${LANG_THAI} "GNUmed connectors"
LangString Sec4Name ${LANG_TRADCHINESE} "GNUmed connectors"
LangString Sec4Name ${LANG_TURKISH} "GNUmed connectors"
LangString Sec4Name ${LANG_UKRAINIAN} "GNUmed connectors"

; Section descriptions
; A LangString for the section description
LangString Sec1Desc ${LANG_ENGLISH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_DUTCH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_FRENCH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_GERMAN} "Dateien, die man mindestens f�r GNUmed braucht"
LangString Sec1Desc ${LANG_SPANISH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_ALBANIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_ARABIC} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_BELARUSIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_BRETON} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_BULGARIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_CATALAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_CROATIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_CZECH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_DANISH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_ESTONIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_FARSI} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_FINNISH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_GREEK} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_HEBREW} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_HUNGARIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_ICELANDIC} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_INDONESIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_ITALIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_JAPANESE} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_KOREAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_LATVIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_LITHUANIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_LUXEMBOURGISH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_MACEDONIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_MONGOLIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_NORWEGIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_POLISH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_PORTUGUESE} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_PORTUGUESEBR} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_ROMANIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_RUSSIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_SERBIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_SERBIANLATIN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_SIMPCHINESE} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_SLOVAK} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_SLOVENIAN} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_SWEDISH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_THAI} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_TRADCHINESE} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_TURKISH} "all files needed for running GNUmed"
LangString Sec1Desc ${LANG_UKRAINIAN} "all files needed for running GNUmed"

LangString Sec2Desc ${LANG_ENGLISH} "files for non-English user interface"
LangString Sec2Desc ${LANG_DUTCH} "files for non-English user interface"
LangString Sec2Desc ${LANG_FRENCH} "files for non-English user interface"
LangString Sec2Desc ${LANG_GERMAN} "Dateien, die GNUmed international machen"
LangString Sec2Desc ${LANG_SPANISH} "files for non-English user interface"
LangString Sec2Desc ${LANG_ALBANIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_ARABIC} "files for non-English user interface"
LangString Sec2Desc ${LANG_BELARUSIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_BRETON} "files for non-English user interface"
LangString Sec2Desc ${LANG_BULGARIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_CATALAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_CROATIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_CZECH} "files for non-English user interface"
LangString Sec2Desc ${LANG_DANISH} "files for non-English user interface"
LangString Sec2Desc ${LANG_ESTONIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_FARSI} "files for non-English user interface"
LangString Sec2Desc ${LANG_FINNISH} "files for non-English user interface"
LangString Sec2Desc ${LANG_GREEK} "files for non-English user interface"
LangString Sec2Desc ${LANG_HEBREW} "files for non-English user interface"
LangString Sec2Desc ${LANG_HUNGARIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_ICELANDIC} "files for non-English user interface"
LangString Sec2Desc ${LANG_INDONESIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_ITALIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_JAPANESE} "files for non-English user interface"
LangString Sec2Desc ${LANG_KOREAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_LATVIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_LITHUANIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_LUXEMBOURGISH} "files for non-English user interface"
LangString Sec2Desc ${LANG_MACEDONIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_MONGOLIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_NORWEGIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_POLISH} "files for non-English user interface"
LangString Sec2Desc ${LANG_PORTUGUESE} "files for non-English user interface"
LangString Sec2Desc ${LANG_PORTUGUESEBR} "files for non-English user interface"
LangString Sec2Desc ${LANG_ROMANIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_RUSSIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_SERBIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_SERBIANLATIN} "files for non-English user interface"
LangString Sec2Desc ${LANG_SIMPCHINESE} "files for non-English user interface"
LangString Sec2Desc ${LANG_SLOVAK} "files for non-English user interface"
LangString Sec2Desc ${LANG_SLOVENIAN} "files for non-English user interface"
LangString Sec2Desc ${LANG_SWEDISH} "files for non-English user interface"
LangString Sec2Desc ${LANG_THAI} "files for non-English user interface"
LangString Sec2Desc ${LANG_TRADCHINESE} "files for non-English user interface"
LangString Sec2Desc ${LANG_TURKISH} "files for non-English user interface"
LangString Sec2Desc ${LANG_UKRAINIAN} "files for non-English user interface"

LangString Sec3Desc ${LANG_ENGLISH} "user manual"
LangString Sec3Desc ${LANG_DUTCH} "user manual"
LangString Sec3Desc ${LANG_FRENCH} "user manual"
LangString Sec3Desc ${LANG_GERMAN} "GNUmed Handbuch"
LangString Sec3Desc ${LANG_SPANISH} "user manual"
LangString Sec3Desc ${LANG_ALBANIAN} "user manual"
LangString Sec3Desc ${LANG_ARABIC} "user manual"
LangString Sec3Desc ${LANG_BELARUSIAN} "user manual"
LangString Sec3Desc ${LANG_BRETON} "user manual"
LangString Sec3Desc ${LANG_BULGARIAN} "user manual"
LangString Sec3Desc ${LANG_CATALAN} "user manual"
LangString Sec3Desc ${LANG_CROATIAN} "user manual"
LangString Sec3Desc ${LANG_CZECH} "user manual"
LangString Sec3Desc ${LANG_DANISH} "user manual"
LangString Sec3Desc ${LANG_ESTONIAN} "user manual"
LangString Sec3Desc ${LANG_FARSI} "user manual"
LangString Sec3Desc ${LANG_FINNISH} "user manual"
LangString Sec3Desc ${LANG_GREEK} "user manual"
LangString Sec3Desc ${LANG_HEBREW} "user manual"
LangString Sec3Desc ${LANG_HUNGARIAN} "user manual"
LangString Sec3Desc ${LANG_ICELANDIC} "user manual"
LangString Sec3Desc ${LANG_INDONESIAN} "user manual"
LangString Sec3Desc ${LANG_ITALIAN} "user manual"
LangString Sec3Desc ${LANG_JAPANESE} "user manual"
LangString Sec3Desc ${LANG_KOREAN} "user manual"
LangString Sec3Desc ${LANG_LATVIAN} "user manual"
LangString Sec3Desc ${LANG_LITHUANIAN} "user manual"
LangString Sec3Desc ${LANG_LUXEMBOURGISH} "user manual"
LangString Sec3Desc ${LANG_MACEDONIAN} "user manual"
LangString Sec3Desc ${LANG_MONGOLIAN} "user manual"
LangString Sec3Desc ${LANG_NORWEGIAN} "user manual"
LangString Sec3Desc ${LANG_POLISH} "user manual"
LangString Sec3Desc ${LANG_PORTUGUESE} "user manual"
LangString Sec3Desc ${LANG_PORTUGUESEBR} "user manual"
LangString Sec3Desc ${LANG_ROMANIAN} "user manual"
LangString Sec3Desc ${LANG_RUSSIAN} "user manual"
LangString Sec3Desc ${LANG_SERBIAN} "user manual"
LangString Sec3Desc ${LANG_SERBIANLATIN} "user manual"
LangString Sec3Desc ${LANG_SIMPCHINESE} "user manual"
LangString Sec3Desc ${LANG_SLOVAK} "user manual"
LangString Sec3Desc ${LANG_SLOVENIAN} "user manual"
LangString Sec3Desc ${LANG_SWEDISH} "user manual"
LangString Sec3Desc ${LANG_THAI} "user manual"
LangString Sec3Desc ${LANG_TRADCHINESE} "user manual"
LangString Sec3Desc ${LANG_TURKISH} "user manual"
LangString Sec3Desc ${LANG_UKRAINIAN} "user manual"

LangString Sec4Desc ${LANG_ENGLISH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_DUTCH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_FRENCH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_GERMAN} "Schnittstelle zur Anbindung von Fremprogrammen"
LangString Sec4Desc ${LANG_SPANISH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_ALBANIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_ARABIC} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_BELARUSIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_BRETON} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_BULGARIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_CATALAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_CROATIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_CZECH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_DANISH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_ESTONIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_FARSI} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_FINNISH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_GREEK} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_HEBREW} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_HUNGARIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_ICELANDIC} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_INDONESIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_ITALIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_JAPANESE} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_KOREAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_LATVIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_LITHUANIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_LUXEMBOURGISH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_MACEDONIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_MONGOLIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_NORWEGIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_POLISH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_PORTUGUESE} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_PORTUGUESEBR} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_ROMANIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_RUSSIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_SERBIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_SERBIANLATIN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_SIMPCHINESE} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_SLOVAK} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_SLOVENIAN} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_SWEDISH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_THAI} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_TRADCHINESE} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_TURKISH} "3rd party connectivity interface"
LangString Sec4Desc ${LANG_UKRAINIAN} "3rd party connectivity interface"

; MUI end ------
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}.${PRODUCT_VERSION}.${PRODUCT_SUBREV}.exe"
InstallDir "$PROGRAMFILES\GNUmed-client"
ShowInstDetails show
ShowUnInstDetails show
;---------------------
Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
  
  ;Extract InstallOptions INI files
  InitPluginsDir
  File /oname=$TEMP\temp.ini "GNUmed.ini"

  Call CheckDependencies
  Call GetPythonPath
  
  ; set GNUmed GUI language to user selected language
  StrCmp $LANGUAGE ${LANG_German} 0 +2
        StrCpy $LANGGETTEXT "--lang-gettext=de"

FunctionEnd
;---------------------
Function GetPythonPath

  ReadRegStr $R0 HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Python.exe" ""
  StrCpy $PYTHON_PATH $R0 -11

FunctionEnd
;---------------------
Function SetPrerequisites

  ;Display prerequisites dialog

  ;Push $R0
  InstallOptions::dialog "$TEMP\temp.ini"
  ;Pop $R0

FunctionEnd
;---------------------
Function ValidatePrerequisites

  ;Validate prerequisites dialog
    
FunctionEnd
;------------------------------
Section !$(Sec1Name) SEC01
  SetOverwrite try
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed"
  File "gnumed-0-2-8-3\gnumed\client\__init__.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\business"
  File "gnumed-0-2-8-3\gnumed\client\business\*.py"
  File "gnumed-0-2-8-3\gnumed\client\business\README"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\exporters"
  File "gnumed-0-2-8-3\gnumed\client\exporters\gmPatientExporter.py"
  File "gnumed-0-2-8-3\gnumed\client\exporters\__init__.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\wxGladeWidgets"
  File "gnumed-0-2-8-3\gnumed\client\wxGladeWidgets\*.py"
  File "gnumed-0-2-8-3\gnumed\client\wxGladeWidgets\__init__.py"  
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\importers"
  File "gnumed-0-2-8-3\gnumed\client\importers\gmLDTimporter.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon"
  File "gnumed-0-2-8-3\gnumed\client\pycommon\*.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools"
  File "gnumed-0-2-8-3\gnumed\client\pycommon\tools\*.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon"
  File "gnumed-0-2-8-3\gnumed\client\pycommon\__init__.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed"
  File "gnumed-0-2-8-3\gnumed\client\sitecustomize.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython"
  File "gnumed-0-2-8-3\gnumed\client\wxpython\*.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\gui"
  File "gnumed-0-2-8-3\gnumed\client\wxpython\gui\*.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\patient"
  File "gnumed-0-2-8-3\gnumed\client\wxpython\patient\*.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython"
  File "gnumed-0-2-8-3\gnumed\client\wxpython\__init__.py"
  SetOutPath "$INSTDIR"
  File "gnumed-0-2-8-3\gnumed\client\__init__.py"

  SetOutPath "$INSTDIR\bin"
  File "gnumed-0-2-8-3\gnumed\client\wxpython\gnumed.py"
  Rename "$INSTDIR\bin\gnumed.py" "$INSTDIR\bin\gnumed.pyw"
  
  SetOutPath "$INSTDIR"
  File "gnumed-0-2-8-3\gnumed\client\gm-from-vcs.conf"
  Rename "$INSTDIR\gm-from-vcs.conf" "$INSTDIR\gnumed.conf"
  
  SetOutPath "$INSTDIR\bitmaps"
  File "gnumed-0-2-8-3\gnumed\client\wxpython\__init__.py"
  File "gnumed-0-2-8-3\gnumed\client\bitmaps\*.png"

  SetOutPath "$INSTDIR"
  CreateDirectory "$SMPROGRAMS\GNUmed"
  CreateShortCut "$SMPROGRAMS\GNUmed\GNUmed.lnk" '"$INSTDIR\bin\gnumed.pyw"' '--conf-file="$INSTDIR\gnumed.conf" $LANGGETTEXT'\
  "" 2 SW_SHOWNORMAL ALT|CTRL|G "This is the GNUmed reference client"
  CreateShortCut "$SMPROGRAMS\GNUmed\GNUmed(slave mode).lnk" '"$INSTDIR\bin\gnumed.pyw"' '--conf-file="$INSTDIR\gnumed.conf" --slave $LANGGETTEXT'\
  "" 2 SW_SHOWNORMAL ALT|CTRL|V "This is the GNUmed reference client in slave mode"
  CreateDirectory "$SMPROGRAMS\GNUmed\config"
  CreateShortCut "$SMPROGRAMS\GNUmed\config\gnumed.conf.lnk" "notepad" '"$INSTDIR\gnumed.conf"'\
  "" 2 SW_SHOWNORMAL ALT|CTRL|G "Use this to edit GNUmed reference client config file"
  CreateShortCut "$SMPROGRAMS\GNUmed\config\gm_ctl_client.conf.lnk" "notepad" '"$INSTDIR\gm_ctl_client.conf"'\
  "" 2 SW_SHOWNORMAL ALT|CTRL|G "Use this to edit GNUmed reference client slave mode config file"
SectionEnd

Section !$(Sec2Name) SEC02
  SetOverwrite try
  SetOutPath "$INSTDIR\locale\de\LC_MESSAGES"
  File "gnumed-0-2-8-3\gnumed\client\locale\de-gnumed.mo"
  Rename "$INSTDIR\locale\de\LC_MESSAGES\de-gnumed.mo" "$INSTDIR\locale\de\LC_MESSAGES\gnumed.mo"
  SetOutPath "$INSTDIR\locale\de_DE\LC_MESSAGES"
  File "gnumed-0-2-8-3\gnumed\client\locale\de-gnumed.mo"
  Rename "$INSTDIR\locale\de_DE\LC_MESSAGES\de-gnumed.mo" "$INSTDIR\locale\de_DE\LC_MESSAGES\gnumed.mo"
  SetOutPath "$INSTDIR\locale\es\LC_MESSAGES"
  File "gnumed-0-2-8-3\gnumed\client\locale\es-gnumed.mo"
  Rename "$INSTDIR\locale\es\LC_MESSAGES\es-gnumed.mo" "$INSTDIR\locale\es\LC_MESSAGES\gnumed.mo"
  SetOutPath "$INSTDIR\locale\es_ES\LC_MESSAGES"
  File "gnumed-0-2-8-3\gnumed\client\locale\es-gnumed.mo"
  Rename "$INSTDIR\locale\es_ES\LC_MESSAGES\es-gnumed.mo" "$INSTDIR\locale\es_ES\LC_MESSAGES\gnumed.mo"
  SetOutPath "$INSTDIR\locale\fr\LC_MESSAGES"
  File "gnumed-0-2-8-3\gnumed\client\locale\fr-gnumed.mo"
    Rename "$INSTDIR\locale\fr\LC_MESSAGES\fr-gnumed.mo" "$INSTDIR\locale\fr\LC_MESSAGES\gnumed.mo"
  SetOutPath "$INSTDIR\locale\fr_FR\LC_MESSAGES"
  File "gnumed-0-2-8-3\gnumed\client\locale\fr-gnumed.mo"
    Rename "$INSTDIR\locale\fr_FR\LC_MESSAGES\fr-gnumed.mo" "$INSTDIR\locale\fr_FR\LC_MESSAGES\gnumed.mo"
SectionEnd

Section !$(Sec3Name) SEC03
  SetOutPath "$INSTDIR\doc\medical_knowledge\de\STIKO"
  ;File "gnumed-0-2-8-3\gnumed\client\doc\medical_knowledge\de\STIKO\STI_NEU.htm"
  SetOutPath "$INSTDIR\doc\user-manual"
  ;File "user-manual\*.html"
SectionEnd

Section !$(Sec4Name) SEC04
  SetOutPath "$INSTDIR"
  File "gnumed-0-2-8-3\gnumed\client\connectors\gm_ctl_client.conf"
  File "gnumed-0-2-8-3\gnumed\client\connectors\gm_ctl_client-doc-viewer.conf"
  File "gnumed-0-2-8-3\gnumed\client\connectors\gm_ctl_client-doc-management.conf"
  SetOutPath "$INSTDIR\bin" 
  File "gnumed-0-2-8-3\gnumed\client\connectors\gm_ctl_client.py"
  Rename "$INSTDIR\bin\gm_ctl_client.py" "$INSTDIR\bin\gm_ctl_client.pyw"
SectionEnd

Section -AdditionalIcons
  SetOutPath $INSTDIR
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateDirectory "$SMPROGRAMS\GNUmed"
  CreateShortCut "$SMPROGRAMS\GNUmed\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\GNUmed\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

; Section descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} $(Sec1Desc)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} $(Sec2Desc)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC03} $(Sec3Desc)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC04} $(Sec4Desc)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) wurde erfolgreich deinstalliert."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "M�chten Sie $(^Name) und alle seinen Komponenten deinstallieren?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\doc\medical_knowledge\de\STIKO\*"
  Delete "$INSTDIR\doc\user-manual\*.*"
  Delete "$INSTDIR\locale\fr_FR\LC_MESSAGES\*.*"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\*.*"
  Delete "$INSTDIR\locale\es_ES\LC_MESSAGES\*.*"
  Delete "$INSTDIR\locale\es\LC_MESSAGES\*.*"
  Delete "$INSTDIR\locale\de_DE\LC_MESSAGES\*.*"
  Delete "$INSTDIR\locale\de\LC_MESSAGES\*.*"
  Delete "$INSTDIR\*.*"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\patient\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\patient\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\gui\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\gui\*.pyc"
  Delete "$INSTDIR\bin\*.*"
  Delete "$INSTDIR\bitmaps\*.*"
  Delete "$INSTDIR\pixmaps\*.*"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools\CVS\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\importers\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\importers\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\wxGladeWidgets\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\wxGladeWidgets\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\exporters\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\exporters\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\business\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\business\*.pyc"

  Delete "$SMPROGRAMS\GNUmed\Uninstall.lnk"
  Delete "$SMPROGRAMS\GNUmed\Website.lnk"
  Delete "$SMPROGRAMS\GNUmed\GNUmed.lnk"
  Delete "$SMPROGRAMS\GNUmed\GNUmed(slave mode).lnk"
  Delete "$SMPROGRAMS\GNUmed\config\gnumed.conf.lnk"
  Delete "$SMPROGRAMS\GNUmed\config\gm_ctl_client.conf.lnk"

  RMDir "$SMPROGRAMS\GNUmed"
  RMDir "$SMPROGRAMS\GNUmed\config"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\patient"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython\gui"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\wxpython"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\importers"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\exporters"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\business"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed"
  RMDir "$INSTDIR\pixmaps"
  RMDir "$INSTDIR\bin"
  RMDir "$INSTDIR\doc\medical_knowledge\de\STIKO"
  RMDir "$INSTDIR\doc\medical_knowledge\de"
  RMDir "$INSTDIR\doc\medical_knowledge"
  RMDir "$INSTDIR\doc\user-manual"
  RMDir "$INSTDIR\doc"
  RMDir "$INSTDIR\locale\fr_FR\LC_MESSAGES"
  RMDir "$INSTDIR\locale\fr_FR"
  RMDir "$INSTDIR\locale\fr\LC_MESSAGES"
  RMDir "$INSTDIR\locale\fr"
  RMDir "$INSTDIR\locale\es_ES\LC_MESSAGES"
  RMDir "$INSTDIR\locale\es_ES"
  RMDir "$INSTDIR\locale\es\LC_MESSAGES"
  RMDir "$INSTDIR\locale\es"
  RMDir "$INSTDIR\locale\de_DE\LC_MESSAGES"
  RMDir "$INSTDIR\locale\de_DE"
  RMDir "$INSTDIR\locale\de\LC_MESSAGES"
  RMDir "$INSTDIR\locale\de"
  RMDir "$INSTDIR\locale"
  RMDir "$INSTDIR\bitmaps"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd