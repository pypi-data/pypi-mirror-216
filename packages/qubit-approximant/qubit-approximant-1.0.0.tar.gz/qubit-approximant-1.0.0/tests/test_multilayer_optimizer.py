import pytest

import numpy as np

from qubit_approximant.core import Circuit, CircuitRxRyRz, Cost
from qubit_approximant.core.optimizer import (
    BlackBoxOptimizer,
    IncrementalOptimizer,
    NonIncrementalOptimizer,
)

rng = np.random.default_rng()

x = np.linspace(-2, 2, 100)
fn = np.exp(-((x) ** 2) / (2 * 0.5**2)) / (0.5 * np.sqrt(2 * np.pi))
min_layer = 6
max_layer = 8
np.random.seed(20)

optimizer = BlackBoxOptimizer(method="L-BFGS-B")


@pytest.mark.parametrize(
    ("circuit", "metric", "params", "new_layer_position", "tol"),
    (
        (CircuitRxRyRz(x, "prob"), "mse", rng.standard_normal(4 * min_layer), "initial", 1e-4),
        (CircuitRxRyRz(x, "prob"), "mse", rng.standard_normal(4 * min_layer), "final", 1e-4),
        (CircuitRxRyRz(x, "prob"), "mse", rng.standard_normal(4 * min_layer), "middle", 1e-4),
        (CircuitRxRyRz(x, "prob"), "mse", rng.standard_normal(4 * min_layer), "random", 1e-4),
    ),
)
def test_incremental_optimizer(
    circuit: Circuit, metric: str, params: np.ndarray, new_layer_position: str, tol: float
) -> None:
    cost = Cost(fn, circuit, metric=metric)
    multilayer_opt = IncrementalOptimizer(min_layer, max_layer, optimizer, 0.3, new_layer_position)
    params_list = multilayer_opt(cost, cost.grad, params)
    for i, params in enumerate(params_list):
        assert cost(params) < tol, f"Error in layer {i} with cost = {cost(params)}"

    if new_layer_position == "initial" or new_layer_position == "final":
        mean_diff, std_diff = multilayer_opt.inital_params_diff


@pytest.mark.parametrize(
    ("circuit", "metric", "params", "tol"),
    (
        (CircuitRxRyRz(x, "prob"), "mse", rng.standard_normal(4 * min_layer), 1e-4),
        (CircuitRxRyRz(x, "prob"), "rmse", rng.standard_normal(4 * min_layer), 5e-3),
    ),
)
def test_nonincremental_optimizer(
    circuit: Circuit, metric: str, params: np.ndarray, tol: float
) -> None:
    cost = Cost(fn, circuit, metric=metric)
    min_layer = 6
    max_layer = 8
    multilayer_opt = NonIncrementalOptimizer(min_layer, max_layer, optimizer, 0.3)
    params_list = multilayer_opt(cost, cost.grad, params)
    for i, params in enumerate(params_list):
        assert cost(params) < tol, f"Error in layer {i} with cost = {cost(params)}"
