from dataqualy.gui_main import requested_pyspark_module


def test_requested_pyspark_module_detects_worker():
    assert (
        requested_pyspark_module(["dataqualy.exe", "-m", "pyspark.worker"])
        == "pyspark.worker"
    )


def test_requested_pyspark_module_ignores_normal_start():
    assert requested_pyspark_module(["dataqualy.exe"]) is None


# @hugaojanuario
