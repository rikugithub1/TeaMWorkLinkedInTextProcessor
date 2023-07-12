from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def display_csv():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('google-linkedin-statistics.csv')
    
    df_sorted = df.sort_values(by='Post Order (Old To New)', ascending=True)

    # Convert DataFrame to HTML table
    html_table = df_sorted.to_html(index=False)

    # Render the HTML template with the table
    return render_template('csv_table.html', table=html_table)

if __name__ == '__main__':
    app.run()
