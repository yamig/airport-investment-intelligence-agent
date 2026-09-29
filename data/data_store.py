import uuid


_DATASETS = {}


def save_dataset(data: list[dict]) -> str:
    dataset_id = str(uuid.uuid4())

    _DATASETS[dataset_id] = data

    return dataset_id


def get_dataset(dataset_id: str) -> list[dict]:
    if dataset_id not in _DATASETS:
        raise ValueError(
            f"Unknown dataset_id: {dataset_id}"
        )

    return _DATASETS[dataset_id]