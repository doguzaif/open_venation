OpenV2 interactive web app

This app turns the supplied OpenV2 growth simulation into a browser interface.
Visitors enter Nx and Ny, start a run, then use Plotly's Play/Pause controls or
iteration slider to explore the resulting animation.

Files

- app.py: Streamlit interface and Plotly animation.
- openv2_core.py: Attractor setup, node growth loop, and iteration snapshots.
- eucDistOV.py, newNodeOV2.py, vectorNorm.py: Simulation helpers.
- Dependencies are declared in the parent project's pyproject.toml and uv.lock.

Run locally from the Simulation_Python project directory:

    uv run streamlit run openv2_web/app.py

Deploying

1. Push the project to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set the entrypoint to openv2_web/app.py.
4. Community Cloud will install dependencies from the project's uv.lock.
5. Choose a memorable streamlit.app subdomain and deploy.

The web version keeps the executable's quasi-random attractor placement and
1,000-attractors-per-10,000-µm² density formula. Its stopping check compares
the actual node-row count before and after growth, so it stops when an
iteration adds no nodes.
