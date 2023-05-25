""" This file contains all Text elements that are used in the demo app, in order to keep the `app.py` file clean. """

from viktor.parametrization import Text, Lookup

# ======================================
# Introduction
# ======================================


introduction_text1 = Text("""

# 👋 Welcome to the demo app! 

This app will take you on a journey, and along the way, present you with features and functionalities that may be 
helpful when creating you own VIKTOR apps. But before we start, here are some fundamentals of VIKTOR apps:

- **User input:** You can add input fields, sliders, buttons and formatted text (like this) on the left side of the app. 
We call this part the `Parametrization`.

- **Results:** At the right-hand side of your app, you can show 3D models, maps, graphs, reports, pictures (like the one 
on the right) and much more. We call this a `View`.

- **Logic:** Each time you change an input field, the app runs your Python code in the background and shows the results 
in the View. You can also integrate other software packages.

To continue, press on the 'Next step' button.
""")

# ======================================
# Map
# ======================================

map_text1 = Text("""
# Interactive Maps

You can show points, (poly)lines, polygons, labels and legends on a map using numerical data 
(calculations, JSON, etc.) or user input.
""")

map_text3 = Text("""
Input fields can be added with a single line of code:

```python
my_geo_polygon = GeoPolygonField("Join the points with a polygon")
description = TextField(
    "Enter a description", 
    default="This triangle is a big mystery") 
```

Creating a map and showing results is as simple as defining a function in Python.

**Note:** all input fields are stored in a single variable called *params*, which is passed to the function as a keyword argument.
The input fields can be retrieved as an attribute of the *params*. For example, the input field `my_geo_polygon` is accessible
through `params.my_geo_polygon`.

```python
@MapView("Map", duration_guess=1)
def map_view(self, params, **kwargs):
    # Draw some points using coordinates (static)
    map_objects = [
        MapPoint(25.7617, -80.1918, description='Miami'),
        MapPoint(18.4655, -66.1057, description='Puerto Rico'),
        MapPoint(32.3078, -64.7505, description='Bermudas')
    ]

    # get map polygon point provided by the user from parametrization
    geo_polygon = params.my_geo_polygon

    # Draw a MapPolygon using the coordinates stored in geo_polygon
    if geo_polygon:
        map_objects.append(MapPolygon.from_geo_polygon(geo_polygon, description=params.description))

    # visualize map
    return MapResult(map_objects)
```
""", visible=Lookup('map.code'))

# ======================================
# 3D model
# ======================================

design_text1 = Text("""
# 3D models
Build parametric 3D models using VIKTOR's geometry module or import them from other software like Grasshopper or Dynamo.
""")

design_text2 = Text("""

The input fields are defined as follows:

```python
width = NumberField("Width", suffix='m', min=10, step=5, default=30)
length = NumberField("Length", suffix='m', min=10, step=5, default=30)
number_of_floors = NumberField("Floors", min=3, max=50, step=1, default=20, variant='slider')
```

This 3D model is created using components from VIKTOR's geometry module, like `Material`, `Color`, `SquareBeam`, 
`Group` and `LinearPattern`.

```python
@GeometryView("Geometry", duration_guess=1)
def geometry_view(self, params, **kwargs):

    # Define Materials
    glass = Material("Glass", color=Color(150, 150, 255))
    facade = Material("Facade", color=Color.white())

    # Create one floor
    floor_glass = SquareBeam(params.width, params.length, 2, material=glass)
    floor_facade = SquareBeam(params.width+1, params.length+1, 1, material=facade)
    floor_facade.translate([0, 0, 1.5])

    # Pattern (duplicate) the floor to create a building
    floor = Group([floor_glass, floor_facade])
    building = LinearPattern(floor, direction=[0, 0, 1], number_of_elements=number_of_floors, spacing=3)

    return GeometryResult(building)
```

""", visible=Lookup('design.code'))

calculate_text1 = Text("""
# Charts, plots and graphs

Use your preferred graphic library (such as Matplotlib,  Plotly and Seaborn, just to name a few) 
to plot results and other libraries like Pandas or Numpy to process your data.

In this example, we want to determine the minimum surface area for a rectangular box with a specified volume. This is
partially determined by visualizing the surface areas for a range of dimensions.

""")

calculate_text2 = Text("Set the ranges for the surface area investigation")

calculate_text3 = Text("""
The input fields:

```python
min_width = NumberField('Minimum width', min=1, default=1, suffix='m')
max_width = NumberField('Maximum width', min=2, default=10, suffix='m')
min_length = NumberField('Minimum length', min=1, default=1, suffix='m')
max_length = NumberField('Maximum length', min=2, default=10, suffix='m')
volume = NumberField('Volume', suffix='m³', min=10, default=50)
```
""", visible=Lookup('calculate.code'))

calculate_text4 = Text("""
This contour plot is created using ```plotly``` and ```numpy```.

The following equations were used to construct the surface plot:
$$
A(w,h,l)=2(w×h)+2(l×h)+2(w×l)
$$
and...
$$
V(w,h,l)=w×h×l
$$
to form the equation...
$$
A(w,l)=2(w×\\frac{V}{w×l})+2(l×\\frac{V}{w×l})+2(w×l)
$$

This was then incorporated in the method that visualizes the surface plot:

```python
@PlotlyAndDataView('Surface area plot', duration_guess=1)
def calculate_contour_plot(self, params, **kwargs):
    # create a range of values between the min and max
    width_array = np.linspace(params.min_width, params.max_width, 101)
    length_array = np.linspace(params.min_length, params.max_length, 101)
    [w, l] = np.meshgrid(length_array, width_array)
    
    # do the calculations
    h = params.volume / (w * l)
    surface_area = 2 * w * h + 2 * l * h + 2 * w * l
    min_surface_area = np.min(np.min(surface_area))

    # create a DataItem for the dataview
    item = DataItem(
        f"Minimum surface area", min_surface_area, suffix='m²', number_of_decimals=1,
        subgroup=DataGroup(
            DataItem("Volume", volume, suffix='m³')
        )
    )
    
    # create a dictionary format of a Plotly visualization
    fig = {
        'data': [{
            'type': "surface",
            'x': width_array.tolist(),
            'y': length_array.tolist(),
            'z': surface_area.tolist()
        }]
    }

    return PlotlyAndDataResult(fig, data=DataGroup(item))
```
""", visible=Lookup('calculate.code'))

report_text1 = Text("""
# Reporting and templates

VIKTOR lets you generate custom documents based on your own Word or Excel templates.
""")

report_text2 = Text("""
**Note:** Press the *Generate certificate* button at the bottom-right corner to get your own VIKTOR certificate.
""")


report_text3 = Text("""
This certificate generator uses a Word template that has the keys {{name}}, {{score}} and {{date}} in the text.
The app takes the user's input, places it into the corresponding keys, and converts the document into a PDF.
 
""", visible=Lookup('report.code'))

report_text4 = Text(""" 
The input fields:
```python
your_name = TextField("Please enter your name")
your_score = NumberField("Give yourself a score", variant='slider', min=1, max=10, default=10)
date = DateField("Select a date")
```

The following function generates the certificate:
```python
@PDFView("PDF", duration_guess=10, update_label="Generate certificate")
def create_report(self, params, **kwargs) -> File:    
    progress_message("VIKTOR is generating your certificate!")

    # DateField returns a Python datetime object
    date = params.report.date.strftime("%d-%m-%Y") if params.report.date is not None else '-'
    components = [
        WordFileTag('name', params.your_name),
        WordFileTag('date', date),
        WordFileTag('score', params.your_score),
    ]

    with open(Path(__file__).parent / 'viktor_certificate.docx', 'rb') as r:
        report = render_word_file(r, components)

    with report.open_binary() as r:
        pdf_report = convert_word_to_pdf(r)      
    return PDFResult(file=pdf_report)
```    
""", visible=Lookup('report.code'))
