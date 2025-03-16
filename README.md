# Thesis 2022 Dashboard Application

This project is a dashboard application built using Dash and Plotly for visualizing various datasets. The application includes multiple pages for different visualizations 
and is styled using Dash Bootstrap Components.

## Project Structure

- `app.py`: Main application file that initializes the Dash app and server.
- `index.py`: Main entry point for the application. It sets up the layout, sidebar, and routing for different pages.
- `apps/`: Directory containing different visualization pages.
  - `__init__.py`: Initialization file for the `apps` module.
  - `compare_data.py`: Contains the layout and callbacks for the "Compare Data" visualization.
  - `compare_data_clustered.py`: Contains the layout and callbacks for the "Compare Data Clustered" visualization.
  - `visualization1.py`: Contains the layout and callbacks for the "Visualization 1" page.
- `assets/`: Directory containing CSS files for styling the application.
- `datasets/`: Directory containing CSV files used as datasets for the visualizations.
- `Procfile`: File for deployment configuration.
- `requirements.txt`: List of Python dependencies required for the project.
- `vis.py`: Additional visualization script.

To run the application, execute the following command:
python index.py
