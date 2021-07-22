"""Cards inspired by [Get Bootstrap Card](https://getbootstrap.com/docs/4.3/components/card/) and
[Card Collapse Tricks](https://disjfa.github.io/bootstrap-tricks/card-collapse-tricks/).

This example was originally created to show case how to create custom Cards.

The Cards have now been contributed to Panel. Checkout the reference guide
[here](https://panel.holoviz.org/reference/layouts/Card.html).
"""
import hvplot.pandas  # pylint: disable=unused-import
import pandas as pd
import panel as pn
from awesome_panel.express.testing import TestApp
from awesome_panel_extensions.pane import Code

pn.widgets.Button.param.sizing_mode.default = "stretch_width"

from awesome_panel_extensions.site import site

COLOR = "#E1477E"

APPLICATION = site.create_application(
    url="bootstrap-card",
    name="Bootstrap Card",
    author="Marc Skov Madsen",
    description="Demonstrates the look and feel of the Panel Cards",
    description_long=__doc__,
    thumbnail="test_bootstrap_card.png",
    resources={
        "code": "awesome_panel_express_tests/test_bootstrap_card.py",
    },
    tags=[
        "Bootstrap",
    ],
)

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

    - A header and body

    And the card it self is full width responsive.
    """

    card = pn.layout.Card(TEXT, header="Card - Header and Body", sizing_mode="stretch_width")
    return TestApp(
        test_card,
        card,
        width=600,
    )


def test_card_fixed_width():
    """We test that we can create a card with

    - A header and body

    And the card it self is fixed to 300px width
    """
    card = pn.layout.Card(
        TEXT,
        header="Card - Fixed Width",
        width=300,
        sizing_mode="fixed",
    )
    return TestApp(
        test_card_fixed_width,
        card,
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
        height=500,
        line_color=COLOR,
        line_width=6,
    )
    scatter_plot = data.hvplot.scatter(x="Day", y="Orders", height=300,).opts(
        marker="o",
        size=10,
        color=COLOR,
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

    - A header and a body with a plot

    And the card it self is has a fixed width
    """
    card = pn.layout.Card(
        _holoviews_chart(),
        header="Card With Plot",
        sizing_mode="fixed",
        width=800,
    )
    return TestApp(
        test_card_with_plot,
        card,
    )


def test_card_with_multiple_panels():
    """We test that we can create a card with

    - A header
    - A Plot Body
    - A Text Body
    - A Plot Body
    - A Text Body

    """
    card = pn.layout.Card(
        _holoviews_chart(),
        "Awesome Panel! " * 50,
        _holoviews_chart(),
        "Awesome Panel! " * 50,
        header="Card With Plot",
        width=600,
    )
    return TestApp(
        test_card_with_multiple_panels,
        card,
    )


def test_card_collapsible():
    """We test that we can create a collapsible card with

    - A header
    - A Plot Body
    - A Text Body

    """
    card = pn.layout.Card(
        _holoviews_chart(),
        "Awesome Panel! " * 50,
        header="Card with Plot",
        collapsible=True,
        width=600,
    )
    return TestApp(
        test_card_collapsible,
        card,
    )


def test_card_with_code():
    """We test that we can create a card with code content"""
    code = """\
        card = pn.layout.Card("Code", pn.layout.Code(code),)
        return TestApp(test_card_collapsible, card)"""
    card = pn.layout.Card(Code(code), header="Code")
    return TestApp(test_card_with_code, card, width=600)


@site.add(APPLICATION)
def view() -> pn.Column:
    """Wraps all tests in a Column that can be included in the Gallery or served independently

    Returns:
        pn.Column -- A Column containing all the tests
    """
    pn.config.sizing_mode = "stretch_width"
    main = [
        APPLICATION.intro_section(),
        test_card(),
        test_card_fixed_width(),
        test_card_with_plot(),
        test_card_with_multiple_panels(),
        test_card_collapsible(),
        test_card_with_code(),
    ]
    return pn.template.FastListTemplate(title="Test Bootstrap Card", main=main)


if __name__.startswith("bokeh"):
    view().servable()
