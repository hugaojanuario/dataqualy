from PyInstaller.utils.hooks import collect_all


pyspark_data, pyspark_binaries, pyspark_hiddenimports = collect_all("pyspark")

analysis = Analysis(
    ["src/dataqualy/__main__.py"],
    pathex=["src"],
    binaries=pyspark_binaries,
    datas=pyspark_data,
    hiddenimports=pyspark_hiddenimports,
)
pyz = PYZ(analysis.pure)
exe = EXE(
    pyz, analysis.scripts, analysis.binaries, analysis.datas, [],
    name="dataqualy", console=False, icon=None,
)


# @hugaojanuario
