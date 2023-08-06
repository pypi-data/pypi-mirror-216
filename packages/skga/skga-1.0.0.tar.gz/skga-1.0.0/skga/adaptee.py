import copy
import random
from datetime import datetime

import numpy as np
from sklearn import clone
from sklearn.base import is_classifier
from sklearn.metrics import check_scoring
from sklearn.metrics._scorer import _check_multimetric_scoring
from sklearn.model_selection import check_cv
from sklearn.model_selection._search import BaseSearchCV, ParameterGrid
from sklearn.model_selection._validation import cross_val_score
from sklearn.utils import indexable
from sklearn.utils.validation import _check_fit_params

from .hbrkga import BrkgaMpIpr, Sense, BaseChromosome, load_configuration_from_dict, BayesianOptimizerElites

class Decoder:

    def __init__(self, parameters, estimator, X, y, cv):
        self._parameters = parameters
        self._estimator = estimator
        self._X = X
        self._y = y
        self._limits = [self._parameters[l] for l in list(self._parameters.keys())]
        self._cv = cv

    def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float:
        return self.score(self.encoder(chromosome))

    def encoder(self, chromosome: BaseChromosome) -> dict:
        chr_size = len(chromosome)
        hyperparameters = copy.deepcopy(self._parameters)

        for geneIdx in range(chr_size):
            gene = chromosome[geneIdx]
            key = list(self._parameters.keys())[geneIdx]
            limits = self._parameters[key]  # evita for's aninhados
            if type(limits) is np.ndarray:
                limits = limits.tolist()

            if type(limits[0]) is str:
                hyperparameters[key] = limits[round(gene * (len(limits) - 1))]
            elif type(limits[0]) is int and len(limits) > 2:
                hyperparameters[key] = int(limits[round(gene * (len(limits) - 1))])
            elif type(limits[0]) is bool:
                hyperparameters[key] = 1 if limits[0] else 0
            else:
                hyperparameters[key] = (gene * (limits[1] - limits[0])) + limits[0]

        return hyperparameters

    def score(self, hyperparameters: dict) -> float:
        estimator_clone = clone(self._estimator)
        estimator_clone.set_params(**hyperparameters)

        try:
            estimator_clone.fit(self._X, self._y)
        except ValueError:
            return 0.0

        # Adicionar o parâmetro scoring para que siga fielmente o SKLearn
        return cross_val_score(estimator_clone, self._X, self._y, cv=self._cv).mean()


class HyperBRKGASearchCV(BaseSearchCV):

    def __init__(
            self,
            estimator,
            brkga_params=None,
            exploit_method=None,
            *,
            scoring=None,
            n_jobs=None,
            refit=True,
            cv=None,
            verbose=0,
            pre_dispatch="2*n_jobs",
            error_score=np.nan,
            return_train_score=True,
            parameters,
            data,
            target
    ):
        super().__init__(
            estimator=estimator,
            scoring=scoring,
            n_jobs=n_jobs,
            refit=refit,
            cv=cv,
            verbose=verbose,
            pre_dispatch=pre_dispatch,
            error_score=error_score,
            return_train_score=return_train_score,
        )
        if brkga_params is not None:
            self.brkga_config, _ = brkga_params
        else:
            self.brkga_config , _ = load_configuration_from_dict({
                'population_size': 10,
                'elite_percentage': 0.3,
                'mutants_percentage': 0.3,
                'num_elite_parents': 1,
                'total_parents': 2,
                'bias_type': 'LOGINVERSE',
                'num_independent_populations': 1,
                'pr_number_pairs': 0,
                'pr_minimum_distance': 0.15,
                'pr_type': 'PERMUTATION',
                'pr_selection': 'BESTSOLUTION',
                'alpha_block_size': 1.0,
                'pr_percentage': 1.0,
                'exchange_interval': 0,
                'num_exchange_indivuduals': 0,
                'reset_interval': 0
            })
        self._parameters = parameters

        self.decoder = Decoder(self._parameters, estimator, data, target, cv)
        elite_number = int(self.brkga_config.elite_percentage * self.brkga_config.population_size)

        if exploit_method is not None:
            self.em = exploit_method(self.decoder, percentage=0.6, eliteNumber=elite_number)
        else:
            self.em = BayesianOptimizerElites(decoder=self.decoder, e=0.3, steps=3, percentage=0.6,
                                              eliteNumber=elite_number)

        chromosome_size = len(self._parameters)
        self.brkga = BrkgaMpIpr(
            decoder=self.decoder,
            sense=Sense.MAXIMIZE,
            seed=random.randint(-10000, 10000),
            chromosome_size=chromosome_size,
            params=self.brkga_config,
            diversity_control_on=True,
            n_close=3,
            exploitation_method=self.em
        )

        self.brkga.initialize()

    def fit(self, X, y=None, *, groups=None, **fit_params):
        estimator = self.estimator

        if callable(self.scoring):
            scorers = self.scoring
        elif self.scoring is None or isinstance(self.scoring, str):
            scorers = check_scoring(self.estimator, self.scoring)
        else:
            scorers = _check_multimetric_scoring(self.estimator, self.scoring)
            self._check_refit_for_multimetric(scorers)

        X, y, groups = indexable(X, y, groups)
        fit_params = _check_fit_params(X, fit_params)

        cv_orig = check_cv(self.cv, y, classifier=is_classifier(estimator))
        n_splits = cv_orig.get_n_splits(X, y, groups)

        def evaluate_candidates(candidate_params, cv=None, more_results=None):
            start = datetime.now()
            candidate_params = list(candidate_params)
            all_candidate_params = []

            for i in range(1, 11):
                print("\n###############################################")
                print(f"Generation {i}")
                print("")
                self.brkga.evolve()

                for pop_idx in range(len(self.brkga._current_populations)):
                    pop_diversity_score = self.brkga.calculate_population_diversity(pop_idx)
                    if self.verbose > 2:
                        print(f"Population {pop_idx}:")
                        print(f"Population diversity score = {pop_diversity_score}")
                        print("")
                        print("Chromosomes = ")
                        for chromo_idx in range(len(self.brkga._current_populations[pop_idx].chromosomes)):
                            print(f"{chromo_idx} -> {self.brkga._current_populations[pop_idx].chromosomes[chromo_idx]}")
                        print("")
                        print("Fitness = ")
                        for fitness in self.brkga._current_populations[pop_idx].fitness:
                            print(fitness)
                        print("------------------------------")

                best_cost = self.brkga.get_best_fitness()
                best_chr = self.brkga.get_best_chromosome()
                if self.verbose > 2:
                    print(f"{datetime.now()} - Best score so far: {best_cost}")
                    print(f"{datetime.now()} - Best chromosome so far: {best_chr}")
                    print(f"{datetime.now()} - Total time so far: {datetime.now() - start}", flush=True)

            best_cost = self.brkga.get_best_fitness()
            best_chr = self.brkga.get_best_chromosome()
            if self.verbose > 2:
                print("\n###############################################")
                print("Final results:")
                print(f"{datetime.now()} - Best score: {best_cost}")
                print(f"{datetime.now()} - Best chromosome: {best_chr}")
                print(f"Total time = {datetime.now() - start}")

            all_candidate_params.extend(candidate_params)
            self.results = {
                "best_chromosome": best_chr,
                "best_param_decoded": self.decoder.encoder(best_chr),
                "best_param_score": best_cost,
                "total_time": (datetime.now() - start).total_seconds(),
            }

        self._run_search(evaluate_candidates)

        # Store the only scorer not as a dict for single metric evaluation
        self.scorer_ = scorers

        self.cv_results_ = self.results
        self.n_splits_ = n_splits

        return self

    def _run_search(self, evaluate_candidates):
        evaluate_candidates(ParameterGrid(self._parameters))
