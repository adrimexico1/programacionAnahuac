using DifferentialEquations
using Gtk.ShortNames
using CSV
using Random
using DataFrames: DataFrames

#Variable to save or not data (default true)
flag1 = true



################################################################################
# Interfaz section
################################################################################
# Environmental variable to allow Window decorations
ENV["gtk_csd"] = 0

global c1 = Canvas()
set_gtk_property!(c1, :visible, true)
set_gtk_property!(c1, :width_request, 300)
set_gtk_property!(c1, :height_request, 400)
global c2 = Canvas()
set_gtk_property!(c2, :visible, true)
set_gtk_property!(c2, :width_request, 300)
set_gtk_property!(c2, :height_request, 400)

w = Window("ACIDHYDROCHEM Simulator V 0.1")


################################################################################
#Grid section
################################################################################
# Grid for second layer (on F1)
g1 = Grid()
set_gtk_property!(g1, :column_homogeneous, true)
set_gtk_property!(g1, :row_homogeneous, false)
set_gtk_property!(g1, :column_spacing, 10)
set_gtk_property!(g1, :row_spacing, 10)
set_gtk_property!(g1, :margin_top, 15)
set_gtk_property!(g1, :margin_bottom, 15)
set_gtk_property!(g1, :margin_left, 15)
set_gtk_property!(g1, :margin_right, 15)

# # Grid to allocate bottons
ButtonsGrid = Grid()
set_gtk_property!(ButtonsGrid, :column_homogeneous, true)
set_gtk_property!(ButtonsGrid, :row_homogeneous, false)
set_gtk_property!(ButtonsGrid, :column_spacing, 10)
set_gtk_property!(ButtonsGrid, :row_spacing, 10)
set_gtk_property!(ButtonsGrid, :margin_top, 10)
set_gtk_property!(ButtonsGrid, :margin_bottom, 10)
set_gtk_property!(ButtonsGrid, :margin_left, 10)
set_gtk_property!(ButtonsGrid, :margin_right, 10)

# VariablesGrid
VariablesGrid = Grid()
set_gtk_property!(VariablesGrid, :column_homogeneous, true)
set_gtk_property!(VariablesGrid, :row_homogeneous, false)
set_gtk_property!(VariablesGrid, :column_spacing, 10)
set_gtk_property!(VariablesGrid, :row_spacing, 10)
set_gtk_property!(VariablesGrid, :margin_top, 10)
set_gtk_property!(VariablesGrid, :margin_bottom, 10)
set_gtk_property!(VariablesGrid, :margin_left, 10)
set_gtk_property!(VariablesGrid, :margin_right, 10)

LabelAuthorsGrid = Grid()
set_gtk_property!(LabelAuthorsGrid, :column_homogeneous, true)
set_gtk_property!(LabelAuthorsGrid, :row_homogeneous, false)
set_gtk_property!(LabelAuthorsGrid, :column_spacing, 10)
set_gtk_property!(LabelAuthorsGrid, :row_spacing, 10)
set_gtk_property!(LabelAuthorsGrid, :margin_top, 10)
set_gtk_property!(LabelAuthorsGrid, :margin_bottom, 10)
set_gtk_property!(LabelAuthorsGrid, :margin_left, 10)
set_gtk_property!(LabelAuthorsGrid, :margin_right, 10)

GraphGrid = Grid()
set_gtk_property!(GraphGrid, :column_homogeneous, true)
set_gtk_property!(GraphGrid, :row_homogeneous, false)
set_gtk_property!(GraphGrid, :column_spacing, 20)
set_gtk_property!(GraphGrid, :row_spacing, 10)
set_gtk_property!(GraphGrid, :margin_top, 10)
set_gtk_property!(GraphGrid, :margin_bottom, 10)
set_gtk_property!(GraphGrid, :margin_left, 10)
set_gtk_property!(GraphGrid, :margin_right, 10)

GraphLabelGrid = Grid()
set_gtk_property!(GraphLabelGrid, :column_homogeneous, true)
set_gtk_property!(GraphLabelGrid, :row_homogeneous, false)
set_gtk_property!(GraphLabelGrid, :column_spacing, 20)
set_gtk_property!(GraphLabelGrid, :row_spacing, 10)
set_gtk_property!(GraphLabelGrid, :margin_top, 10)
set_gtk_property!(GraphLabelGrid, :margin_bottom, 10)
set_gtk_property!(GraphLabelGrid, :margin_left, 10)
set_gtk_property!(GraphLabelGrid, :margin_right, 10)

################################################################################
# Frames Section
################################################################################
# F1 - First layer
F1 = Frame("ACIDHYDROCHEM Simulator V 0.1")
set_gtk_property!(F1, :width_request, 300)
set_gtk_property!(F1, :height_request, 500)

ButtonFrame = Frame()
set_gtk_property!(ButtonFrame, :width_request, 300)
set_gtk_property!(ButtonFrame, :height_request, 100)
set_gtk_property!(ButtonFrame, :margin_top, 5)
set_gtk_property!(ButtonFrame, :margin_bottom, 10)
set_gtk_property!(ButtonFrame, :margin_left, 10)
set_gtk_property!(ButtonFrame, :margin_right, 10)

VariablesFrame = Frame("Variables")
set_gtk_property!(VariablesFrame, :width_request, 150)
set_gtk_property!(VariablesFrame, :height_request, 50)
set_gtk_property!(VariablesFrame, :margin_top, 10)
set_gtk_property!(VariablesFrame, :margin_bottom, 5)
set_gtk_property!(VariablesFrame, :margin_left, 10)
set_gtk_property!(VariablesFrame, :margin_right, 10)

LabelAuthorsFrame = Frame()
set_gtk_property!(LabelAuthorsFrame, :width_request, 300)
set_gtk_property!(LabelAuthorsFrame, :height_request, 100)
set_gtk_property!(LabelAuthorsFrame, :margin_top, 220)
set_gtk_property!(LabelAuthorsFrame, :margin_bottom, 20)
set_gtk_property!(LabelAuthorsFrame, :margin_left, 10)
set_gtk_property!(LabelAuthorsFrame, :margin_right, 10)

GraphFrame = Frame("Graph")
set_gtk_property!(GraphFrame, :width_request, 300)
set_gtk_property!(GraphFrame, :height_request, 100)
set_gtk_property!(GraphFrame, :margin_top, 10)
set_gtk_property!(GraphFrame, :margin_bottom, 200)
set_gtk_property!(GraphFrame, :margin_left, 10)
set_gtk_property!(GraphFrame, :margin_right, 10)

GraphLabelFrame = Frame()
set_gtk_property!(GraphLabelFrame, :width_request, 300)
set_gtk_property!(GraphLabelFrame, :height_request, 100)
set_gtk_property!(GraphLabelFrame, :margin_top, 10)
set_gtk_property!(GraphLabelFrame, :margin_bottom, 200)
set_gtk_property!(GraphLabelFrame, :margin_left, 10)
set_gtk_property!(GraphLabelFrame, :margin_right, 10)

################################################################################
# Entry section
################################################################################
# Liquid ratio entry
LsrEntry = Entry()
set_gtk_property!(LsrEntry, :width_request, 5)
set_gtk_property!(LsrEntry, :height_request, 5)

# Solid ratio entry
Lsr2Entry = Entry()
set_gtk_property!(Lsr2Entry, :width_request, 5)
set_gtk_property!(Lsr2Entry, :height_request, 5)

# Sulfuric acid concentration
C_AcidEntry = Entry()
set_gtk_property!(C_AcidEntry, :width_request, 5)
set_gtk_property!(C_AcidEntry, :height_request, 5)
# Residence time entry
ResidenceEntry = Entry()
set_gtk_property!(ResidenceEntry, :width_request, 5)
set_gtk_property!(ResidenceEntry, :height_request, 5)

################################################################################
# Kinetic parameters and constants section
################################################################################
# Parameters
# Parameters
kH0 = 7.709e8
EH = 20301.9
βH = 1
R = 1.98
kX0 = 2.6e8
EX = 20312
βX = 0.15
T = 121.1 + 273.15
ρa = 1.84
################################################################################
# Button section
################################################################################

# Starting simulation button
Run = Button("Run")
set_gtk_property!(Run, :tooltip_text, "Press to run simulation")
signal_connect(Run, :clicked) do widget
	################################################################################
	# Variables section
	################################################################################
	global RLS1 = get_gtk_property(LsrEntry, :text, String)
	RLSkg = parse(Float64, RLS1)

	global RLS2 = get_gtk_property(Lsr2Entry, :text, String)
	RS = parse(Float64, RLS2)

	global C_ac1 = get_gtk_property(C_AcidEntry, :text, String)
	C_acid = parse(Float64, C_ac1)

	global t1 = get_gtk_property(ResidenceEntry, :text, String)
	t = parse(Float64, t1)


	################################################################################
	# Getting factor fi

	RL = RLSkg * ρa
	Φ = (RL / RS)


	################################################################################
	function acidH(du, u, p, t)
		# Resolucion de conjunto de ecuaciones diferenciales
		#Defining the function
		# Defining the differential equations of the process
		# du[1] = Hemicellulose concentration
		# du[2] = Xylose concentration
		# du[3] = Furural concentration

		du[1] = -kH0 * C_acid^βH * exp(-(EH / (R * T))) .* u[1] * Φ
		du[2] = kH0 * C_acid^βH * exp(-(EH / (R * T))) .* u[1] * Φ - kX0 * C_acid^βX * exp(-(EX / (R * T))) .* u[2] * Φ
		du[3] = kH0 * C_acid^βH * exp(-(EH / (R * T))) .* u[1] - kX0 * C_acid^βX * exp(-(EX / (R * T))) .* u[3] * 0.7 * Φ


	end

	# Solving differential equations through ODEProblem with Rosebrock23 method
	u0 = [70, 0, 0]
	tspan = (0.0, t)
	prob = ODEProblem(acidH, u0, tspan)
	global sol = solve(prob, Rosenbrock23(), saveat = 1)
	show(sol)

	set_gtk_property!(Grp, :sensitive, true)
	set_gtk_property!(New, :sensitive, true)
	set_gtk_property!(sd, :sensitive, true)
	set_gtk_property!(GraphFrame, :sensitive, true)
	set_gtk_property!(Run, :sensitive, false)
end

New = Button("New Simulation")
set_gtk_property!(New, :sensitive, false)
set_gtk_property!(New, :tooltip_text, "Press for a new simulation")
signal_connect(New, :clicked) do widget
	# Clear canvas section (Graph section)
	set_gtk_property!(c1, :visible, false)
	set_gtk_property!(c2, :visible, false)

	# Bottons configuration (active and inactive)
	set_gtk_property!(Run, :sensitive, true)
	set_gtk_property!(Grp, :sensitive, false)
	set_gtk_property!(New, :sensitive, false)
	set_gtk_property!(sd, :sensitive, false)
	set_gtk_property!(GraphFrame, :sensitive, false)

	# Entrys configuration in zero
	set_gtk_property!(LsrEntry, :text, "")
	set_gtk_property!(Lsr2Entry, :text, "")
	set_gtk_property!(C_AcidEntry, :text, "")
	set_gtk_property!(ResidenceEntry, :text, "")
end

Grp = Button("Graph")
set_gtk_property!(Grp, :sensitive, false)
set_gtk_property!(Grp, :tooltip_text, "Press to create graphics")
signal_connect(Grp, :clicked) do widget
	global sol
	global p1 = Winston.plot(sol.t, sol[1, :], sol[2, :], "r", sol[3, :], "g")
	title("Hemicellulose, xylose and degradation products concentration profile")
	xlabel("Residence time [min]")
	ylabel("Hemicelullose, xylose and PD concentration [g/L]")
	display(p1)

	set_gtk_property!(c1, :visible, true)
end

sd = Button("Save data")
set_gtk_property!(sd, :sensitive, false)
set_gtk_property!(sd, :tooltip_text, "Press to save data")
signal_connect(sd, :clicked) do widget
	dataCSV = DataFrames.DataFrame(
		time = sol.t,
		Hemicellulose = sol[1, :],
		Xylose = sol[2, :],
		Furfural = sol[3, :])

	# Print the data in form of table
	println(dataCSV)

	# Save data to excel
	if flag1 == true
		pathfile = save_dialog_native("Save as..", Null(), ("*.csv",))
		filename = string(pathfile, ".csv")
		CSV.write(filename, dataCSV)
	end
end

C = Button("Close")
set_gtk_property!(C, :tooltip_text, "Press to close")
signal_connect(C, :clicked) do widget
	destroy(w)
end

################################################################################
# Variables sections text
################################################################################
Lsr = Gtk.Label("Liquid fraction [L]")
Gtk.GAccessor.justify(Lsr, Gtk.GConstants.GtkJustification.CENTER)
set_gtk_property!(Lsr, :margin_top, 5)
set_gtk_property!(Lsr, :margin_bottom, 5)
set_gtk_property!(Lsr, :margin_left, 5)
set_gtk_property!(Lsr, :margin_right, 5)

Lsr2 = Label("Solid biomass [kg]")
Gtk.GAccessor.justify(Lsr, Gtk.GConstants.GtkJustification.CENTER)
set_gtk_property!(Lsr, :margin_top, 5)
set_gtk_property!(Lsr, :margin_bottom, 5)
set_gtk_property!(Lsr, :margin_left, 5)
set_gtk_property!(Lsr, :margin_right, 5)

Acid = Label("Acid concentration [% v/v]")
Gtk.GAccessor.justify(Acid, Gtk.GConstants.GtkJustification.CENTER)
set_gtk_property!(Acid, :margin_top, 5)
set_gtk_property!(Acid, :margin_bottom, 5)
set_gtk_property!(Acid, :margin_left, 5)
set_gtk_property!(Acid, :margin_right, 5)

Time = Label("Residence time [min]")
Gtk.GAccessor.justify(Time, Gtk.GConstants.GtkJustification.CENTER)
set_gtk_property!(Time, :margin_top, 5)
set_gtk_property!(Time, :margin_bottom, 5)
set_gtk_property!(Time, :margin_left, 5)
set_gtk_property!(Time, :margin_right, 5)

HemicelluloseColorLabel = Label("Black line = Hemicellulose")
Gtk.GAccessor.justify(HemicelluloseColorLabel, Gtk.GConstants.GtkJustification.CENTER)
set_gtk_property!(HemicelluloseColorLabel, :margin_top, 5)
set_gtk_property!(HemicelluloseColorLabel, :margin_bottom, 5)
set_gtk_property!(HemicelluloseColorLabel, :margin_left, 5)
set_gtk_property!(HemicelluloseColorLabel, :margin_right, 5)

XyloseColorLabel = Label("Red line = Xylose")
Gtk.GAccessor.justify(XyloseColorLabel, Gtk.GConstants.GtkJustification.CENTER)
set_gtk_property!(XyloseColorLabel, :margin_top, 5)
set_gtk_property!(XyloseColorLabel, :margin_bottom, 5)
set_gtk_property!(XyloseColorLabel, :margin_left, 5)
set_gtk_property!(XyloseColorLabel, :margin_right, 5)

FurfuralColorLabel = Label("Green line = Furfural")
Gtk.GAccessor.justify(FurfuralColorLabel, Gtk.GConstants.GtkJustification.CENTER)
set_gtk_property!(FurfuralColorLabel, :margin_top, 5)
set_gtk_property!(FurfuralColorLabel, :margin_bottom, 5)
set_gtk_property!(FurfuralColorLabel, :margin_left, 5)
set_gtk_property!(FurfuralColorLabel, :margin_right, 5)

GlucoseColorLabel = Label("Green line = Glucose concentration")
Gtk.GAccessor.justify(GlucoseColorLabel, Gtk.GConstants.GtkJustification.CENTER)
set_gtk_property!(GlucoseColorLabel, :margin_top, 5)
set_gtk_property!(GlucoseColorLabel, :margin_bottom, 5)
set_gtk_property!(GlucoseColorLabel, :margin_left, 5)
set_gtk_property!(GlucoseColorLabel, :margin_right, 5)

################################################################################
#  Authors section text
################################################################################
Authors =
	Label("M.Sc. Luis Antonio Velázquez Herrera\n Ph.D Leticia López Zamora\n PhD Eusebio Bolaños Reynoso")
Gtk.GAccessor.justify(Authors, Gtk.GConstants.GtkJustification.CENTER)

Institution =
	Label("Tecnológico Nacional de México/ Instituto Tecnológico de Orizaba, Veracruz")
Gtk.GAccessor.justify(Institution, Gtk.GConstants.GtkJustification.CENTER)

Posgrade = Gtk.Label("División de Estudios de Posgrado e Investigación")
Gtk.GAccessor.justify(Posgrade, Gtk.GConstants.GtkJustification.CENTER)
################################################################################
# Element Collocation
################################################################################

ButtonsGrid[1, 1] = New
ButtonsGrid[2, 1] = Grp
ButtonsGrid[3, 1] = sd
ButtonsGrid[4, 1] = C
ButtonsGrid[1:4, 2] = Run

LabelAuthorsGrid[1, 1] = Authors
LabelAuthorsGrid[1, 2] = Institution
LabelAuthorsGrid[1, 3] = Posgrade

VariablesGrid[1, 1] = Lsr
VariablesGrid[2, 1] = LsrEntry

VariablesGrid[1, 2] = Lsr2
VariablesGrid[2, 2] = Lsr2Entry

VariablesGrid[1, 3] = Acid
VariablesGrid[2, 3] = C_AcidEntry

VariablesGrid[1, 4] = Time
VariablesGrid[2, 4] = ResidenceEntry

GraphGrid[1, 1] = c1
GraphGrid[2, 1] = c2

GraphLabelGrid[1, 1] = HemicelluloseColorLabel
GraphLabelGrid[1, 2] = XyloseColorLabel
GraphLabelGrid[1, 3] = FurfuralColorLabel
GraphLabelGrid[1, 4] = GlucoseColorLabel

push!(F1, g1)

g1[1:4, 1] = ButtonFrame
g1[1, 2] = VariablesFrame
g1[2:4, 2:3] = GraphFrame
g1[1:4, 3] = LabelAuthorsFrame
g1[1, 3] = GraphLabelFrame

push!(ButtonFrame, ButtonsGrid)
push!(VariablesFrame, VariablesGrid)
push!(LabelAuthorsFrame, LabelAuthorsGrid)
push!(GraphFrame, GraphGrid)
push!(GraphLabelFrame, GraphLabelGrid)
push!(w, F1)
Gtk.showall(w)