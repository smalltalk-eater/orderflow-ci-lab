from orderflow.inventory import Warehouse, allocate_order, release_order


def test_duplicate_sku_exceeds_stock():
    warehouse = Warehouse({"A": 5})

    result = allocate_order(
        warehouse,
        "ORD-1",
        [
            {"sku": "A", "quantity": 3},
            {"sku": "A", "quantity": 3},
        ],
    )

    assert result is False
    assert warehouse.available["A"] == 5
    assert warehouse.reserved == {}


def test_repeated_reservation():
    warehouse = Warehouse({"A": 5})

    assert allocate_order(
        warehouse,
        "ORD-1",
        [{"sku": "A", "quantity": 2}],
    )

    result = allocate_order(
        warehouse,
        "ORD-1",
        [{"sku": "A", "quantity": 1}],
    )

    assert result is False
    assert warehouse.available["A"] == 3

    release_order(warehouse, "ORD-1")
    assert warehouse.available["A"] == 5