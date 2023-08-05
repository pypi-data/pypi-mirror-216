import albylib.machine_learning.sklearn as albylib_sklearn


def test_feature_selector():
    columns = ["a", "b", "c"]
    fs = albylib_sklearn.FeatureSelector(columns)

    assert fs.columns == columns


