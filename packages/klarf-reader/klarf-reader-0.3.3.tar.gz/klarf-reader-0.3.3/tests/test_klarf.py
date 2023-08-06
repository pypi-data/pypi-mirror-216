# MODULES
from dataclasses import asdict
from pathlib import Path

# UNITTEST
import unittest

# KLARF_READER
from klarf_reader.klarf import Klarf
from klarf_reader.utils import klarf_convert

# TESTS
from tests.utils import *


ASSETS_PATH: Path = Path(__file__).parent / "assets"
ASSETS_SAVED_PATH: Path = ASSETS_PATH / "saved"


class TestKlarf(unittest.TestCase):
    def setUp(self) -> None:
        self.path_klarf_single_wafer = ASSETS_PATH / "J052SBN_8196_J052SBN-01.000"
        self.path_klarf_multi_wafers = ASSETS_PATH / "J237DTA_3236.000"

    def assertListOfDictEqual(self, first: list[dict], second: list[dict]):
        self.assertEqual(len(first), len(second))
        for index, item in enumerate(first):
            if isinstance(item, dict):
                self.assertNestedDictEqual(item, second[index])
            else:
                self.assertEqual(item, second[index])

    def assertNestedDictEqual(self, first: dict, second: dict):
        self.assertEqual(len(first), len(second))

        first = {key: first[key] for key in sorted(first.keys())}
        second = {key: second[key] for key in sorted(second.keys())}

        for key, value in first.items():
            second_value = second.get(key)
            if isinstance(value, (list, tuple)):
                self.assertListOfDictEqual(value, second_value)
            elif isinstance(value, dict):
                self.assertNestedDictEqual(value, second_value)
            else:
                self.assertEqual(value, second_value)

    @load_expected_data(saved_path=ASSETS_SAVED_PATH)
    def test_klarf_single_wafer(self, expected_data, saved_path) -> None:
        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_single_wafer)
        content_dict = asdict(content)

        save_as_json(
            saved_path,
            dict=content_dict,
        )

        # Then
        self.assertNestedDictEqual(content_dict, expected_data)

    @load_expected_data(saved_path=ASSETS_SAVED_PATH)
    def test_klarf_single_wafer_with_custom_attributes(
        self, expected_data, saved_path
    ) -> None:
        # Given
        custom_columns_lot = ["TOTO"]
        custom_columns_defects = ["DEFECTAREA"]

        # When
        content = Klarf.load_from_file(
            filepath=self.path_klarf_single_wafer,
            custom_columns_wafer=custom_columns_lot,
            custom_columns_defect=custom_columns_defects,
        )
        content_dict = asdict(content)

        save_as_json(
            saved_path,
            dict=content_dict,
        )

        # Then
        self.assertNestedDictEqual(content_dict, expected_data)

    def test_klarf_single_wafer_with_raw_content(self) -> None:
        # Given
        expected_raw_content_length = 13356

        # When
        _, raw_content = Klarf.load_from_file_with_raw_content(
            filepath=self.path_klarf_single_wafer
        )

        # Then
        self.assertEqual(len(raw_content), expected_raw_content_length)

    @load_expected_data(saved_path=ASSETS_SAVED_PATH)
    def test_klarf_multi_wafers(self, expected_data, saved_path) -> None:
        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_multi_wafers)
        content_dict = asdict(content)

        save_as_json(
            saved_path,
            dict=content_dict,
        )

        # Then
        self.assertNestedDictEqual(content_dict, expected_data)

    @load_expected_data(saved_path=ASSETS_SAVED_PATH)
    def test_convert_single_klarf_content(self, expected_data, saved_path) -> None:
        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_multi_wafers)
        single_klarf_content = klarf_convert.convert_to_single_klarf_content(
            klarf_content=content, wafer_index=0
        )
        single_klarf_content_dict = asdict(single_klarf_content)

        save_as_json(
            saved_path,
            dict=single_klarf_content_dict,
        )

        # Then
        self.assertNestedDictEqual(single_klarf_content_dict, expected_data)
