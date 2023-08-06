import os

from random import randint
from astar_heuristics import *
from time import time

from evaluate_astar_heuristic import get_heuristic_score
import pickle


class GeneticAlgorithm:

    def __init__(self, heuristics, ranges, model_files):
        self.heuristics = heuristics
        self.pop_size = 0
        self.ranges = ranges
        self.population = None
        self.is_elite = None
        self.scores = None, None
        self.generation_count = 0
        self.best_individual = None
        self.best_score = 0
        self.model_files = model_files

    def create_population(self):
        pop = np.array([
            np.concatenate(
                [np.random.uniform(low=r[0], high=r[1], size=1)
                 for r in self.ranges]
            ) for _ in range(self.pop_size)
        ])
        return pop, np.zeros(pop.shape[0])

    def save_state(self, save_file):
        pickle.dump(self.__dict__, open(save_file, "wb"))

    def load_state(self, save_file):
        self.__dict__ = pickle.load(open(save_file, "rb"))

    def crossover(self, i1, i2, pc):
        if random() > pc:
            return np.copy(i1), np.copy(i2)
        start, end = np.random.choice(len(i1) - 1, size=2, replace=False)
        start, end = (end, start) if start > end else (start, end)
        c1 = np.concatenate((i1[:start], i2[start: end], i1[end:]))
        c2 = np.concatenate((i2[:start], i1[start: end], i2[end:]))
        return np.array([c1, c2])

    def point_mutation(self, individual, pm):
        if random() > pm:
            return np.copy(individual)
        rand_idx = randint(0, len(individual) - 1)
        individual[rand_idx] = np.random.uniform(
            low=self.ranges[rand_idx][0], high=self.ranges[rand_idx][1], size=1)[0]
        return individual

    def get_score(self, idx, questions, max_timeout):
        print(".", end="")
        if self.is_elite[idx]:
            return self.scores[idx]
        gh = GeneHeuristic(
            self.heuristics,
            self.population[idx],
            self.model_files)
        return get_heuristic_score(gh.gene_meta_dist, questions, max_timeout)

    def update_scores(self, questions, max_timeout):
        self.scores = np.array([self.get_score(i, questions, max_timeout)
                               for i in range(len(self.population))])
        best_idx = np.argmax(self.scores)
        if self.scores[best_idx] > self.best_score:
            self.best_individual, self.best_score = self.population[best_idx], self.scores[best_idx]

    def tournament_selection(self, k=3):
        idxs = np.random.choice(self.pop_size, k, replace=False)
        pick = max(idxs, key=lambda i: self.scores[i])
        return pick

    def run_generation(self, questions, elitism, pc, pm, max_timeout):
        parent_idxs = [self.tournament_selection()
                       for _ in range(self.pop_size)]
        parents, parent_scores = self.population[parent_idxs], self.scores[parent_idxs]
        children = []

        for i in range(len(parents) - 1):
            for c in self.crossover(parents[i], parents[i + 1], pc):
                mc = self.point_mutation(c, pm)
                children.append(mc)

        if elitism > 0:
            sorted_order = np.argsort(self.scores)[::-1]
            sorted_pop, sorted_scores = self.population[sorted_order], self.scores[sorted_order]
            elite = sorted_pop[:elitism]
        else:
            elite = []
            sorted_scores = []

        self.population = np.concatenate(
            (np.copy(elite[:elitism]), children[:self.pop_size - elitism]))
        # first few not reevaluated
        self.scores = np.concatenate(
            (sorted_scores[:elitism], self.scores[elitism:]))
        self.update_scores(questions, max_timeout)

    def train(self, population_size, questions, num_generations=10, elitism=1, pc=0.8, pm=0.2, max_timeout=1,
              save_file=None):
        begin_time = time()

        if save_file is not None:
            start = time()
            self.load_state(save_file)
            end = time()
            print(f"\nPrevious State | {end-start:.4f} seconds | "
                  f"\tAvg Score: {np.mean(self.scores)}\tBest Score: {self.best_score}")
            print(f"Scores: {self.scores}")
            print(f"Best Weights: {self.best_individual}\n")
        elif self.population is None:
            start = time()
            self.pop_size = population_size
            self.population, self.scores = self.create_population()
            self.is_elite = [False] * self.pop_size
            self.update_scores(questions, max_timeout)
            end = time()
            print(f"\nBaseline | {end-start:.4f} seconds | "
                  f"\tAvg Score: {np.mean(self.scores)}\tBest Score: {self.best_score}")
            print(f"Scores: {self.scores}")
            print(f"Best Weights: {self.best_individual}\n")

        self.is_elite = [True] * elitism + [False] * (self.pop_size - elitism)
        for g in range(num_generations):
            start = time()
            self.run_generation(questions, elitism, pc, pm, max_timeout)
            end = time()
            print(f"\nGeneration {g+1}/{num_generations} | {end-start:.4f} seconds | "
                  f"\tAvg Score: {np.mean(self.scores)}\tBest Score: {self.best_score}")
            print(f"Scores: {self.scores}")
            print(f"Best Weights: {self.best_individual}\n")

        end_time = time()
        print(f"Total running time: {end_time-begin_time:.4f} seconds.")

        gh = GeneHeuristic(
            self.heuristics,
            self.best_individual,
            self.model_files)
        gh.set_params({
            "pop_size": self.pop_size, "questions": len(questions), "generations": num_generations, "elitism": elitism,
            "pc": pc, "pm": pm, "max_timeout": max_timeout
        })
        return gh


def base_ga_train():
    # neh_1 = NeuralEmbeddingHeuristic(os.path.join("models", "sol_dist_model_parameters.pt"))
    # neh_2 = NeuralEmbeddingHeuristic(os.path.join("models", "sol_dist_biased_model_2_parameters.pt"))
    heuristics = [
        levenshtein_distance,
        unitary_distance,
        len_distance,
        variable_mismatch] + RuleDists().all_dists  # + [neh_1.embedding_dist, neh_2.embedding_dist]
    # + [(0, 1)] * 2  # [(-10, 10)] * (len(heuristics)-6)
    ranges = [(0, 10)] * 16
    with open("../questions.json", "r") as qf:
        questions = json.load(qf)['questions']
    model_files = [os.path.join("models", "sol_dist_model_parameters.pt"),
                   os.path.join(
        "models", "sol_dist_biased_model_2_parameters.pt"),
        None, None]
    ga = GeneticAlgorithm(heuristics, ranges, model_files)
    gh = ga.train(
        population_size=5, questions=questions[:5], num_generations=3,
        max_timeout=3, elitism=1, pm=0.2, pc=0.8,
        # os.path.join("heuristics_and_results", "genetic_states", "genetic_embedded.json")
        save_file=None
    )
    print(get_heuristic_score(gh.gene_meta_dist, questions, max_timeout=1))
    # ga.save_state(os.path.join("heuristics_and_results", "genetic_states", "genetic_embedded_test.json"))
    return gh


if __name__ == "__main__":
    gh = base_ga_train()
    print(gh.weights)
    # gh.save(os.path.join("heuristics_and_results", "genetic_weights", "gene_weights_embedded_test.txt"))
