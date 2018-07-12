import unittest

from src.coords_form import CoordsForm


class TestUserForm(unittest.TestCase):
    form_class = CoordsForm

    def test_form_requires_fields(self):
        form = CoordsForm(
            latitude=None,
            longitude=None,
        )
        self.assertFalse(form.validate())

    def test_form_with_inaccurate_values_does_not_validate(self):
        form = CoordsForm(
            latitude=155.4,
            longitude=245.4,
        )
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()
