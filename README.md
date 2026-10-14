# OpenV2 Space Colonisation

Python implementation of a space-colonisation growth simulation.

## Run In-Browser

[Click here to run simulation in browser.](https://doguopenvenation.streamlit.app)

OR follow the link: https://doguopenvenation.streamlit.app

Supplied with a desktop Matplotlib executable and an interactive browser app.

## Run the desktop simulation

    uv run python openv2.py

## Run the interactive web app locally

    uv run streamlit run openv2_web/app.py

The web app asks for the space width and height (Nx and Ny), runs the network
growth simulation, and presents its iterations with Plotly Play/Pause controls
and a slider.

## Publish the web app

Push this project to GitHub, then create an app in Streamlit Community Cloud
with openv2_web/app.py as the entrypoint. The project-level pyproject.toml
and uv.lock declare its dependencies.

The executable uses a density formula of 1,000 attractors per 10,000 µm².
The loop stops when a growth iteration adds no nodes.
