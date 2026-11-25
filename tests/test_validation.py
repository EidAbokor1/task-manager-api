import pytest
from task_manager import create_task


def test_create_task_rejects_spaces_only_title():
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task("   ")