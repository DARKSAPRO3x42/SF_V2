import random

class JobGeneticAlgorithm:
    def __init__(self, jobs, pop_size=50, generations=100, mutation_rate=0.1):
        self.jobs = jobs
        self.num_jobs = len(jobs)
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def calculate_fitness(self, schedule):
        """Calculates fitness based on weighted wait times."""
        total_cost = 0
        current_wait_time = 0
        
        for job_index in schedule:
            job = self.jobs[job_index]
            # Cost penalty: Wait time multiplied by the job's urgency
            total_cost += current_wait_time * job['urgency']
            # Add this job's processing time to the wait time for the next job
            current_wait_time += job['processing_time']
            
        # We want to minimize cost, so fitness is inversely proportional
        return 1.0 / (total_cost + 1)

    def create_population(self):
        """Creates an initial population of random schedules (permutations)."""
        population = []
        base_schedule = list(range(self.num_jobs))
        for _ in range(self.pop_size):
            shuffled = base_schedule[:]
            random.shuffle(shuffled)
            population.append(shuffled)
        return population

    def selection(self, population, fitnesses):
        """Tournament selection to pick the best parents."""
        tournament_size = 3
        best_idx = -1
        best_fitness = -1
        
        for _ in range(tournament_size):
            idx = random.randint(0, self.pop_size - 1)
            if fitnesses[idx] > best_fitness:
                best_fitness = fitnesses[idx]
                best_idx = idx
        return population[best_idx]

    def crossover(self, parent1, parent2):
        """Order Crossover (OX1) - Ideal for permutation-based chromosomes."""
        start, end = sorted(random.sample(range(self.num_jobs), 2))
        child = [-1] * self.num_jobs
        
        # Copy a random slice from parent 1
        child[start:end] = parent1[start:end]
        
        # Fill the rest with genes from parent 2, preserving their order
        p2_filtered = [gene for gene in parent2 if gene not in child]
        idx = 0
        for i in range(self.num_jobs):
            if child[i] == -1:
                child[i] = p2_filtered[idx]
                idx += 1
        return child

    def mutate(self, schedule):
        """Swap mutation: Randomly swaps two jobs in the schedule."""
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(self.num_jobs), 2)
            schedule[idx1], schedule[idx2] = schedule[idx2], schedule[idx1]
        return schedule

    def run(self):
        """Executes the Genetic Algorithm and returns the best schedule."""
        if self.num_jobs <= 1:
            return list(range(self.num_jobs)) # No optimization needed
            
        population = self.create_population()
        best_schedule = None
        best_fitness_overall = -1

        for _ in range(self.generations):
            fitnesses = [self.calculate_fitness(ind) for ind in population]
            
            # Track the absolute best
            max_fitness_idx = fitnesses.index(max(fitnesses))
            if fitnesses[max_fitness_idx] > best_fitness_overall:
                best_fitness_overall = fitnesses[max_fitness_idx]
                best_schedule = population[max_fitness_idx]

            new_population = []
            # Elitism: keep the best individual
            new_population.append(population[max_fitness_idx])
            
            # Breed the rest of the new generation
            while len(new_population) < self.pop_size:
                p1 = self.selection(population, fitnesses)
                p2 = self.selection(population, fitnesses)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_population.append(child)
                
            population = new_population

        return best_schedule