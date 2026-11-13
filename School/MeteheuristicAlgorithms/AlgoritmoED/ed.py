"""Evolución Diferencial clásica con tablas compactas en consola."""
import random
import time
import statistics


#==================== DATOS PERSONALES ====================
# Eric Oswaldo Aguilar Nova
# Algoritmos Metaheurísticos
# 12/11/2026
# Algoritmo ED: Evolución Diferencial
# Gabriel Contreras Garcia


# =============== HIPERPARÁMETROS EDITABLES ===============
populationSize = 15       # Número de individuos
maxGenerations = 100      # Máximo de generaciones
mutationFactor = 0.4      # Factor diferencial F
crossoverRate = 0.9       # Probabilidad de cruce CR
strategy = "rand_1_bin"   # Estrategia de evolución diferencial
tolerance = 1e-10         # Umbral de convergencia
stagnationLimit = 50      # Generaciones consecutivas sin mejora

# =============== CONFIGURACIÓN GENERAL ===================
bounds = [(-5.0, 5.0), (-5.0, 5.0)]
printInterval = 10


class DifferentialEvolution:
    def __init__(self, fitness_function, bounds, population_size=30,
                 max_generations=150, mutation_factor=0.6, crossover_rate=0.9,
                 strategy="rand_1_bin", tolerance=1e-10, stagnation_limit=50,
                 print_interval=10):
        # Los parámetros controlan la exploración, la recombinación y la parada.
        if not bounds or any(low >= high for low, high in bounds):
            raise ValueError("Los límites deben ser pares (inferior, superior) válidos")
        if strategy not in ("rand_1_bin", "rand_2_bin"):
            raise ValueError("Estrategia no soportada")
        min_population = 4 if strategy == "rand_1_bin" else 6
        if population_size < min_population:
            raise ValueError(f"Se requieren al menos {min_population} individuos")
        if not 0 < mutation_factor <= 2 or not 0 <= crossover_rate <= 1:
            raise ValueError("F debe estar en (0,2] y CR en [0,1]")
        self.fitness_function = fitness_function
        self.bounds = bounds
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_factor = mutation_factor
        self.crossover_rate = crossover_rate
        self.strategy = strategy
        self.tolerance = tolerance
        self.stagnation_limit = stagnation_limit
        self.print_interval = max(1, print_interval)
        self.population = []
        self.history = []
        self.best_individual = None
        self.best_fitness = float("inf")

    def create_individual(self):
        # Inicializa una solución uniformemente dentro de cada dimensión.
        return [random.uniform(low, high) for low, high in self.bounds]

    def _clip(self, individual):
        # Evita soluciones fuera del dominio de búsqueda.
        return [min(high, max(low, value)) for value, (low, high) in zip(individual, self.bounds)]

    def mutate(self, target_index):
        # DE/rand/1: r1 + F(r2-r3); DE/rand/2: r1 + F(r2-r3+r4-r5).
        count = 3 if self.strategy == "rand_1_bin" else 5
        indices = random.sample([i for i in range(self.population_size) if i != target_index], count)
        donors = [self.population[i] for i in indices]
        if count == 3:
            mutant = [a + self.mutation_factor * (b-c) for a,b,c in zip(*donors)]
        else:
            mutant = [a + self.mutation_factor * (b-c+d-e) for a,b,c,d,e in zip(*donors)]
        return self._clip(mutant)

    def crossover(self, target, mutant):
        # Cruce binomial: al menos una dimensión procede del mutante.
        forced_index = random.randrange(len(target))
        return [mutant[i] if i == forced_index or random.random() < self.crossover_rate
                else target[i] for i in range(len(target))]

    def _diversity(self):
        # Distancia Manhattan promedio entre pares de individuos.
        pairs = 0
        distance = 0.0
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                distance += sum(abs(a-b) for a,b in zip(self.population[i], self.population[j]))
                pairs += 1
        return distance / pairs if pairs else 0.0

    def _stats(self, generation, fitnesses):
        return {"generation": generation, "best": min(fitnesses),
                "mean": statistics.fmean(fitnesses), "diversity": self._diversity()}

    def run(self, verbose=True):
        # Cada generación compara descendiente contra objetivo, sin reinicios aleatorios.
        start = time.perf_counter()
        self.population = [self.create_individual() for _ in range(self.population_size)]
        fitnesses = [self.fitness_function(x) for x in self.population]
        initial_best = min(fitnesses)
        best_index = fitnesses.index(initial_best)
        self.best_fitness = initial_best
        self.best_individual = list(self.population[best_index])
        self.history = [self._stats(0, fitnesses)]
        stagnant = 0
        stop_reason = "Máximo de generaciones"
        if verbose:
            print("\nEVOLUCIÓN DIFERENCIAL | Minimización")
            print(f"Función: Sphere | NP={self.population_size} | F={self.mutation_factor} | CR={self.crossover_rate} | {self.strategy}")
            print("┌──────┬──────────────────────┬──────────────────────┬──────────────────────┐")
            print("│ Gen. │ Mejor fitness        │ Fitness medio        │ Diversidad           │")
            print("├──────┼──────────────────────┼──────────────────────┼──────────────────────┤")
        for generation in range(1, self.max_generations + 1):
            if self.best_fitness <= self.tolerance:
                stop_reason = "Tolerancia alcanzada"
                break
            next_population = []
            next_fitnesses = []
            for i, target in enumerate(self.population):
                mutant = self.mutate(i)
                trial = self.crossover(target, mutant)
                trial_fitness = self.fitness_function(trial)
                if trial_fitness <= fitnesses[i]:
                    next_population.append(trial)
                    next_fitnesses.append(trial_fitness)
                else:
                    next_population.append(target)
                    next_fitnesses.append(fitnesses[i])
            self.population = next_population
            fitnesses = next_fitnesses
            generation_best = min(fitnesses)
            if generation_best < self.best_fitness:
                self.best_fitness = generation_best
                self.best_individual = list(self.population[fitnesses.index(generation_best)])
                stagnant = 0
            else:
                stagnant += 1
            stats = self._stats(generation, fitnesses)
            self.history.append(stats)
            if verbose and (generation == 1 or generation % self.print_interval == 0 or generation == self.max_generations):
                print(f"│ {generation:>4} │ {stats['best']:>20.16f} │ {stats['mean']:>20.16f} │ {stats['diversity']:>20.16f} │")
            if self.stagnation_limit > 0 and stagnant >= self.stagnation_limit:
                stop_reason = "Estancamiento"
                break
        elapsed = time.perf_counter() - start
        if verbose:
            print("└──────┴──────────────────────┴──────────────────────┴──────────────────────┘")
            print("╔════════════════════════════════════════════════════╗")
            print("║                 ★ MEJOR RESULTADO ★                ║")
            print("╠════════════════════════════════════════════════════╣")
            results = [("Mejor fitness", f"{self.best_fitness:.16f}"),
                       ("Mejor individuo", "[" + ", ".join(f"{x:.10f}" for x in self.best_individual) + "]"),
                       ("Fitness inicial", f"{initial_best:.16f}"),
                       ("Generaciones", str(self.history[-1]['generation'])),
                       ("Tiempo", f"{elapsed:.4f} s"),
                       ("Parada", stop_reason)]
            for key, value in results:
                text = f"{key}: {value}"
                print("║ " + text[:50].ljust(50) + " ║")
            print("╚════════════════════════════════════════════════════╝")
        return self.best_individual, self.best_fitness


if __name__ == "__main__":
    def sphere(individual):
        return sum(component ** 2 for component in individual)

    # Utiliza los hiperparámetros declarados al inicio del archivo.
    optimizer = DifferentialEvolution(
        fitness_function=sphere,
        bounds=bounds,
        population_size=populationSize,
        max_generations=maxGenerations,
        mutation_factor=mutationFactor,
        crossover_rate=crossoverRate,
        strategy=strategy,
        tolerance=tolerance,
        stagnation_limit=stagnationLimit,
        print_interval=printInterval,
    )
    optimizer.run()
