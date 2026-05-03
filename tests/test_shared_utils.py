"""
test_shared_utils.py - Unit tests for shared utility functions.

These are pure unit tests — they do not require a database or HTTP client.
Covers: paginate(), generate_random_string(), get_current_utc_time()
"""
import pytest
from datetime import timezone
from app.shared.utils import paginate, generate_random_string, get_current_utc_time


class TestPaginate:
    def test_returns_correct_structure(self):
        """paginate() must always return data and meta keys."""
        result = paginate(items=["a", "b"], page=1, size=2, total=10)
        assert "data" in result
        assert "meta" in result

    def test_data_contains_items(self):
        """data key must be exactly the items passed in."""
        items = [{"id": 1}, {"id": 2}]
        result = paginate(items=items, page=1, size=2, total=10)
        assert result["data"] == items

    def test_has_next_true(self):
        """has_next is True when there are more pages."""
        result = paginate(items=[], page=1, size=10, total=25)
        assert result["meta"]["has_next"] is True

    def test_has_next_false(self):
        """has_next is False on the last page."""
        result = paginate(items=[], page=3, size=10, total=25)
        assert result["meta"]["has_next"] is False

    def test_has_previous_false_on_first_page(self):
        """has_previous is False on page 1."""
        result = paginate(items=[], page=1, size=10, total=50)
        assert result["meta"]["has_previous"] is False

    def test_has_previous_true_on_later_pages(self):
        """has_previous is True on page 2 and beyond."""
        result = paginate(items=[], page=2, size=10, total=50)
        assert result["meta"]["has_previous"] is True

    def test_meta_values_match_inputs(self):
        """Meta fields correctly reflect the inputs."""
        result = paginate(items=[], page=3, size=15, total=100)
        assert result["meta"]["page"] == 3
        assert result["meta"]["size"] == 15
        assert result["meta"]["total"] == 100


class TestGenerateRandomString:
    def test_default_length(self):
        """Default output is 10 characters."""
        result = generate_random_string()
        assert len(result) == 10

    def test_custom_length(self):
        """Custom length is respected exactly."""
        assert len(generate_random_string(24)) == 24
        assert len(generate_random_string(1)) == 1

    def test_alphanumeric_only(self):
        """Output contains only alphanumeric characters."""
        result = generate_random_string(100)
        assert result.isalnum()

    def test_unique_outputs(self):
        """Two calls should produce different strings (probabilistically)."""
        a = generate_random_string(20)
        b = generate_random_string(20)
        assert a != b


class TestGetCurrentUtcTime:
    def test_returns_datetime(self):
        """get_current_utc_time() returns a datetime object."""
        from datetime import datetime
        result = get_current_utc_time()
        assert isinstance(result, datetime)

    def test_is_utc_timezone_aware(self):
        """Returned datetime must be timezone-aware and in UTC."""
        result = get_current_utc_time()
        assert result.tzinfo is not None
        assert result.tzinfo == timezone.utc
