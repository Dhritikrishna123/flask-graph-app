from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    # Get data from the form
    ix_values = request.form.get('ix_values').split(',')
    vh_values_1 = request.form.get('vh_values_1').split(',')
    bz_values = request.form.get('bz_values').split(',')
    vh_values_2 = request.form.get('vh_values_2').split(',')

    # Convert string inputs to float
    Ix = [float(x) for x in ix_values]
    Vh1 = [float(y) for y in vh_values_1]
    Bz = [float(z) for z in bz_values]
    Vh2 = [float(w) for w in vh_values_2]

    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

    # Plotting Vh vs Ix
    ax1.plot(Ix, Vh1, marker='o', linestyle='-', color='blue')
    ax1.set_title('Hall Voltage (V$_h$) vs Current (I$_x$)', fontsize=14)
    ax1.set_xlabel('Current (I$_x$) in A', fontsize=12)
    ax1.set_ylabel('Hall Voltage (V$_h$) in mV', fontsize=12)
    ax1.grid(True)

    # Plotting Vh vs Bz
    ax2.plot(Bz, Vh2, marker='o', linestyle='-', color='green')
    ax2.set_title('Hall Voltage (V$_h$) vs Magnetic Field (B$_z$)', fontsize=14)
    ax2.set_xlabel('Magnetic Field (B$_z$) in Wb/cm²', fontsize=12)
    ax2.set_ylabel('Hall Voltage (V$_h$) in mV', fontsize=12)
    ax2.grid(True)

    # Save the plot
    plot_path = os.path.join('static', 'plot.png')
    pdf_path = os.path.join('static', 'plot.pdf')
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.savefig(pdf_path)  # Save as PDF as well
    plt.close()

    return render_template('result.html', plot_url=plot_path)

@app.route('/save_pdf', methods=['POST'])
def save_pdf():
    plot_url = request.form['plot_url']
    pdf_path = os.path.join('static', 'plot.pdf')

    return send_file(pdf_path, as_attachment=True, download_name='plot.pdf')

if __name__ == '__main__':
    app.run(debug=True)
