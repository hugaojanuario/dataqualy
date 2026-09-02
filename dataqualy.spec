from PyInstaller.utils.hooks import collect_all


pyspark_data, pyspark_binaries, pyspark_hiddenimports = collect_all("pyspark")

analysis = Analysis(
    ["src/dataqualy/gui_main.py"],
    pathex=["src"],
    binaries=pyspark_binaries,
    datas=pyspark_data,
    hiddenimports=pyspark_hiddenimports,
    excludes=["pandas", "pyarrow", "pyspark.sql.connect", "pyspark.pandas"],
)
pyz = PYZ(analysis.pure)
exe = EXE(
    pyz, analysis.scripts, analysis.binaries, analysis.datas, [],
    name="dataqualy", console=False, icon=None,
)


# @hugaojanuario
