import plotly.graph_objects as go
import streamlit as st

from openv2_core import run_openv2


st.set_page_config(
    page_title="OpenV2 Space Colonisation",
    page_icon="🌱",
    layout="wide",
)


def make_animation(result):
    """Build a browser-playable Plotly animation from saved simulation frames."""
    frames_data = result["frames"]
    nx = result["nx"]
    ny = result["ny"]

    def traces_for(snapshot):
        attractors = snapshot["attractors"]
        nodes = snapshot["nodes"]
        return [
            go.Scatter(
                x=attractors[:, 0],
                y=attractors[:, 1],
                mode="markers",
                name="Attractors",
                marker={"color": "#77ac30", "size": 6},
                hovertemplate="Attractor<br>x=%{x:.2f}, y=%{y:.2f}<extra></extra>",
            ),
            go.Scatter(
                x=nodes[:, 0],
                y=nodes[:, 1],
                mode="markers",
                name="Nodes",
                marker={"color": "#222222", "size": 5},
                hovertemplate="Node<br>x=%{x:.2f}, y=%{y:.2f}<extra></extra>",
            ),
            go.Scatter(
                x=[frames_data[0]["nodes"][0, 0]],
                y=[frames_data[0]["nodes"][0, 1]],
                mode="markers",
                name="Root",
                marker={
                    "color": "#a2143d",
                    "size": 14,
                    "symbol": "x",
                    "line": {"width": 3},
                },
                hovertemplate="Root<br>x=%{x:.2f}, y=%{y:.2f}<extra></extra>",
            ),
        ]

    initial_traces = traces_for(frames_data[0])
    plot_frames = []
    slider_steps = []

    for frame_index, snapshot in enumerate(frames_data):
        frame_name = f"iteration-{snapshot['iteration']}"
        plot_frames.append(
            go.Frame(
                name=frame_name,
                data=traces_for(snapshot),
                traces=[0, 1, 2],
                layout=go.Layout(
                    title_text=(
                        f"OpenV2 · iteration {snapshot['iteration']} · "
                        f"{snapshot['nodes'].shape[0]} nodes"
                    )
                ),
            )
        )
        slider_steps.append(
            {
                "label": str(snapshot["iteration"]),
                "method": "animate",
                "args": [
                    [frame_name],
                    {
                        "mode": "immediate",
                        "frame": {"duration": 0, "redraw": True},
                        "transition": {"duration": 0},
                    },
                ],
            }
        )

    figure = go.Figure(
        data=initial_traces,
        frames=plot_frames,
        layout=go.Layout(
            title=(
                f"OpenV2 · iteration 0 · "
                f"{frames_data[0]['nodes'].shape[0]} nodes"
            ),
            height=680,
            margin={"l": 55, "r": 20, "t": 70, "b": 110},
            hovermode="closest",
            legend={"orientation": "h", "y": 1.02, "x": 0},
            xaxis={
                "title": "Distance (µm)",
                "range": [-0.1 * nx, 1.1 * nx],
                "constrain": "domain",
                "zeroline": False,
            },
            yaxis={
                "title": "Distance (µm)",
                "range": [-0.1 * ny, 1.1 * ny],
                "scaleanchor": "x",
                "scaleratio": 1,
                "zeroline": False,
            },
            updatemenus=[
                {
                    "type": "buttons",
                    "direction": "left",
                    "x": 0,
                    "y": -0.13,
                    "showactive": False,
                    "buttons": [
                        {
                            "label": "▶ Play",
                            "method": "animate",
                            "args": [
                                None,
                                {
                                    "fromcurrent": True,
                                    "frame": {
                                        "duration": 75,
                                        "redraw": True,
                                    },
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                        {
                            "label": "⏸ Pause",
                            "method": "animate",
                            "args": [
                                [None],
                                {
                                    "mode": "immediate",
                                    "frame": {
                                        "duration": 0,
                                        "redraw": False,
                                    },
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                    ],
                }
            ],
            sliders=[
                {
                    "active": 0,
                    "x": 0.19,
                    "y": -0.13,
                    "len": 0.81,
                    "currentvalue": {"prefix": "Iteration: "},
                    "steps": slider_steps,
                }
            ],
        ),
    )
    return figure


st.title("OpenV2: Space Colonisation")
st.write(
    "Explore how attractors guide a growing network. Set the space dimensions, "
    "run the simulation, then play the animation or scrub through its iterations."
)

with st.form("simulation_inputs"):
    col_nx, col_ny = st.columns(2)
    nx = col_nx.number_input(
        "Space width, Nx (µm)",
        min_value=40,
        max_value=200,
        value=150,
        step=10,
    )
    ny = col_ny.number_input(
        "Space height, Ny (µm)",
        min_value=40,
        max_value=200,
        value=150,
        step=10,
    )
    submitted = st.form_submit_button("Run simulation", type="primary")

if submitted:
    with st.spinner("Growing the network and preparing animation frames..."):
        try:
            st.session_state["openv2_result"] = run_openv2(int(nx), int(ny))
        except Exception as error:
            st.error(f"The simulation could not complete: {error}")
            st.stop()

    st.session_state["openv2_dimensions"] = (int(nx), int(ny))

result = st.session_state.get("openv2_result")
dimensions = st.session_state.get("openv2_dimensions")

if result is not None:
    metric_cols = st.columns(4)
    metric_cols[0].metric("Iterations", result["iterations"])
    metric_cols[1].metric(
        "Attractors at start",
        f"{result['initial_attractor_count']:,}",
    )
    metric_cols[2].metric(
        "Attractors remaining",
        f"{result['remaining_attractor_count']:,}",
    )
    metric_cols[3].metric(
        "Nodes at end",
        f"{result['final_node_count']:,}",
    )

    st.plotly_chart(
        make_animation(result),
        width="stretch",
        config={"displaylogo": False},
        key=f"openv2-animation-{dimensions[0]}-{dimensions[1]}",
    )
    st.caption(result["stop_reason"])

st.caption(
    "Attractor placement uses a scrambled Halton sequence. The executable's "
    "density formula is 1,000 attractors per 10,000 µm²."
)
