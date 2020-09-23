"""Tests of the Cards inspired by Bootstrap Cards.

- [Get Bootstrap Card](https://getbootstrap.com/docs/4.3/components/card/) and
- [Card Collapse Tricks](https://disjfa.github.io/bootstrap-tricks/card-collapse-tricks/)

Please note that

- the css and javascript of Bootstrap and does not play well with Panel/ Bokeh in my
experience, so I've had to create a custom version for Panel/ Bokeh.
    - in order to use the bootstrap functionality you need to run
    `awesome_panel.express.bootstrap.extend()` to import the relevant css.
- I'm not sure this is the right way to implement a new Layout. **Is there some better way
to implement this using the api of Panel and Bokeh?**.
"""
import hvplot.pandas  # pylint: disable=unused-import
import pandas as pd
import panel as pn

import awesome_panel.express as pnx
from awesome_panel.express.testing import TestApp

pnx.bootstrap.extend()

TEXT = """\
Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid.
3 wolf moon officia aute, non cupidatat skateboard dolor brunch.
Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on
 it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft
 beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo.
 Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably
 haven't heard of them accusamus labore sustainable VHS."""


def test_card():
    """We test that we can create a card with

    - A header with lightgray background
    - A Body

    And the card it self is full width responsive by default.
    """

    card = pnx.Card("Card - Header and Body", TEXT, sizing_mode="stretch_width")
    return TestApp(
        test_card,
        card,
        width=600,
        background="ghostwhite",
    )


def test_card_fixed_width():
    """We test that we can create a card with

    - A header with lightgray background
    - A Body

    And the card it self is fixed to 300px
    """
    card = pnx.Card(
        "Card - Fixed Width",
        TEXT,
        width=300,
        sizing_mode="fixed",
    )
    return TestApp(
        test_card_fixed_width,
        card,
        background="ghostwhite",
    )


def _get_chart_data() -> pd.DataFrame:
    """## Chart Data

    Returns:
        pd.DataFrame -- A DataFrame with dummy data and columns=["Day", "Orders"]
    """

    chart_data = {
        "Day": [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ],
        "Orders": [
            15539,
            21345,
            18483,
            24003,
            23489,
            24092,
            12034,
        ],
    }
    return pd.DataFrame(chart_data)


def _holoviews_chart():
    """## Dashboard Orders Chart generated by HoloViews"""
    data = _get_chart_data()
    line_plot = data.hvplot.line(
        x="Day",
        y="Orders",
        width=None,
        height=500,
        line_color="#007BFF",
        line_width=6,
    )
    scatter_plot = data.hvplot.scatter(x="Day", y="Orders", height=300,).opts(
        marker="o",
        size=10,
        color="#007BFF",
    )
    fig = line_plot * scatter_plot
    gridstyle = {
        "grid_line_color": "black",
        "grid_line_width": 0.1,
    }
    fig = fig.opts(
        responsive=True,
        toolbar=None,
        yticks=list(
            range(
                12000,
                26000,
                2000,
            )
        ),
        ylim=(
            12000,
            26000,
        ),
        gridstyle=gridstyle,
        show_grid=True,
    )
    return fig


def test_card_with_plot():
    """We test that we can create a card with

    - A header with lightgray background
    - A Plot Body

    And the card it self is has a fixed width
    """
    card = pnx.Card(
        "Card With Plot",
        _holoviews_chart(),
        width=600,
    )
    return TestApp(
        test_card_with_plot,
        card,
    )


def test_card_with_multiple_panels():
    """We test that we can create a card with

    - A header with lightgray background
    - A Plot Body
    - A Text Body
    - A Plot Body
    - A Text Body

    Please note that due to some Bokeh formatting I've not been able to create
    a divider line that stretches to full width.
    """
    card = pnx.Card(
        "Card With Plot",
        [
            _holoviews_chart(),
            "Awesome Panel! " * 50,
            _holoviews_chart(),
            "Awesome Panel! " * 50,
        ],
        width=600,
    )
    return TestApp(
        test_card_with_multiple_panels,
        card,
    )


def test_card_collapsable():
    """We test that we can create a collapsable card with

    - A header with lightgray background
    - A Plot Body
    - A Text Body

    Please **note** that

    - the header text and collapse button text are not vertically aligned. I have yet to figure
    that out.
    - I have not been able to use the *chevron down* with a *rotation* transition like at
    [Card Collapse Tricks](https://disjfa.github.io/bootstrap-tricks/card-collapse-tricks/)
    - When you click the collabse button, the button is shown for a short while. I would like to
    remove that but I do not yet know how.
    - I would like to change the collapse button callback from a Python callback to JS callback.
    """
    card = pnx.Card(
        "Card with Plot",
        [
            _holoviews_chart(),
            "Awesome Panel! " * 50,
        ],
        collapsable=True,
        width=600,
    )
    return TestApp(
        test_card_collapsable,
        card,
    )


def test_card_with_code():
    """We test that we can create a card with code content"""
    code = """\
        card = pnx.Card("Code", pnx.Code(code),)
        return TestApp(test_card_collapsable, card)"""
    card = pnx.Card("Code", pnx.Code(code))
    return TestApp(test_card_with_code, card, width=600)


def view() -> pn.Column:
    """Wraps all tests in a Column that can be included in the Gallery or served independently

    Returns:
        pn.Column -- A Column containing all the tests
    """
    return pn.Column(
        pn.pane.Markdown(__doc__),
        pn.layout.Divider(),
        test_card(),
        pn.layout.Divider(),
        test_card_fixed_width(),
        pn.layout.Divider(),
        test_card_with_plot(),
        pn.layout.Divider(),
        test_card_with_multiple_panels(),
        pn.layout.Divider(),
        test_card_collapsable(),
        pn.layout.Divider(),
        test_card_with_code(),
        sizing_mode="stretch_width",
    )


if __name__.startswith("bokeh"):
    view().servable()
