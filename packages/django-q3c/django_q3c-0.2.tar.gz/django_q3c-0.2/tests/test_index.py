import pytest

from q3c_test.models import Position


@pytest.mark.django_db
def test_index_creation():
    # Position has an index, it should save to the database correctly
    position = Position(ra=35, dec=23)
    position.save()
