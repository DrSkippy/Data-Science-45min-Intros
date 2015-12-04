from collections import OrderedDict
import pandas as pd
import numpy as np

from jinja2 import Template

from bokeh.embed import components
from bokeh.models import (
    ColumnDataSource, Plot, Circle, Range1d,
    LinearAxis, HoverTool, Text,
    SingleIntervalTicker, Slider, Callback
)
from bokeh.palettes import Spectral6
from bokeh.plotting import vplot, hplot
from bokeh.resources import INLINE, Resources
from bokeh.templates import RESOURCES


def _get_data():
    # Get the data
    fertility_df = pd.read_csv('assets/fertility.csv', index_col='Country')
    life_expectancy_df = pd.read_csv('assets/life_expectancy.csv', index_col='Country')
    population_df = pd.read_csv('assets/population.csv', index_col='Country')
    regions_df = pd.read_csv('assets/regions.csv', index_col='Country')

    columns = list(fertility_df.columns)
    years = list(range(int(columns[0]), int(columns[-1])))
    rename_dict = dict(zip(columns, years))
    fertility_df = fertility_df.rename(columns=rename_dict)
    life_expectancy_df = life_expectancy_df.rename(columns=rename_dict)
    population_df = population_df.rename(columns=rename_dict)
    regions_df = regions_df.rename(columns=rename_dict)

    scale_factor = 200
    population_df_size = np.sqrt(population_df / np.pi) / scale_factor
    min_size = 3
    population_df_size = population_df_size.where(population_df_size >= min_size).fillna(min_size)

    regions_df.Group = regions_df.Group.astype('category')
    regions = list(regions_df.Group.cat.categories)

    def get_color(r):
        return Spectral6[regions.index(r.Group)]
    regions_df['region_color'] = regions_df.apply(get_color, axis=1)
    return (years, regions, fertility_df, life_expectancy_df, population_df_size, regions_df)


def _get_plot():
    years, regions, fertility_df, life_expectancy_df, population_df_size, regions_df = _get_data()

    # Set-up the sources
    sources = {}

    region_color = regions_df['region_color']
    region_color.name = 'region_color'

    for year in years:
        fertility = fertility_df[year]
        fertility.name = 'fertility'
        life = life_expectancy_df[year]
        life.name = 'life'
        population = population_df_size[year]
        population.name = 'population'
        new_df = pd.concat([fertility, life, population, region_color], axis=1)
        sources['_' + str(year)] = ColumnDataSource(new_df)

    dictionary_of_sources = dict(zip([x for x in years], ['_%s' % x for x in years]))
    js_source_array = str(dictionary_of_sources).replace("'", "")

    # Build the plot

    # Set up the plot
    xdr = Range1d(1, 9)
    ydr = Range1d(20, 100)
    plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=800,
        plot_height=400,
        outline_line_color=None,
        toolbar_location=None,
    )
    AXIS_FORMATS = dict(
        minor_tick_in=None,
        minor_tick_out=None,
        major_tick_in=None,
        major_label_text_font_size="10pt",
        major_label_text_font_style="normal",
        axis_label_text_font_size="10pt",

        axis_line_color='#AAAAAA',
        major_tick_line_color='#AAAAAA',
        major_label_text_color='#666666',

        major_tick_line_cap="round",
        axis_line_cap="round",
        axis_line_width=1,
        major_tick_line_width=1,
    )

    xaxis = LinearAxis(SingleIntervalTicker(interval=1), axis_label="Children per woman (total fertility)", **AXIS_FORMATS)
    yaxis = LinearAxis(SingleIntervalTicker(interval=20), axis_label="Life expectancy at birth (years)", **AXIS_FORMATS)
    plot.add_layout(xaxis, 'below')
    plot.add_layout(yaxis, 'left')
    # Add the year in background (add before circle)
    text_source = ColumnDataSource({'year': ['%s' % years[0]]})
    text = Text(x=2, y=35, text='year', text_font_size='150pt', text_color='#EEEEEE')
    plot.add_glyph(text_source, text)
    # Add the circle
    renderer_source = sources['_%s' % years[0]]
    circle_glyph = Circle(
        x='fertility', y='life', size='population',
        fill_color='region_color', fill_alpha=0.8,
        line_color='#7c7e71', line_width=0.5, line_alpha=0.5)
    circle_renderer = plot.add_glyph(renderer_source, circle_glyph)

    # Add the hover (only against the circle and not other plot elements)
    tooltips = "@index"
    plot.add_tools(HoverTool(tooltips=tooltips, renderers=[circle_renderer]))

    text_x = 7
    text_y = 95
    for i, region in enumerate(regions):
        plot.add_glyph(Text(x=text_x, y=text_y, text=[region], text_font_size='10pt', text_color='#666666'))
        plot.add_glyph(Circle(x=text_x - 0.1, y=text_y + 2, fill_color=Spectral6[i], size=10, line_color=None, fill_alpha=0.8))
        text_y = text_y - 5

    # Add the slider
    code = """
        var year = slider.get('value'),
            sources = %s,
            new_source_data = sources[year].get('data');
        renderer_source.set('data', new_source_data);
        renderer_source.trigger('change');
        text_source.set('data', {'year': [String(year)]});
        text_source.trigger('change');
    """ % js_source_array

    callback = Callback(args=sources, code=code)
    slider = Slider(start=years[0], end=years[-1], value=1, step=1, title="Year", callback=callback)
    callback.args["slider"] = slider
    callback.args["renderer_source"] = renderer_source
    callback.args["text_source"] = text_source

    # Lay it out
    return vplot(plot, hplot(slider))


def get_bubble_html(plot=None):
    if plot:
        layout = plot
    else:
        layout = _get_plot()
    with open('assets/bubble_template.html', 'r') as f:
        template = Template(f.read())
    resources = Resources(mode='server', root_url='/tree/')
    bokeh_js = RESOURCES.render(js_files=resources.js_files)
    script, div = components(layout)
    html = template.render(
        title="Bokeh - Gapminder demo",
        bokeh_js=bokeh_js,
        plot_script=script,
        plot_div=div,
    )
    return html


def get_1964_data():
    years, regions, fertility_df, life_expectancy_df, population_df_size, regions_df = _get_data()
    year = 1964
    region_color = regions_df['region_color']
    region_color.name = 'region_color'
    fertility = fertility_df[year]
    fertility.name = 'fertility'
    life = life_expectancy_df[year]
    life.name = 'life'
    population = population_df_size[year]
    population.name = 'population'
    new_df = pd.concat([fertility, life, population, region_color], axis=1)
    return new_df


def get_scatter_data():
    years, regions, fertility_df, life_expectancy_df, population_df_size, regions_df = _get_data()
    xyvalues = OrderedDict()
    xyvalues['1964'] = list(
        zip(
            fertility_df[1964].dropna().values,
            life_expectancy_df[1964].dropna().values
        )
    )
    return xyvalues
