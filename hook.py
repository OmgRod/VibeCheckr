from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('transformers.models')

if 'transformers.models.doge' in hiddenimports:
    hiddenimports.remove('transformers.models.doge')
