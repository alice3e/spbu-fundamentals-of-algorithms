from abc import ABC, abstractmethod
from typing import Literal, Sequence, Type

import numpy as np
from numpy.typing import DTypeLike, ArrayLike


EvaluationMethod = Literal["standard", "optimal"]


class Evaluator(ABC):
    def __init__(
        self,
        coeffs: ArrayLike,
        dtype: DTypeLike,
        evaluation_method: EvaluationMethod,
    ):
        self.coeffs = coeffs
        self.dtype = dtype
        self.eval_func = None
        self.reset_evaluation_method(evaluation_method)

    def __call__(self, *args):
        return self.eval_func(*args)

    def reset_evaluation_method(self, evaluation_method: EvaluationMethod):
        if evaluation_method == "standard":
            self.eval_func = self._eval_standard
        elif evaluation_method == "optimal":
            self.eval_func = self._eval_optimal
        else:
            raise ValueError(f"Unknown evaluation method: {evaluation_method}")

    @abstractmethod
    def _eval_standard(self, *args): ...

    @abstractmethod
    def _eval_optimal(self, *args): ...


class Polynomial(Evaluator):
    def __init__(
        self,
        coeffs: ArrayLike,
        dtype: DTypeLike,
        evaluation_method: EvaluationMethod,
    ):
        super().__init__(coeffs, dtype, evaluation_method)

    def _eval_standard(self, x):
        res = self.dtype(0.0)
        x = self.dtype(x)

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        return res

    def _eval_optimal(self, x):
        res = self.dtype(0.0)
        x = self.dtype(x)

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        return res


class QuadraticEquationRoots(Evaluator):
    def __init__(
        self,
        coeffs: ArrayLike,
        dtype: DTypeLike,
        evaluation_method: EvaluationMethod,
    ):
        super().__init__(coeffs, dtype, evaluation_method)

    def _eval_standard(self):
        a = self.coeffs[2]
        b = self.coeffs[1]
        c = self.coeffs[0]
        root_of_d = np.sqrt(
            np.power(b, 2, dtype=self.dtype) - self.dtype(4.0) * a * c, dtype=self.dtype
        )
        x1 = (-b + root_of_d) / (self.dtype(2.0) * a)
        x2 = (-b - root_of_d) / (self.dtype(2.0) * a)
        return x1, x2

    def _eval_optimal(self):
        a = self.coeffs[2]
        b = self.coeffs[1]
        c = self.coeffs[0]
        root_of_d = np.sqrt(
            np.power(b, 2, dtype=self.dtype) - self.dtype(4.0) * a * c, dtype=self.dtype
        )
        x1 = -(self.dtype(2.0) * c) / (b + root_of_d)
        x2 = -(self.dtype(2.0) * c) / (b - root_of_d)
        return x1, x2


def _get_value(f, x):
    return f() if x is None else f(x)


def _print_relative_error(eval_by_precision: dict[int, Evaluator], val_exact, x=None):
    for n_bits in (16, 32):
        val_appr = _get_value(eval_by_precision[n_bits], x)
        if isinstance(val_appr, Sequence):
            for i in range(len(val_appr)):
                rel_err = np.abs((val_exact[i] - val_appr[i]) / val_exact[i])
                print(
                    f"Float{n_bits} value #{i+1}: {val_appr[i]:.5f}. "
                    f"Relative error: {rel_err:.2e}"
                )
        else:
            rel_err = np.abs((val_exact - val_appr) / val_exact)
            print(
                f"Float{n_bits} value: {val_appr:.5f}. "
                f"Relative error: {rel_err:.2e}"
            )


def run_different_precision_levels(
    original_coeffs: ArrayLike, evaluator: Type[Evaluator], x=None
):
    dtypes = (np.float16, np.float32, np.float64)
    eval_by_precision = {
        n_bits: evaluator(coeffs=coeffs, dtype=dtype, evaluation_method="standard")
        for n_bits, coeffs, dtype in zip(
            [16, 32, 64],
            (np.array(original_coeffs, dtype=dtype) for dtype in dtypes),
            dtypes,
        )
    }

    val_exact = _get_value(eval_by_precision[64], x)

    print("Relative errors for standard evaluation")
    _print_relative_error(eval_by_precision, val_exact, x)

    print("Relative errors for optimal evaluation")
    for eval in eval_by_precision.values():
        eval.reset_evaluation_method("optimal")

    _print_relative_error(eval_by_precision, val_exact, x)


if __name__ == "__main__":
    # Comparison of two different ways to compute quadratic equation roots
    original_coeffs = [1.0, 62.1, 1.0]

    print("Quadratic equation roots")
    run_different_precision_levels(original_coeffs, QuadraticEquationRoots)

    # Horner's method for polynomial evaluation
    original_coeffs = [1.5, 10.2, -10.1, 1.0]
    x = 4.71

    print("\nHorner's method")
    run_different_precision_levels(original_coeffs, Polynomial, x)
