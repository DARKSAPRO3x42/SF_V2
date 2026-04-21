from flask import Flask, request, jsonify, render_template
from ga_optimizer import JobGeneticAlgorithm

app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    jobs = data.get('jobs', [])
    
    if not jobs:
        return jsonify({'optimized_schedule': []})

    # Instantiate the modular Genetic Algorithm
    # Scalability: You can easily adjust pop_size and generations here for larger datasets
    ga = JobGeneticAlgorithm(jobs=jobs, pop_size=100, generations=150, mutation_rate=0.15)
    
    # Run the evolution
    best_schedule_indices = ga.run()
    
    # Map the optimal indices back to the original job data
    optimized_schedule = []
    for rank, original_index in enumerate(best_schedule_indices):
        job = jobs[original_index]
        optimized_schedule.append({
            'job_id': job['id'],
            'original_position': original_index + 1,
            'execution_order': rank + 1
        })
        
    return jsonify({'optimized_schedule': optimized_schedule})

if __name__ == '__main__':
    app.run(debug=True)