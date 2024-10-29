from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    mean_breakdown = float(request.form['mean_breakdown'])
    std_breakdown = float(request.form['std_breakdown'])
    mean_repair = float(request.form['mean_repair'])
    std_repair = float(request.form['std_repair'])

    # Call your function here and store results
    results = calculate_repairman_problem(mean_breakdown, std_breakdown, mean_repair, std_repair)

    return render_template('index.html', results=results)

def calculate_repairman_problem(mean_breakdown, std_breakdown, mean_repair, std_repair):
    import math
    from scipy.stats import norm

    # Step 1: Calculate mean and standard deviation of D = T_B - T_R
    mean_D = mean_breakdown - mean_repair
    variance_D = (std_breakdown ** 2) + (std_repair ** 2)
    std_D = math.sqrt(variance_D)

    # Step 2: Calculate Z value for D < 0
    Z = (0 - mean_D) / std_D

    # Step 3: Use the normal CDF to calculate the probability of breakdown before repair
    prob_breakdown_before_repair = norm.cdf(Z)

    # Step 4: Calculate expected number of events until the factory halts
    expected_events = 5 / prob_breakdown_before_repair

    # Step 5: Calculate expected total time until halt
    average_time_per_event = (mean_breakdown + mean_repair) / 2
    expected_time = expected_events * average_time_per_event

    # Return results as a dictionary
    return {
        # 'prob_breakdown_before_repair': prob_breakdown_before_repair,
        # 'expected_events': expected_events,
        # 'expected_time': expected_time
        "prob_breakdown_before_repair": f"{prob_breakdown_before_repair:.4f}",
        "expected_events": f"{expected_events:.2f}",
        "expected_time": f"{expected_time:.2f}"
    }

if __name__ == "__main__":
    app.run(debug=True)