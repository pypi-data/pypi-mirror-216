from typing import Tuple, Dict, List, Any
import gc

from skopt import Optimizer
from skopt.space import Real, Categorical, Integer
from skopt.utils import use_named_args

from gpforecaster.model.gpf import GPF
from gpforecaster.utils.logger import Logger
from gpforecaster import __version__


def single_trial(
    dataset_name: str,
    hierarchical_data: Dict[str, List],
    hyperparameters: Dict[str, Any],
    gp_type: str,
    device: str,
    logger_tuning: Logger,
) -> Tuple[float, Dict[str, Any]]:
    """
    Train a single GPF model with the given hyperparameters.

    Args:
        dataset_name (str): The name of the dataset.
        hierarchical_data (Dict[str, List]): The hierarchical data for the model.
        hyperparameters (Dict[str, Any]): The hyperparameters to use for the model.
        gp_type (str): The type of Gaussian Process model to use (e.g., "exact").

    Yields:
        Tuple[float, Dict[str, Any]]: A tuple containing the validation loss and the hyperparameters used.
    """
    gpf = GPF(
        dataset=dataset_name,
        groups=hierarchical_data,
        gp_type=gp_type,
        device=device
    )
    model, like = gpf.train(
        lr=hyperparameters["learning_rates"],
        weight_decay=hyperparameters["weight_decays"],
        scheduler_type=hyperparameters["scheduler_types"],
        gamma_rate=hyperparameters["gamma_rates"],
        patience=hyperparameters["patiences"],
    )
    val_loss = gpf.val_losses[-1]

    log_and_print_best_hyperparameters(
        gp_type, dataset_name, hyperparameters, val_loss, logger_tuning
    )

    del model
    del gpf
    del like
    gc.collect()

    return (val_loss, hyperparameters)


def optimize_hyperparameters_bayesian(
    dataset_name: str,
    hierarchical_data: Dict[str, List],
    num_trials: int,
    gp_type: str = "exact",
    device="cpu",
) -> Dict[str, Any]:
    """
    Optimize hyperparameters using Bayesian search.

    Args:
        dataset_name (str): The name of the dataset.
        hierarchical_data (Dict[str, List]): The hierarchical data for the model.
        num_trials (int): The number of trials to perform.
        gp_type (str): The type of Gaussian Process model to use (e.g., "exact").

    Returns:
        Dict[str, Any]: The best set of hyperparameters found during optimization.
    """
    logger_tuning = Logger(
        "hyperparameter_tuning", dataset=f"{dataset_name}_hypertuning", to_file=True
    )

    # Define the search space for hyperparameters
    search_space = [
        Real(1e-3, 1e-2, name="learning_rates"),
        Real(1e-5, 1e-3, name="weight_decays"),
        Categorical(["step", "exponential", "cosine", "none"], name="scheduler_types"),
        Real(0.1, 0.95, name="gamma_rates"),
        Integer(3, 12, name="patiences"),
    ]

    optimizer = Optimizer(search_space)

    @use_named_args(search_space)
    def wrapped_single_trial(**hyperparameters):
        val_loss, _ = single_trial(
            dataset_name,
            hierarchical_data,
            hyperparameters,
            gp_type,
            device,
            logger_tuning,
        )
        return val_loss

    results = optimizer.run(wrapped_single_trial, num_trials)
    best_hyperparameters = {k.name: v for k, v in zip(search_space, results.x)}

    log_and_print_best_hyperparameters(
        gp_type,
        dataset_name,
        best_hyperparameters,
        results.fun,
        logger_tuning,
        best="BEST",
    )
    return best_hyperparameters


def log_and_print_best_hyperparameters(
    gp_type: str,
    dataset_name: str,
    best_hyperparameters: Dict[str, Any],
    best_val_loss: float,
    logger_tuning: Logger,
    best="",
):
    """
    Log and print the best hyperparameters and validation loss.

    Args:
        gp_type (str): The type of Gaussian Process model used (e.g., "exact").
        dataset_name (str): The name of the dataset.
        best_hyperparameters (Dict[str, Any]): The best set of hyperparameters found.
        best_val_loss (float): The best validation loss.
    """

    logger_tuning.info(
        f"\n{best} -> "
        f"Algorithm: gpf_{gp_type}, "
        f"Version: {__version__}, "
        f"Dataset: {dataset_name}, "
        f"{best} hyperparameters: {best_hyperparameters}, "
        f"Validation loss: {best_val_loss}\n"
    )

    print(
        f"\n{best} -> "
        f"Algorithm: gpf_{gp_type}, \n"
        f"Version: {__version__}, \n"
        f"Dataset: {dataset_name}, \n"
        f"{best} hyperparameters: {best_hyperparameters}, \n"
        f"Validation loss: {best_val_loss}\n"
    )
