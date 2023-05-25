"""
This file is the entry point for your application and is used to:

    - Define all entity types that are part of the app, and
    - Create 1 or more initial entities (of above type(s)), which are generated upon starting the app

For more information about this file, see: https://docs.viktor.ai/docs/create-apps/fundamentals/#apppy
"""
# Import required classes and functions
from pathlib import Path
import numpy as np

from viktor import File, Color, ViktorController, UserError
from viktor.core import progress_message
from viktor.external.word import WordFileTag, render_word_file
from viktor.geometry import SquareBeam, Material, Group, LinearPattern
from viktor.result import DownloadResult
from viktor.parametrization import ViktorParametrization, Step, NumberField, DownloadButton, DateField, \
    TextField, LineBreak, GeoPolygonField, BooleanField
from viktor.utils import convert_word_to_pdf
from viktor.views import MapView, MapPoint, MapResult, MapPolygon, PDFView, PDFResult, GeometryView, \
    GeometryResult, DataGroup, DataItem, ImageView, ImageResult, PlotlyAndDataView, PlotlyAndDataResult, \
    WebView, WebResult

from _text_elements import *


class Parametrization(ViktorParametrization):
    """
    A Parametrization defines the fields and views visible in an entity type's editor.
    """

    # ===================================
    # Introduction
    # ===================================

    intro = Step("Intro", views='image_view')
    intro.text1 = introduction_text1

    # ===================================
    # Map View
    # ===================================

    map = Step("Map", views='map_view')
    map.text1 = map_text1
    map.my_geo_polygon = GeoPolygonField(
        "Click the pencil to draw a polygon on the map",
        description="Tip: It is also possible to modify the polygon after drawing")
    map.description = TextField(
        "Enter a description",
        default="This triangle is a big mystery",
        description='Click on the polygon to see this description')
    map.linebreak = LineBreak()
    map.code = BooleanField('**Show the code**')
    map.text2 = map_text3

    # ===================================
    # 3D model
    # ===================================

    design = Step("3D model", views='geometry_view')
    design.text1 = design_text1
    design.width = NumberField("Width", suffix='m', min=10, step=5, default=30)
    design.length = NumberField("Length", suffix='m', min=10, step=5, default=30)
    design.lb1 = LineBreak()
    design.floors = NumberField("Floors", min=3, max=50, step=1, default=20, variant='slider', flex=67)
    design.linebreak = LineBreak()
    design.code = BooleanField('**Show the code**')
    design.text2 = design_text2

    # ===================================
    # Graph
    # ===================================

    calculate = Step("Graphs", views='calculate_contour_plot')
    calculate.text1 = calculate_text1
    calculate.volume = NumberField('Volume, $V$', suffix='m³', min=10, default=50)
    calculate.text2 = calculate_text2
    calculate.min_width = NumberField('Minimum width, $w_{min}$', min=1, default=1, suffix='m')
    calculate.max_width = NumberField('Maximum width, $w_{max}$', min=2, default=10, suffix='m')
    calculate.linebreak2 = LineBreak()
    calculate.min_length = NumberField('Minimum length, $l_{min}$', min=1, default=1, suffix='m')
    calculate.max_length = NumberField('Maximum length, , $l_{max}$', min=2, default=10, suffix='m')
    calculate.linebreak = LineBreak()
    calculate.code = BooleanField('**Show the code**')
    calculate.text3 = calculate_text3
    calculate.text4 = calculate_text4

    # ===================================
    # Report
    # ===================================

    report = Step("Report", views='create_report')
    report.text = report_text1
    report.your_name = TextField("Please enter your name")
    report.lb1 = LineBreak()
    report.your_score = NumberField("Give yourself a score", variant='slider', min=1, max=10, default=10)
    report.lb2 = LineBreak()
    report.date = DateField("Select a date")
    report.lb3 = LineBreak()
    report.text2 = report_text2
    report.linebreak = LineBreak()
    report.code = BooleanField('**Show the code**')
    report.text3 = report_text3
    report.download = DownloadButton("Download template", method="download_template", visible=Lookup('report.code'))
    report.text4 = report_text4

    # ===================================
    # Build your own app
    # ===================================

    evaluate = Step("Build your own app", views='final_step')


# Creates an entity type 'Controller'
class Controller(ViktorController):
    """
    For more information on views, see: https://docs.viktor.ai/docs/create-apps/results-and-visualizations/
    """
    label = 'My Entity Type'  # label of the entity type as seen by the user in the app's interface
    parametrization = Parametrization  # parametrization associated with the editor of the Controller entity type

    @ImageView("View", duration_guess=1, description="This is a View!")
    def image_view(self, params, **kwargs):
        """ https://docs.viktor.ai/docs/create-apps/results-and-visualizations/images """
        svg_path = Path(__file__).parent / 'viktor-app.svg'
        return ImageResult.from_path(svg_path)

    @MapView("Map", duration_guess=1)
    def map_view(self, params, **kwargs):
        map_objects = [
            MapPoint(25.7617, -80.1918, description='Miami'),
            MapPoint(18.4655, -66.1057, description='Puerto Rico'),
            MapPoint(32.3078, -64.7505, description='Bermudas')
        ]

        # get map polygon point from parametrization
        geo_polygon = params.map.my_geo_polygon

        # create map object
        if geo_polygon:
            map_objects.append(MapPolygon.from_geo_polygon(geo_polygon, description=params.map.description))

        # visualize map
        return MapResult(map_objects)

    @GeometryView("Geometry", duration_guess=1)
    def geometry_view(self, params, **kwargs):
        # Get parameters
        width = params.design.width
        length = params.design.length
        floors = params.design.floors
        floor_height = 3

        # Materials
        glass = Material("Glass", color=Color(150, 150, 255))
        facade = Material("Facade", color=Color.white())

        # Create geometry objects
        floor_1 = SquareBeam(width, length, 2, material=glass)
        floor_2 = SquareBeam(width+1, length+1, 1, material=facade)
        floor_2.translate([0, 0, 1.5])

        floor = Group([floor_1, floor_2])
        building = LinearPattern(floor, direction=[0, 0, 1], number_of_elements=floors, spacing=floor_height)

        # add center of building to center of screen
        building.translate((0, 0, - floors * floor_height / 2))

        return GeometryResult(building)

    @PlotlyAndDataView('Surface area plot', duration_guess=1)
    def calculate_contour_plot(self, params, **kwargs):
        min_width = params.calculate.min_width
        max_width = params.calculate.max_width
        min_length = params.calculate.min_length
        max_length = params.calculate.max_length
        volume = params.calculate.volume
        if min_width > max_width or min_length > max_length:
            raise UserError('Check your minimum/maximum values, as the minimum exceeds the maximum.')

        width_array = np.linspace(min_width, max_width, 101)
        length_array = np.linspace(min_length, max_length, 101)
        [w, l] = np.meshgrid(length_array, width_array)
        h = volume / (w * l)
        surface_area = 2 * w * h + 2 * l * h + 2 * w * l
        min_surface_area = np.min(np.min(surface_area))
        width_idx, length_idx = np.where(surface_area==min_surface_area)
        width = float(width_array[width_idx[0]])
        length = float(length_array[length_idx[0]])
        
        item = DataItem(
            f"Minimum surface area", min_surface_area, suffix='m²', number_of_decimals=1,
            subgroup=DataGroup(
                DataItem("Volume", volume, suffix='m³'),
                DataItem("Length", length, suffix='m', number_of_decimals=2),
                DataItem("Width", width, suffix='m', number_of_decimals=2),
                DataItem("Height", volume / (length * width), suffix='m', number_of_decimals=2),
            )
        )
        fig = {
            'data': [{
                'type': "surface",
                'x': width_array.tolist(),
                'y': length_array.tolist(),
                'z': surface_area.tolist(),
                'colorbar': {
                    'title': 'Surface area [m²]',
                    'titleside': 'right'},
                'contours': {'z': {'show': True, 'color': 'white'}},
                'colorscale': 'Jet',
            }
            ],
            'layout': {'title': {'text': f"Box surface area distribution for volume {volume}m³"},
                       'scene': {'xaxis': {'title': {'text': "Width [m]"}},
                                 'yaxis': {'title': {'text': "Length [m]"}},
                                 'zaxis': {'title': {'text': "Surface area [m²]"}}}
                       }
        }
        return PlotlyAndDataResult(fig, data=DataGroup(item))

    @staticmethod
    def download_template(params, entity_name: str, **kwargs):
        """ Enables the user to download a report.

        For more information on downloading files, see: https://docs.viktor.ai/docs/create-apps/managing-files/downloading-files
        """
        template = File.from_path(Path(__file__).parent / 'viktor_certificate.docx')
        return DownloadResult(template, "report_template.docx")

    @PDFView("PDF", duration_guess=10, update_label="Generate certificate",
             description="The PDFView makes it possible to show a static or dynamically generated report directly in "
                         "your VIKTOR app.")
    def create_report(self, params, **kwargs):
        """ Create a report using a Word-file template, converting to PDF, and displaying in a View.

        For more information on Word file templating, see:
        https://docs.viktor.ai/docs/create-apps/documents-and-spreadsheets/word-file-templater

        For more information on displaying a PDF, see:
        https://docs.viktor.ai/docs/create-apps/results-and-visualizations/report
        """
        progress_message("VIKTOR is generating your certificate!")

        # DateField returns a Python datetime object
        date = params.report.date.strftime("%d-%m-%Y") if params.report.date is not None else '-'
        components = [
            WordFileTag('name', params.report.your_name),
            WordFileTag('date', date),
            WordFileTag('score', params.report.your_score),
        ]

        with open(Path(__file__).parent / 'viktor_certificate.docx', 'rb') as r:
            report = render_word_file(r, components)

        with report.open_binary() as r:
            pdf_report = convert_word_to_pdf(r)
              
        return PDFResult(file=pdf_report)

    @WebView('🥳', duration_guess=1)
    def final_step(self, params, **kwargs):
        html_path = Path(__file__).parent / 'final_step.html'
        with html_path.open() as f:
            html_string = f.read()
        return WebResult(html=html_string)
