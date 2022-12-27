import unittest
from unittest import IsolatedAsyncioTestCase
from model import Model


class MyTestCase(IsolatedAsyncioTestCase):
    async def test_get_score(self):
        model = Model('../resource/model8.pth', '../resource/init_data_path.data', '../resource/prognostics.pth')
        list1 = [0.001 for _ in range(0, 3 * 128)]
        list2 = [0.002 for _ in range(0, 3 * 128)]
        list3 = [0.003 for _ in range(0, 3 * 128)]

        score, time = await model.get_model_res(list1, list2, list3)

        print(score, time)


if __name__ == '__main__':
    unittest.main()
