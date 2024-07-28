import pytest
import softest


@pytest.mark.usefixtures("setup")
class BaseClass(softest.TestCase):

    # example: hard_assert_equal(text, 'new')
    def hard_assert_equal(self, actual_val, expected_val):
        assert actual_val == expected_val, "{0} does not equal {1}".format(actual_val, expected_val)

    # example: hard_assert_is(1, 1)
    def hard_assert_is(self, actual_val, expected_val):
        assert actual_val is expected_val, "{0} is not correct".format(actual_val)

    # example: hard_assert_contains('to do', 'do')
    def hard_assert_contains(self, parent, child):
        assert parent.__contains__(child), "{0} does not contain {1}".format(parent, child)

    # example: hard_assert_in([1, 2, 3], 1)
    def hard_assert_in(self, child, parent):
        assert child in parent, "{0} does not in {1}".format(child, parent)

    def soft_assert_equal(self, actual_val, expected_val):
        self.soft_assert(self.assertEqual, actual_val, expected_val,
                         "{0} does not eqqual {1}".format(actual_val, expected_val))

    def soft_assert_is(self, actual_val, expected_val):
        self.soft_assert(self.assertIs, actual_val, expected_val, "{0} is not correct".format(actual_val))

    def soft_assert_contains(self, parent, child):
        self.soft_assert(self.assertTrue, parent.__contains__(child), "{0} does not contain {1}".format(parent, child))

    def soft_assert_in(self, child, parent):
        self.soft_assert(self.assertIn, child, parent, "{0} does not in {1}".format(child, parent))

    # we need to add this assert after all soft assert to make sure test case run correctly
    def assert_all_after_soft_asserts(self):
        self.assert_all("======= Assert All After Soft Assert ======")
