import unittest
import numpy as np
import pandas as pd
from datetime import date
from datetime import datetime
from pandas_import import join_df
from pandas_import import round_df
from pandas_import import set_time_index
from pandas_import import rename_columns
from pandas_import import group_df


class TestTimeSeries(unittest.TestCase):

    def _test_join(self):
        left_df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6],
                                        [7, 8, 9]]),
                               columns=["a", "b", "c"])

        right_df = pd.DataFrame(np.array([["a", "b", "c"], ["d", "e", "f"],
                                         [None, None, None]]),
                                columns=[1, 2, 3])

        joined = pd.DataFrame(np.array([[1, 2, 3, "a", "b", "c"],
                                        [4, 5, 6, "d", "e", "f"],
                                        [7, 8, 9, 0, 0, 0]]),
                              columns=["a", "b", "c", 1, 2, 3])

        pd.testing.assert_frame_equal(join_df(left_df, right_df), joined)

    def test_round(self):
        df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                          columns=["a", "b", "c"],
                          index=[datetime(2019, 1, 1, 16, 30),
                                 datetime(2019, 1, 2, 16, 32),
                                 datetime(2019, 1, 3, 16, 34)])

        trans = pd.DataFrame(np.array([[1, 2], [4, 5], [7, 8]]),
                             columns=["a", "b"],
                             index=[datetime(2019, 1, 1, 16, 30),
                                    datetime(2019, 1, 2, 16, 30),
                                    datetime(2019, 1, 3, 16, 35)])

        pd.testing.assert_frame_equal(round_df(df, "5min", ["a", "b"]),
                                      trans)

    def _test_set_time(self):
        df = pd.DataFrame(np.array([[1, "1/1/19"],
                                   [2, "1/2/19"],
                                   [3, "1/3/19"]]),
                          columns=["value", "time"])

        trans = pd.DataFrame(np.array([[1], [2], [3]]),
                             columns=["value"],
                             index=[date(2019, 1, 1),
                                    date(2019, 1, 2),
                                    date(2019, 1, 3)])

        pd.testing.assert_frame_equal(set_time_index(df, "time"), trans)

    def test_rename_cols(self):
        df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                          columns=["a", "b", "c"])
        file = "test/test_.csv"
        trans = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                             columns=["test", "b", "c"])
        pd.testing.assert_frame_equal(rename_columns(df, file, "a"), trans)

    def test_group(self):
        df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                          columns=["a", "b", "c"], index=[1, 1, 2])

        group = pd.DataFrame(np.array([[5, 7, 4.5], [7, 8, 9]]),
                             columns=["a", "b", "c"], index=[1, 2])

        pd.testing.assert_frame_equal(group_df(df, ["a", "b"], ["c"]),
                                      group, check_dtype=False)


if __name__ == '__main__':
    unittest.main()
