import os
import pathlib
import csv
from time import time
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import serial
import asyncio

import pandas as pd

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Variable Resistor Deshboard"
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "spc_data.csv")))

params = list(df)
max_length = len(df)

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("MTE201 Course Project"),
                    html.H6("Jenna Kong, Carter Demars, Rumaisa Bhatti, Albert Wood"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.A(
                        html.Button(children="ENTERPRISE DEMO"),
                        href="https://plotly.com/get-demo/",
                    ),
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.A(
                        html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png")),
                        href="https://plotly.com/dash/",
                    ),
                ],
            ),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Variable Resistor Dashboard",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    )
                ],
            )
        ],
    )






def build_tab_1():
    return [
        # Manually select metrics
        html.Div(
            id="set-specs-intro-container",
            # className='twelve columns',
            children=html.P(
                "Use historical control limits to establish a benchmark, or set new values."
            ),
        ),
        html.Div(
            id="settings-menu",
            children=[
                html.Div(
                    id="metric-select-menu",
                    # className='five columns',
                    children=[
                        html.Label(id="metric-select-title", children="Select Metrics"),
                        html.Br(),
                        dcc.Dropdown(
                            id="metric-select-dropdown",
                            options=list(
                                {"label": param, "value": param} for param in params[1:]
                            ),
                            value=params[1],
                        ),
                    ],
                ),
                html.Div(
                    id="value-setter-menu",
                    # className='six columns',
                    children=[
                        html.Div(id="value-setter-panel"),
                        html.Br(),
                        html.Div(
                            id="button-div",
                            children=[
                                html.Button("Update", id="value-setter-set-btn"),
                                html.Button(
                                    "View current setup",
                                    id="value-setter-view-btn",
                                    n_clicks=0,
                                ),
                            ],
                        ),
                        html.Div(
                            id="value-setter-view-output", className="output-datatable"
                        ),
                    ],
                ),
            ],
        ),
    ]


def build_value_setter_line(line_num, label, value, col3):
    return html.Div(
        id=line_num,
        children=[
            html.Label(label, className="four columns"),
            html.Label(value, className="four columns"),
            html.Div(col3, className="four columns"),
        ],
        className="row",
    )

def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("Operator ID"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value="1704",
                        color="#92e0d3",
                        backgroundColor="#1e2130",
                        size=50,
                    ),
                ],
            ),
            html.Div(
                id="card-2",
                children=[
                    html.P("Time to completion"),
                    daq.Gauge(
                        id="progress-gauge",
                        max=max_length * 2,
                        min=0,
                        showCurrentValue=True,  # default size 200 pixel
                    ),
                ],
            ),
            html.Div(
                id="utility-card",
                children=[daq.StopButton(id="stop-button", size=160, n_clicks=0)],
            ),
        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)

def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("Live SPC Chart"),
            dcc.Graph(
                id="control-chart-live",
                figure=generate_graph()
            ),
        ],
    )


def generate_graph():
    import plotly.express as px
    import pandas as pd

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    fig = px.line(df, x='Date', y='AAPL.High', title='Time Series with Range Slider and Selectors')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig


    # stats = state_dict[col]
    # col_data = stats["data"]
    # mean = stats["mean"]
    # ucl = specs_dict[col]["ucl"]
    # lcl = specs_dict[col]["lcl"]
    # usl = specs_dict[col]["usl"]
    # lsl = specs_dict[col]["lsl"]
    #
    # x_array = state_dict["Batch"]["data"].tolist()
    # y_array = col_data.tolist()
    #
    # total_count = 0
    #
    # if interval > max_length:
    #     total_count = max_length - 1
    # elif interval > 0:
    #     total_count = interval
    #
    # ooc_trace = {
    #     "x": [],
    #     "y": [],
    #     "name": "Out of Control",
    #     "mode": "markers",
    #     "marker": dict(color="rgba(210, 77, 87, 0.7)", symbol="square", size=11),
    # }
    #
    # for index, data in enumerate(y_array[:total_count]):
    #     if data >= ucl or data <= lcl:
    #         ooc_trace["x"].append(index + 1)
    #         ooc_trace["y"].append(data)
    #
    # histo_trace = {
    #     "x": x_array[:total_count],
    #     "y": y_array[:total_count],
    #     "type": "histogram",
    #     "orientation": "h",
    #     "name": "Distribution",
    #     "xaxis": "x2",
    #     "yaxis": "y2",
    #     "marker": {"color": "#f4d44d"},
    # }
    #
    # fig = {
    #     "data": [
    #         {
    #             "x": x_array[:total_count],
    #             "y": y_array[:total_count],
    #             "mode": "lines+markers",
    #             "name": col,
    #             "line": {"color": "#f4d44d"},
    #         },
    #         ooc_trace,
    #         histo_trace,
    #     ]
    # }
    #
    # len_figure = len(fig["data"][0]["x"])
    #
    # fig["layout"] = dict(
    #     margin=dict(t=40),
    #     hovermode="closest",
    #     uirevision=col,
    #     paper_bgcolor="rgba(0,0,0,0)",
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     legend={"font": {"color": "darkgray"}, "orientation": "h", "x": 0, "y": 1.1},
    #     font={"color": "darkgray"},
    #     showlegend=True,
    #     xaxis={
    #         "zeroline": False,
    #         "showgrid": False,
    #         "title": "Batch Number",
    #         "showline": False,
    #         "domain": [0, 0.8],
    #         "titlefont": {"color": "darkgray"},
    #     },
    #     yaxis={
    #         "title": col,
    #         "showgrid": False,
    #         "showline": False,
    #         "zeroline": False,
    #         "autorange": True,
    #         "titlefont": {"color": "darkgray"},
    #     },
    #     annotations=[
    #         {
    #             "x": 0.75,
    #             "y": lcl,
    #             "xref": "paper",
    #             "yref": "y",
    #             "text": "LCL:" + str(round(lcl, 3)),
    #             "showarrow": False,
    #             "font": {"color": "white"},
    #         },
    #         {
    #             "x": 0.75,
    #             "y": ucl,
    #             "xref": "paper",
    #             "yref": "y",
    #             "text": "UCL: " + str(round(ucl, 3)),
    #             "showarrow": False,
    #             "font": {"color": "white"},
    #         },
    #         {
    #             "x": 0.75,
    #             "y": usl,
    #             "xref": "paper",
    #             "yref": "y",
    #             "text": "USL: " + str(round(usl, 3)),
    #             "showarrow": False,
    #             "font": {"color": "white"},
    #         },
    #         {
    #             "x": 0.75,
    #             "y": lsl,
    #             "xref": "paper",
    #             "yref": "y",
    #             "text": "LSL: " + str(round(lsl, 3)),
    #             "showarrow": False,
    #             "font": {"color": "white"},
    #         },
    #         {
    #             "x": 0.75,
    #             "y": mean,
    #             "xref": "paper",
    #             "yref": "y",
    #             "text": "Targeted mean: " + str(round(mean, 3)),
    #             "showarrow": False,
    #             "font": {"color": "white"},
    #         },
    #     ],
    #     shapes=[
    #         {
    #             "type": "line",
    #             "xref": "x",
    #             "yref": "y",
    #             "x0": 1,
    #             "y0": usl,
    #             "x1": len_figure + 1,
    #             "y1": usl,
    #             "line": {"color": "#91dfd2", "width": 1, "dash": "dot"},
    #         },
    #         {
    #             "type": "line",
    #             "xref": "x",
    #             "yref": "y",
    #             "x0": 1,
    #             "y0": lsl,
    #             "x1": len_figure + 1,
    #             "y1": lsl,
    #             "line": {"color": "#91dfd2", "width": 1, "dash": "dot"},
    #         },
    #         {
    #             "type": "line",
    #             "xref": "x",
    #             "yref": "y",
    #             "x0": 1,
    #             "y0": ucl,
    #             "x1": len_figure + 1,
    #             "y1": ucl,
    #             "line": {"color": "rgb(255,127,80)", "width": 1, "dash": "dot"},
    #         },
    #         {
    #             "type": "line",
    #             "xref": "x",
    #             "yref": "y",
    #             "x0": 1,
    #             "y0": mean,
    #             "x1": len_figure + 1,
    #             "y1": mean,
    #             "line": {"color": "rgb(255,127,80)", "width": 2},
    #         },
    #         {
    #             "type": "line",
    #             "xref": "x",
    #             "yref": "y",
    #             "x0": 1,
    #             "y0": lcl,
    #             "x1": len_figure + 1,
    #             "y1": lcl,
    #             "line": {"color": "rgb(255,127,80)", "width": 1, "dash": "dot"},
    #         },
    #     ],
    #     xaxis2={
    #         "title": "Count",
    #         "domain": [0.8, 1],  # 70 to 100 % of width
    #         "titlefont": {"color": "darkgray"},
    #         "showgrid": False,
    #     },
    #     yaxis2={
    #         "anchor": "free",
    #         "overlaying": "y",
    #         "side": "right",
    #         "showticklabels": False,
    #         "titlefont": {"color": "darkgray"},
    #     },
    # )
    #
    # return fig


# def update_sparkline(interval, param):
#     x_array = state_dict["Batch"]["data"].tolist()
#     y_array = state_dict[param]["data"].tolist()
#
#     if interval == 0:
#         x_new = y_new = None
#
#     else:
#         if interval >= max_length:
#             total_count = max_length
#         else:
#             total_count = interval
#         x_new = x_array[:total_count][-1]
#         y_new = y_array[:total_count][-1]
#
#     return dict(x=[[x_new]], y=[[y_new]]), [0]

#
# def update_count(interval, col, data):
#     if interval == 0:
#         return "0", "0.00%", 0.00001, "#92e0d3"
#
#     if interval > 0:
#
#         if interval >= max_length:
#             total_count = max_length - 1
#         else:
#             total_count = interval - 1
#
#         ooc_percentage_f = data[col]["ooc"][total_count] * 100
#         ooc_percentage_str = "%.2f" % ooc_percentage_f + "%"
#
#         # Set maximum ooc to 15 for better grad bar display
#         if ooc_percentage_f > 15:
#             ooc_percentage_f = 15
#
#         if ooc_percentage_f == 0.0:
#             ooc_grad_val = 0.00001
#         else:
#             ooc_grad_val = float(ooc_percentage_f)
#
#         # Set indicator theme according to threshold 5%
#         if 0 <= ooc_grad_val <= 5:
#             color = "#92e0d3"
#         elif 5 < ooc_grad_val < 7:
#             color = "#f4d44d"
#         else:
#             color = "#FF0000"
#
#     return str(total_count + 1), ooc_percentage_str, ooc_grad_val, color


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="value-setter-store", data=df.to_dict()),
        dcc.Store(id="n-interval-stage", data=50),
    ],
)


@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return build_tab_1(), stopped_interval
    return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                html.Div(
                    id="graphs-container",
                    children=[build_chart_panel()],
                ),
            ],
        ),
        stopped_interval,
    )

# Update interval
@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
    [
        State("interval-component", "n_intervals"),
        State("interval-component", "disabled"),
        State("n-interval-stage", "data"),
    ],
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    return cur_stage


# Callbacks for stopping interval update
@app.callback(
    [Output("interval-component", "disabled"), Output("stop-button", "buttonText")],
    [Input("stop-button", "n_clicks")],
    [State("interval-component", "disabled")],
)
def stop_production(n_clicks, current):
    if n_clicks == 0:
        return True, "start recording"
    return not current, "stop" if current else "start"


# ======= Callbacks for modal popup =======
# @app.callback(
#     Output("markdown", "style"),
#     [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
# )
# def update_click_output(button_click, close_click):
#     ctx = dash.callback_context
#
#     if ctx.triggered:
#         prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
#         if prop_id == "learn-more-button":
#             return {"display": "block"}
#
#     return {"display": "none"}


# ======= update progress gauge =========
@app.callback(
    output=Output("progress-gauge", "value"),
    inputs=[Input("interval-component", "n_intervals")],
)
def update_gauge(interval):
    if interval < max_length:
        total_count = interval
    else:
        total_count = max_length

    return int(total_count)


# ===== Callbacks to update values based on store data and dropdown selection =====
@app.callback(
    output=[
        Output("value-setter-panel", "children"),
        Output("ud_usl_input", "value"),
        Output("ud_lsl_input", "value"),
        Output("ud_ucl_input", "value"),
        Output("ud_lcl_input", "value"),
    ],
    inputs=[Input("metric-select-dropdown", "value")],
    state=[State("value-setter-store", "data")],
)
# def build_value_setter_panel(dd_select, state_value):
#     return (
#         [
#             build_value_setter_line(
#                 "value-setter-panel-header",
#                 "Specs",
#                 "Historical Value",
#                 "Set new value",
#             ),
#             build_value_setter_line(
#                 "value-setter-panel-usl",
#                 "Upper Specification limit",
#                 state_dict[dd_select]["usl"],
#                 ud_usl_input,
#             ),
#             build_value_setter_line(
#                 "value-setter-panel-lsl",
#                 "Lower Specification limit",
#                 state_dict[dd_select]["lsl"],
#                 ud_lsl_input,
#             ),
#             build_value_setter_line(
#                 "value-setter-panel-ucl",
#                 "Upper Control limit",
#                 state_dict[dd_select]["ucl"],
#                 ud_ucl_input,
#             ),
#             build_value_setter_line(
#                 "value-setter-panel-lcl",
#                 "Lower Control limit",
#                 state_dict[dd_select]["lcl"],
#                 ud_lcl_input,
#             ),
#         ],
#         state_value[dd_select]["usl"],
#         state_value[dd_select]["lsl"],
#         state_value[dd_select]["ucl"],
#         state_value[dd_select]["lcl"],
#     )


# ====== Callbacks to update stored data via click =====
@app.callback(
    output=Output("value-setter-store", "data"),
    inputs=[Input("value-setter-set-btn", "n_clicks")],
    state=[
        State("metric-select-dropdown", "value"),
        State("value-setter-store", "data"),
        State("ud_usl_input", "value"),
        State("ud_lsl_input", "value"),
        State("ud_ucl_input", "value"),
        State("ud_lcl_input", "value"),
    ],
)


@app.callback(
    output=Output("value-setter-view-output", "children"),
    inputs=[
        Input("value-setter-view-btn", "n_clicks"),
        Input("metric-select-dropdown", "value"),
        Input("value-setter-store", "data"),
    ],
)
# def show_current_specs(n_clicks, dd_select, store_data):
#     if n_clicks > 0:
#         curr_col_data = store_data[dd_select]
#         new_df_dict = {
#             "Specs": [
#                 "Upper Specification Limit",
#                 "Lower Specification Limit",
#                 "Upper Control Limit",
#                 "Lower Control Limit",
#             ],
#             "Current Setup": [
#                 curr_col_data["usl"],
#                 curr_col_data["lsl"],
#                 curr_col_data["ucl"],
#                 curr_col_data["lcl"],
#             ],
#         }
#         new_df = pd.DataFrame.from_dict(new_df_dict)
#         return dash_table.DataTable(
#             style_header={"fontWeight": "bold", "color": "inherit"},
#             style_as_list_view=True,
#             fill_width=True,
#             style_cell_conditional=[
#                 {"if": {"column_id": "Specs"}, "textAlign": "left"}
#             ],
#             style_cell={
#                 "backgroundColor": "#1e2130",
#                 "fontFamily": "Open Sans",
#                 "padding": "0 2rem",
#                 "color": "darkgray",
#                 "border": "none",
#             },
#             css=[
#                 {"selector": "tr:hover td", "rule": "color: #91dfd2 !important;"},
#                 {"selector": "td", "rule": "border: none !important;"},
#                 {
#                     "selector": ".dash-cell.focused",
#                     "rule": "background-color: #1e2130 !important;",
#                 },
#                 {"selector": "table", "rule": "--accent: #1e2130;"},
#                 {"selector": "tr", "rule": "background-color: transparent"},
#             ],
#             data=new_df.to_dict("rows"),
#             columns=[{"id": c, "name": c} for c in ["Specs", "Current Setup"]],
#         )


# decorator for list of output
# def create_callback(param):
#     def callback(interval, stored_data):
#         count, ooc_n, ooc_g_value, indicator = update_count(
#             interval, param, stored_data
#         )
#         spark_line_data = update_sparkline(interval, param)
#         return count, spark_line_data, ooc_n, ooc_g_value, indicator
#
#     return callback


# for param in params[1:]:
#     update_param_row_function = create_callback(param)
#     app.callback(
#         output=[
#             Output(param + suffix_count, "children"),
#             Output(param + suffix_sparkline_graph, "extendData"),
#             Output(param + suffix_ooc_n, "children"),
#             Output(param + suffix_ooc_g, "value"),
#             Output(param + suffix_indicator, "color"),
#         ],
#         inputs=[Input("interval-component", "n_intervals")],
#         state=[State("value-setter-store", "data")],
#     )(update_param_row_function)


# @app.callback(
#     output=Output("control-chart-live", "figure"),
#     inputs=[
#         Input("interval-component", "n_intervals"),
#         Input(params[1] + suffix_button_id, "n_clicks"),
#         Input(params[2] + suffix_button_id, "n_clicks"),
#         Input(params[3] + suffix_button_id, "n_clicks"),
#         Input(params[4] + suffix_button_id, "n_clicks"),
#         Input(params[5] + suffix_button_id, "n_clicks"),
#         Input(params[6] + suffix_button_id, "n_clicks"),
#         Input(params[7] + suffix_button_id, "n_clicks"),
#     ],
#     state=[State("value-setter-store", "data"), State("control-chart-live", "figure")],
# )
# def update_control_chart(interval, n1, n2, n3, n4, n5, n6, n7, data, cur_fig):
#     # Find which one has been triggered
#     ctx = dash.callback_context
#
#     if not ctx.triggered:
#         return generate_graph(interval, data, params[1])
#
#     if ctx.triggered:
#         # Get most recently triggered id and prop_type
#         splitted = ctx.triggered[0]["prop_id"].split(".")
#         prop_id = splitted[0]
#         prop_type = splitted[1]
#
#         if prop_type == "n_clicks":
#             curr_id = cur_fig["data"][0]["name"]
#             prop_id = prop_id[:-7]
#             if curr_id == prop_id:
#                 return generate_graph(interval, data, curr_id)
#             else:
#                 return generate_graph(interval, data, prop_id)
#
#         if prop_type == "n_intervals" and cur_fig is not None:
#             curr_id = cur_fig["data"][0]["name"]
#             return generate_graph(interval, data, curr_id)

def read_data(filename):
    pass

async def write_data():
    import datetime

    data = pd.DataFrame([[0.0, 0.0]], columns=['voltage', 'distance'], index=[datetime.datetime.now()])

    # report a message
    print('Coroutine is running')
    print(data)
    ser = serial.Serial('/dev/cu.usbmodem142401', timeout=1)
    #f = open("/data/voltages.csv", "a+")
    #writer = csv.writer(f, delimiter=',')

    while True:
        await asyncio.sleep(0.6)
        s = ser.readline().decode()
        rows = [float(x) for x in s.split(',')]
        #eq = 9.0e-5*rows[0]**2 - 0.1062*rows[0] + 30.772
        eq = 9.0e-5*rows[0]**2 - 0.1062*rows[0] + 30.696
        a = 0.0 if rows[0] <= 150 else 14-round(eq,1)
        rows.append(a)
        cur = pd.DataFrame([rows], columns=['voltage', 'distance'], index=[datetime.datetime.now()])
        data = pd.concat([data, cur])
        print(cur.values[0])
        # if s != "":
        #     rows = [float(x) for x in s.split(',')]
        #     # Insert local time to list's first position
        #     rows.insert(0, int(time()))
        #     print(rows)
        #     writer.writerow(rows)
        #     f.flush()


async def main():
    task = asyncio.create_task(write_data())
    await asyncio.sleep(0)
    # report a message
    #print('Main doing other stuff...')
    # simulate continue on with other things

    while True:
        await asyncio.sleep(5)
        #print('main still running')
    #app.run_server(debug=True, port=8050)


# Running the server
if __name__ == "__main__":
    asyncio.run(main())