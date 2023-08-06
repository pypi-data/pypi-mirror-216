import numpy as np
from geci_plots import geci_plot, roundup, ticks_positions_array, order_magnitude
from bootstrapping_tools import power_law
import matplotlib.pyplot as plt


def resample_seasons(df):
    first_season = int(df.Temporada.min())
    last_season = int(df.Temporada.max())
    return np.linspace(first_season, last_season, last_season - first_season + 1).astype(int)


def calculate_upper_limit(data_interest_variable):
    upper_limit = roundup(
        data_interest_variable.max() * 1.2,
        10 ** order_magnitude(data_interest_variable),
    )
    return upper_limit


class Population_Trend_Model:
    def __init__(self, fit_data, intervals, interest_variable):
        self.intervals = intervals
        self.plot_seasons = fit_data["Temporada"][:] - fit_data["Temporada"].iloc[0] + 1
        self.ticks_text = resample_seasons(fit_data)
        self.ticks_positions = ticks_positions_array(self.ticks_text)
        self.time_to_model = np.linspace(
            self.ticks_positions.min(), self.ticks_positions.max(), 100
        )
        self.initial_population = fit_data[interest_variable].iloc[0]

    @property
    def model_min(self):
        return power_law(self.time_to_model, self.intervals[0], self.initial_population)

    @property
    def model_med(self):
        return power_law(self.time_to_model, self.intervals[1], self.initial_population)

    @property
    def model_max(self):
        return power_law(self.time_to_model, self.intervals[2], self.initial_population)


class Plotter_Population_Trend_Model:
    def __init__(self):
        self.fig, self.ax = geci_plot()

    def plot_smooth(self, Population_Trend_Model):
        self.ax.fill_between(
            Population_Trend_Model.time_to_model,
            Population_Trend_Model.model_min,
            Population_Trend_Model.model_max,
            alpha=0.2,
            label="Confidence zone",
            color="b",
        )

    def plot_model(self, Population_Trend_Model):
        plt.plot(
            Population_Trend_Model.time_to_model,
            Population_Trend_Model.model_med,
            label="Population growth model",
            color="b",
        )
        return self.fig

    def plot_data(self, Population_Trend_Model, fit_data):
        plt.plot(
            Population_Trend_Model.plot_seasons,
            fit_data,
            "-Dk",
            label="Active Nests",
        )

    def plot_growth_rate_interval(self, legend_mpl_object, lambda_latex):
        legend_box_positions = legend_mpl_object.get_window_extent()
        self.ax.annotate(
            r"$\lambda =$ {}".format(lambda_latex),
            (legend_box_positions.p0[0], legend_box_positions.p1[1] - 320),
            xycoords="figure pixels",
            fontsize=25,
            color="k",
            alpha=1,
        )

    def set_y_lim(self, fit_data):
        self.ax.set_ylim(
            0,
            calculate_upper_limit(fit_data),
        )

    def set_x_lim(self, Population_Trend_Model):
        plt.xlim(
            Population_Trend_Model.ticks_positions.min() - 0.2,
            Population_Trend_Model.ticks_positions.max(),
        )

    def set_labels(self):
        plt.ylabel("Number of breeding pairs", size=20)
        plt.xlabel("Seasons", size=20)

    def set_ticks(self, Population_Trend_Model):
        plt.xticks(
            Population_Trend_Model.ticks_positions,
            Population_Trend_Model.ticks_text,
            rotation=90,
            size=20,
        )
        plt.yticks(size=20)

    def draw(self):
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.draw()

    def savefig(self, islet, output_path=None):
        if output_path is None:
            plt.savefig(
                "reports/figures/cormorant_population_trend_{}".format(
                    islet.replace(" ", "_").lower()
                ),
                dpi=300,
            )
        else:
            plt.savefig(
                output_path,
                dpi=300,
            )

    def set_legend_location(self, islet):
        legend_mpl_object = plt.legend(loc="best")
        if islet == "Natividad":
            legend_mpl_object = plt.legend(loc="upper left")
        return legend_mpl_object
