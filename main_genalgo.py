import random,os
class gen_algo:
    def genetic_algorithm(key):
        target_key = key
        population_size = 100
        mutation_rate = 0.01
        generations = 100

        # Generate an initial population of random keys
        def generate_population(size):
            population = []
            for _ in range(size):
                key = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*-_+=<,.>/?[]{()\|~`}") for _ in range(len(target_key)))
                population.append(key)
            return population

        # Calculate the fitness of each key in the population
        def calculate_fitness(population):
            fitness_scores = []
            for key in population:
                score = sum(1 for a, b in zip(key, target_key) if a == b)
                fitness_scores.append(score)
            return fitness_scores

        # Select parents for mating using roulette wheel selection
        def selection(population, fitness_scores):
            total_fitness = sum(fitness_scores)
            probabilities = [score / total_fitness for score in fitness_scores]
            selected_parents = random.choices(population, probabilities, k=2)
            return selected_parents

        # Perform crossover between two parent keys to produce offspring
        def crossover(parent1, parent2):
            crossover_point = random.randint(1, len(target_key) - 1)
            offspring = parent1[:crossover_point] + parent2[crossover_point:]
            return offspring

        # Perform mutation on a key by randomly changing a character
        def mutate(key):
            mutated_key = list(key)
            for i in range(len(mutated_key)):
                if random.random() < mutation_rate:
                    mutated_key[i] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*-_+=<,.>/?[]{()\|~`}")
            return "".join(mutated_key)

        # Run the genetic algorithm
        def run_genetic_algorithm():
            population = generate_population(population_size)

            for generation in range(generations):
                fitness_scores = calculate_fitness(population)
                best_key = population[fitness_scores.index(max(fitness_scores))]
                # print(f"Generation {generation + 1}: Best key = {best_key}, Fitness = {max(fitness_scores)}")

                new_population = [best_key]

                while len(new_population) < population_size:
                    parent1, parent2 = selection(population, fitness_scores)
                    offspring = crossover(parent1, parent2)
                    mutated_offspring = mutate(offspring)
                    new_population.append(mutated_offspring)

                population = new_population
            # print(f"Generation {generation + 1}: Best key = {best_key}, Fitness = {max(fitness_scores)}")
            return best_key
        return run_genetic_algorithm()