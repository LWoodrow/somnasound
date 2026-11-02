"""Somnasound first mechanical floorplan.

Run with FreeCADCmd 1.1.4.  This is a review model, not production CAD.
All values are in mm and are intentionally gathered below for quick revision after
the full-size physical mock-up and real component selection.
"""
import os
import FreeCAD as App
import Part
import Import

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "output")
os.makedirs(OUT, exist_ok=True)

# --- Provisional master dimensions -------------------------------------------------
WIDTH = 220.0
PANEL_HEIGHT = 132.0
PANEL_THICKNESS = 4.0
TILT_DEG = -15.0              # top leans toward the rear (+Y)
BASE_WIDTH = 236.0
BASE_DEPTH = 142.0
BASE_HEIGHT = 7.0
BOARD_WIDTH = 200.0
BOARD_DEPTH = 112.0
BOARD_THICKNESS = 1.6

doc = App.newDocument("Somnasound_Enclosure_Draft")

params = doc.addObject("Spreadsheet::Sheet", "Parameters")
for cell, value, label in [
    ("A1", "Somnasound enclosure draft 0.1", ""),
    ("A3", "Front width", ""), ("B3", str(WIDTH), "mm"),
    ("A4", "Front height", ""), ("B4", str(PANEL_HEIGHT), "mm"),
    ("A5", "Front tilt", ""), ("B5", str(abs(TILT_DEG)), "degrees"),
    ("A6", "Board envelope", ""), ("B6", "200 x 112 x 1.6", "mm"),
    ("A8", "Status", ""), ("B8", "MECHANICAL REVIEW ONLY", ""),
]:
    params.set(cell, value)
    if label:
        params.set(cell.replace("A", "C").replace("B", "C"), label)

def feature(name, label, shape, color, transparency=0):
    obj = doc.addObject("Part::Feature", name)
    obj.Label = label
    obj.Shape = shape
    # FreeCADCmd can run without a GUI ViewObject.  Colours are a convenience
    # for the desktop review model, never a prerequisite for regeneration.
    if obj.ViewObject:
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.Transparency = transparency
    return obj

tilt = App.Rotation(App.Vector(1, 0, 0), TILT_DEG)
front_origin = App.Vector(0, 0, BASE_HEIGHT)

def panel_to_world(shape):
    shape.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), TILT_DEG)
    shape.translate(front_origin)
    return shape

# Base: slightly wider than the front, intentionally simple in this first pass.
base = Part.makeBox(BASE_WIDTH, BASE_DEPTH, BASE_HEIGHT, App.Vector(-BASE_WIDTH / 2, -8, 0))
feature("Base", "Wider rubber-foot base envelope", base, (0.10, 0.10, 0.10))

# Front fascia with the display, sensor detail, button and wheel apertures.
front = Part.makeBox(WIDTH, PANEL_THICKNESS, PANEL_HEIGHT, App.Vector(-WIDTH / 2, 0, 0))
# Display opening: final exact opening waits for the selected red PMOLED drawing.
front = front.cut(Part.makeBox(92, 12, 50, App.Vector(-46, -4, 61)))
# Dark horizontal sensor detail: clear thermal aperture at left, unpainted radar radome at right.
front = front.cut(Part.makeBox(52, 12, 8, App.Vector(-26, -4, 116)))
front = front.cut(Part.makeBox(11, 12, 8, App.Vector(-26, -4, 116)))
# Lower controls: two wheel bores and three compact tactile-button openings.
for x in (-55, 55):
    front = front.cut(Part.makeCylinder(16, 12, App.Vector(x, -4, 27), App.Vector(0, 1, 0)))
for x in (-28, 0, 28):
    front = front.cut(Part.makeBox(16, 12, 8, App.Vector(x - 8, -4, 45)))
front = panel_to_world(front)
feature("FrontFascia", "ASA first-run / future CNC front interface", front, (0.055, 0.055, 0.055))

# Display plane and sensor detail are review-only visual/interface objects.
display = Part.makeBox(88, 1.0, 46, App.Vector(-44, -0.5, 63))
display = panel_to_world(display)
feature("DisplayEnvelope", "Red PMOLED mechanical envelope (provisional)", display, (0.45, 0.015, 0.015), 15)
sensor = Part.makeBox(48, 1.2, 5.5, App.Vector(-24, -0.7, 117.2))
sensor = panel_to_world(sensor)
feature("SensorDetail", "Thermal aperture + radar radome envelope", sensor, (0.16, 0.16, 0.16))

# Rear service spine, parallel to front (same tilt), shallow by intention.
spine = Part.makeBox(202, 38, 118, App.Vector(-101, 27, 0))
# Lower downward-facing connection bay; actual terminal geometry deliberately deferred.
spine = spine.cut(Part.makeBox(158, 46, 39, App.Vector(-79, 23, 0)))
# Top protected well for microSD and black rocker.
spine = spine.cut(Part.makeBox(72, 14, 18, App.Vector(-36, 48, 94)))
spine = panel_to_world(spine)
feature("RearServiceSpine", "Shallow rear-parallel service/power spine", spine, (0.075, 0.075, 0.075))

# Board envelope uses the KiCad study dimensions and is deliberately visible.
board = Part.makeBox(BOARD_WIDTH, BOARD_THICKNESS, BOARD_DEPTH, App.Vector(-BOARD_WIDTH / 2, 7, 7))
board = panel_to_world(board)
feature("MainBoardEnvelope", "200 x 112 mm main PCB envelope", board, (0.05, 0.33, 0.10), 55)

# Rear-only fastener / brass-insert concept; no holes pass through the visible front.
for x in (-88, 88):
    for z in (18, 103):
        insert = Part.makeCylinder(3.1, 7, App.Vector(x, 41, z), App.Vector(0, 1, 0))
        insert = panel_to_world(insert)
        feature("Insert_%s_%s" % (str(x).replace('-', 'N'), z), "Rear-installed brass insert envelope", insert, (0.62, 0.43, 0.12))

# Keep the connection-bay and cooling openings conspicuous in review exports.
bay = Part.makeBox(150, 28, 31, App.Vector(-75, 23, 4))
bay = panel_to_world(bay)
feature("ConnectionBayEnvelope", "Downward-facing 24 V + four speaker terminals envelope", bay, (0.15, 0.20, 0.38), 65)

doc.recompute()

native = os.path.join(OUT, "somnasound-enclosure-draft.FCStd")
step = os.path.join(OUT, "somnasound-enclosure-draft.step")
stl = os.path.join(OUT, "somnasound-enclosure-draft.stl")
doc.saveAs(native)

# Exchange only the physical architecture, excluding review-only transparent envelopes.
export_objs = [doc.Base, doc.FrontFascia, doc.RearServiceSpine]
Import.export(export_objs, step)
Part.export(export_objs, stl)
print("Created:")
for path in (native, step, stl):
    print(path)
