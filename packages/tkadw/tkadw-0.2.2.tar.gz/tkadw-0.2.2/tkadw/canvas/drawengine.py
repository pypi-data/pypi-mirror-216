from tkinter import Canvas

def rounded_rectangle(size, radius, fill):
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius, fill)
    return img

poly = """
# poly.tcl

proc poly_round {win outline fill args} {
    if {[llength $args] % 3 != 0 || [llength $args] < 9} {
        error "wrong # args: should be \"poly_round\
                win outline fill x1 y1 d1 x2 y2 d2 x3 y3 d3 ?...?\""
    }

    # Determine the tag to use.
    if {![info exists ::poly_next_id]} {
        set ::poly_next_id 1
    }
    set tag poly#$::poly_next_id
    incr ::poly_next_id

    # Filter out illegal circles and collinear points.
    set pts [list]
    lassign [lrange $args 0 4] Ux Uy d Vx Vy
    foreach {d Wx Wy} [concat [lrange $args 5 end] [lrange $args 0 4]] {
        set test [expr {$Ux * ($Vy - $Wy) - $Vx * ($Uy - $Wy) +
                $Wx * ($Uy - $Vy)}]
        if {($d > 0) && $test != 0} {
            lappend pts $Vx $Vy $d $test
            lassign [list $Wx $Wy $Vx $Vy] Vx Vy Ux Uy
        } else {
            lassign [list $Wx $Wy] Vx Vy
        }
    }

    # V    C    T   W
    #  *---*----*-+-*-- Given: U, V, W, d
    #  |\ /    /|_|     Find:  S, E, T
    #  | *B   / |
    #  |/ \  /  |       The length of ES and ET each is d.
    # A*   \/   |
    #  |   /\   |       VB bisects angle UVW.  SE _|_ VU; TE _|_ VW.
    #  |  /  \  |       B is halfway between A and C.
    #  | /    \ |       Angles UVW and SET are not necessarily right.
    #  |/      \|       The length of AV and CV each is 1.
    # S*-+------*E
    #  |_|       \      The new polygon is along USTW.
    # U*          \     The new arc has center E, radius d, and angle SET, and
    #  |           \    it is tangential to VU at S and VW at T.

    # Calculate new polygon vertices and create arcs.
    set coords [list]
    lassign [lrange $pts 0 5] Ux Uy d test Vx Vy
    foreach {d test Wx Wy} [concat [lrange $pts 6 end] [lrange $pts 0 5]] {
        # Find A and C.
        foreach {pt x y} [list A $Ux $Uy C $Wx $Wy] {
            set      k [expr {sqrt(($Vx - $x) ** 2 + ($Vy - $y) ** 2)}]
            set ${pt}x [expr {($x - $Vx) / $k + $Vx}]
            set ${pt}y [expr {($y - $Vy) / $k + $Vy}]
        }

        # Find B.
        set Bx [expr {($Ax + $Cx) / 2.0}]
        set By [expr {($Ay + $Cy) / 2.0}]

        # Find the parameters for lines VB and VW.
        foreach {pt x y} [list B $Bx $By W $Wx $Wy] {
            set       k [expr {sqrt(($Vx - $x) ** 2 + ($Vy - $y) ** 2)}]
            set V${pt}a [expr {+($Vy - $y) / $k}]
            set V${pt}b [expr {-($Vx - $x) / $k}]
            set V${pt}c [expr {($Vx * $y - $Vy * $x) / $k}]
        }

        # Find point E.
        set sign [expr {$test < 0 ? -1 : +1}]
        set  k [expr {$VWa * $VBb - $VWb * $VBa}]
        set Ex [expr {(+$VWb * $VBc - ($VWc - $d * $sign) * $VBb) / $k}]
        set Ey [expr {(-$VWa * $VBc + ($VWc - $d * $sign) * $VBa) / $k}]

        # Find tangent points S and T.
        foreach {pt x y} [list S $Ux $Uy T $Wx $Wy] {
            set      k [expr {($Vx - $x) ** 2 + ($Vy - $y) ** 2}]
            set ${pt}x [expr {($Ex * ($Vx - $x) ** 2 + ($Vy - $y) *
                              ($Ey * ($Vx - $x) - $Vx * $y + $Vy * $x)) / $k}]
            set ${pt}y [expr {($Ex * ($Vx - $x) * ($Vy - $y) +
                              ($Ey * ($Vy - $y) ** 2 + ($Vx - $x) *
                              ($Vx * $y - $Vy * $x))) / $k}]
        }

        # Find directions for lines ES and ET.
        foreach {pt x y} [list S $Sx $Sy T $Tx $Ty] {
            set E${pt}d [expr {atan2($Ey - $y, $x - $Ex)}]
        }

        # Find start and extent directions.
        if {$ESd < 0 && $ETd > 0} {
            set start  [expr {180 / acos(-1) * $ETd}]
            set extent [expr {180 / acos(-1) * ($ESd - $ETd)}]
            if {$sign > 0} {
                set extent [expr {$extent + 360}]
            }
        } else {
            set start  [expr {180 / acos(-1) * $ESd}]
            set extent [expr {180 / acos(-1) * ($ETd - $ESd)}]
            if {$sign < 0 && $ESd > 0 && $ETd < 0} {
                set extent [expr {$extent + 360}]
            }
        }

        # Draw arc.
        set opts [list                             \
                [expr {$Ex - $d}] [expr {$Ey - $d}]\
                [expr {$Ex + $d}] [expr {$Ey + $d}]\
                -start $start -extent $extent]
        $win create arc {*}$opts -style pie -tags [list $tag pie]
        $win create arc {*}$opts -style arc -tags [list $tag arc]

        # Draw border line.
        if {[info exists prevx]} {
            $win create line $prevx $prevy $Sx $Sy -tags [list $tag line]
        } else {
            lassign [list $Sx $Sy] firstx firsty
        }
        lassign [list $Tx $Ty] prevx prevy

        # Remember coordinates for polygon.
        lappend coords $Sx $Sy $Tx $Ty

        # Rotate vertices.
        lassign [list $Wx $Wy $Vx $Vy] Vx Vy Ux Uy
    }

    # Draw final border line.
    $win create line $prevx $prevy $firstx $firsty -tags [list $tag line]

    # Draw fill polygon.
    $win create polygon {*}$coords -tags [list $tag poly]

    # Configure colors.
    $win itemconfigure $tag&&(poly||pie) -fill $fill
    $win itemconfigure $tag&&pie         -outline ""
    $win itemconfigure $tag&&line        -fill $outline -capstyle round
    $win itemconfigure $tag&&arc         -outline $outline

    # Set proper stacking order.
    $win raise $tag&&poly
    $win raise $tag&&pie
    $win raise $tag&&(line||arc)

    return $tag
}
       """

poly2 = """
 #----------------------------------------------------------------------
 #
 # RoundPoly -- Draw a polygon with rounded corners in the canvas, based
 # off of ideas and code from "Drawing rounded rectangles"
 #
 # Parameters:
 #       w - Path name of the canvas
 #       xy - list of coordinates of the vertices of the polygon
 #       radii - list of radius of the bend each each vertex
 #       args - Other args suitable to a 'polygon' item on the canvas
 #
 # Results:
 #       Returns the canvas item number of the rounded polygon.
 #
 # Side effects:
 #       Creates a rounded polygon in the canvas.
 #
 #----------------------------------------------------------------------
 
 proc RoundPoly {w xy radii args} {
    set lenXY [llength $xy]
    set lenR [llength $radii]
    if {$lenXY != 2 * $lenR} {
        error "wrong number of vertices and radii"
    }
 
    # Walk down vertices keeping previous, current and next
    lassign [lrange $xy end-1 end] x0 y0
    lassign $xy x1 y1
    eval lappend xy [lrange $xy 0 1]
    set knots {}                                ;# These are the control points
 
    for {set i 0} {$i < $lenXY} {incr i 2} {
        set radius [lindex $radii [expr {$i/2}]]
        set r [winfo pixels $w $radius]
 
        lassign [lrange $xy [expr {$i + 2}] [expr {$i + 3}]] x2 y2
        set z [_RoundPoly2 $x0 $y0 $x1 $y1 $x2 $y2 $r]
        eval lappend knots $z
 
        lassign [list $x1 $y1] x0 y0           ;# Current becomes previous
        lassign [list $x2 $y2] x1 y1           ;# Next becomes current
    }
    set n [eval $w create polygon $knots -smooth 1 $args]
    return $n
 }
 proc _RoundPoly2 {x0 y0 x1 y1 x2 y2 radius} {
    set d [expr { 2 * $radius }]
    set maxr 0.75
 
    set v1x [expr {$x0 - $x1}]
    set v1y [expr {$y0 - $y1}]
    set v2x [expr {$x2 - $x1}]
    set v2y [expr {$y2 - $y1}]
 
    set vlen1 [expr {sqrt($v1x*$v1x + $v1y*$v1y)}]
    set vlen2 [expr {sqrt($v2x*$v2x + $v2y*$v2y)}]
    if {$d > $maxr * $vlen1} {
        set d [expr {$maxr * $vlen1}]
    }
    if {$d > $maxr * $vlen2} {
        set d [expr {$maxr * $vlen2}]
    }
 
    lappend xy [expr {$x1 + $d * $v1x/$vlen1}] [expr {$y1 + $d * $v1y/$vlen1}]
    lappend xy $x1 $y1
    lappend xy [expr {$x1 + $d * $v2x/$vlen2}] [expr {$y1 + $d * $v2y/$vlen2}]
 
    return $xy
 }

"""


class AdwDrawEngine(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def win32_high_dpi(self):
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(2)

    def draw_gradient(self, color1, color2, type="x"):
        self.tk.eval("""
  proc + {n1 n2} {
    expr {$n1 + $n2}
  }
  proc - {n1 n2} {
    expr {$n1 - $n2}
  }
  proc * {n1 n2} {
    expr {$n1 * $n2}
  }
  proc / {n1 n2} {
    expr {$n1 / $n2}
  }
  proc toInt {n} {
    expr int($n)
  }
  
  proc drawGradient {win type col1Str col2Str} {
    $win delete gradient
    
    set width [winfo width $win]
    set height [winfo height $win]
    
    lassign [winfo rgb $win $col1Str] r1 g1 b1
    lassign  [winfo rgb $win $col2Str] r2 g2 b2
    set rRange [- $r2.0 $r1]
    set gRange [- $g2.0 $g1]
    set bRange [- $b2.0 $b1]
  
    if {$type == "x"} {
      set rRatio [/ $rRange $width]
      set gRatio [/ $gRange $width]
      set bRatio [/ $bRange $width]
    
      for {set x 0} {$x < $width} {incr x} {
        set nR [toInt [+ $r1 [* $rRatio $x]]]
        set nG [toInt [+ $g1 [* $gRatio $x]]]
        set nB [toInt [+ $b1 [* $bRatio $x]]]
  
        set col [format {%4.4x} $nR]
        append col [format {%4.4x} $nG]
        append col [format {%4.4x} $nB]
        $win create line $x 0 $x $height -tags gradient -fill #${col}
      }
    } else {
      set rRatio [/ $rRange $height]
      set gRatio [/ $gRange $height]
      set bRatio [/ $bRange $height]
  
      for {set y 0} {$y < $height} {incr y} {
        set nR [toInt [+ $r1 [* $rRatio $y]]]
        set nG [toInt [+ $g1 [* $gRatio $y]]]
        set nB [toInt [+ $b1 [* $bRatio $y]]]
  
        set col [format {%4.4x} $nR]
        append col [format {%4.4x} $nG]
        append col [format {%4.4x} $nB]
        $win create line 0 $y $width $y -tags gradient -fill #${col}
      }
    }
    return $win
  }
        """)

        self.tk.call("drawGradient", self._w, type, color1, color2)

    def create_round_rectangle(self, x1, y1, x2, y2, radius: float = 5, width=2, fill="white", outline="black"):
        # 自研
        _radius = radius*2
        nw = self.create_arc(x1, y1, x1+_radius, y1+_radius, start=90, extent=90, width=width, fill=fill,
                        outline=outline)  # ⌜ north | west
        sw = self.create_arc(x1, y2, x1+_radius, y2-_radius, start=180, extent=90, width=width, fill=fill,
                        outline=outline)  # ⌞ south | wast
        ne = self.create_arc(x2-_radius, y1, x2, y1+_radius, start=0, extent=90, width=width, fill=fill,
                        outline=outline)  # ⌝ north | east
        se = self.create_arc(x2-_radius, y2, x2, y2-_radius, start=270, extent=90, width=width, fill=fill,
                        outline=outline)  # ⌟ south | east

        w = self.create_line(x1, y1+_radius/2, x1, y2-_radius/2, width=width, fill=outline)  # | left
        n = self.create_line(x1+_radius/2, y1, x2-_radius/2, y1, width=width, fill=outline)  # —— up
        e = self.create_line(x2, y1+_radius/2, x2, y2-_radius/2, width=width, fill=outline)  # | right
        s = self.create_line(x1+_radius/2, y2, x2-_radius/2, y2, width=width, fill=outline)  # —— down

        top = self.create_rectangle(x1+_radius/2-width, y1+width/2, x2-_radius/2+width, y1+_radius/2, fill=fill,
                                    width=0)  # ▭ top

        center = self.create_rectangle(x1+width/2, y1+_radius/2-width, x2-width/2, y2-_radius/2+width, fill=fill,
                                       width=0)  # ▭ center

        bottom = self.create_rectangle(x1+_radius/2-width, y2-_radius/2, x2-_radius/2+width, y2-width/2, fill=fill,
                                       width=0)  # ▭ bottom

        return {
            "nw": nw, "sw": sw, "ne": ne, "se": se, "w": w, "n": n, "e": e, "s": s,
            "top": top, "center": center, "bottom": bottom
                }

    create_round_rect = create_round_rectangle

    def create_round_rectangle2(self, x0, y0, x3, y3, radius, *args, **kwargs):
        # wiki上
        self.tk.eval("""
#----------------------------------------------------------------------
#
# roundRect --
#
#       Draw a rounded rectangle in the canvas.
#
# Parameters:
#       w - Path name of the canvas
#       x0, y0 - Co-ordinates of the upper left corner, in pixels
#       x3, y3 - Co-ordinates of the lower right corner, in pixels
#       radius - Radius of the bend at the corners, in any form
#                acceptable to Tk_GetPixels
#       args - Other args suitable to a 'polygon' item on the canvas
#
# Results:
#       Returns the canvas item number of the rounded rectangle.
#
# Side effects:
#       Creates a rounded rectangle as a smooth polygon in the canvas.
#
#----------------------------------------------------------------------

proc roundRect { w x0 y0 x3 y3 radius args } {

set r [winfo pixels $w $radius]
set d [expr { 2 * $r }]

# Make sure that the radius of the curve is less than 3/8
# size of the box!

set maxr 0.75

if { $d > $maxr * ( $x3 - $x0 ) } {
    set d [expr { $maxr * ( $x3 - $x0 ) }]
}
if { $d > $maxr * ( $y3 - $y0 ) } {
    set d [expr { $maxr * ( $y3 - $y0 ) }]
}

set x1 [expr { $x0 + $d }]
set x2 [expr { $x3 - $d }]
set y1 [expr { $y0 + $d }]
set y2 [expr { $y3 - $d }]

set cmd [list $w create polygon]
lappend cmd $x0 $y0
lappend cmd $x1 $y0
lappend cmd $x2 $y0
lappend cmd $x3 $y0
lappend cmd $x3 $y1
lappend cmd $x3 $y2
lappend cmd $x3 $y3
lappend cmd $x2 $y3
lappend cmd $x1 $y3
lappend cmd $x0 $y3
lappend cmd $x0 $y2
lappend cmd $x0 $y1
lappend cmd -smooth 1
return [eval $cmd $args]
}
        """)
        rect = self.tk.call("roundRect", self._w, x0, y0, x3, y3, radius)
        self.itemconfig(rect, *args, **kwargs)
        return rect

    create_round_rect2 = create_round_rectangle2

    def create_round_rectangle3(self, tag, x, y, width, height, radius, fill: str = "black", outline: str = "black", *args, **kwargs):
        # wiki上 圆角看起来更舒服
        self.tk.eval("""
proc roundRect2 {w L T Rad width height fill outline tag} {

  $w create oval $L $T [expr $L + $Rad] [expr $T + $Rad] -fill $fill -outline $outline -tag $tag
  $w create oval [expr $width-$Rad] $T $width [expr $T + $Rad] -fill $fill -outline $outline -tag $tag
  $w create oval $L [expr $height-$Rad] [expr $L+$Rad] $height -fill $fill -outline $outline -tag $tag
  $w create oval [expr $width-$Rad] [expr $height-$Rad] [expr $width] $height -fill $fill -outline $outline -tag $tag
  $w create rectangle [expr $L + ($Rad/2.0)] $T [expr $width-($Rad/2.0)] $height -fill $fill -outline $outline -tag $tag
  $w create rectangle $L [expr $T + ($Rad/2.0)] $width [expr $height-($Rad/2.0)] -fill $fill -outline $outline -tag $tag
}
            """)
        _rect = self.tk.call("roundRect2", self._w, x, y, radius, width, height, fill, outline, tag)
        self.itemconfig(_rect, *args, **kwargs)
        return _rect

    create_round_rect3 = create_round_rectangle3

    def create_round_rectangle4(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        _poly = self.create_polygon(points, **kwargs, smooth=True)

        return _poly

    create_round_rect4 = create_round_rectangle4

    def polygon_round(self, win, outline="black", fill="black", *args, **kwargs):
        self.tk.eval(poly)
        _poly = self.tk.eval(f"poly_round {win} {outline} {fill}")
        self.itemconfig(_poly, *args, **kwargs)
        return _poly

    poly_round = polygon_round

    def demo_polygon_round(self):
        demo = """
 package require Tcl 8.5
 package require Tk

 proc draw {win} {
     global demo

     set sharp_pts [list]
     set round_pts [list]
     for {set id 0} {$id < $demo(num_pts)} {incr id} {
         set x [expr {([lindex [$win coords vtx#$id] 0] +
                       [lindex [$win coords vtx#$id] 2]) / 2}]
         set y [expr {([lindex [$win coords vtx#$id] 1] +
                       [lindex [$win coords vtx#$id] 3]) / 2}]
         lappend sharp_pts $x $y
         lappend round_pts $x $y $demo(radius)
     }

     .c delete sharp_poly
     .c create polygon {*}$sharp_pts -outline gray50 -fill ""\
             -dash {6 5} -tags {sharp_poly}

     if {[info exists demo(tag)]} {
         .c delete $demo(tag)
     }
     set demo(tag) [poly_round .c $demo(outline) $demo(fill) {*}$round_pts]
     .c itemconfigure $demo(tag) -width $demo(thickness)

     .c raise vtx
 }

 proc down {win x y} {
     global demo

     $win dtag selected
     $win addtag selected withtag current
     $win raise current
     set demo(last_x) $x
     set demo(last_y) $y
 }
 
 proc move {win x y} {
     global demo

     if {[info exists demo(last_x)]} {
         $win move selected\
                 [expr {$x - $demo(last_x)}]\
                 [expr {$y - $demo(last_y)}]
         set demo(last_x) $x
         set demo(last_y) $y

         draw $win
     }
 }

 proc main {args} {
     global demo

     array set demo {
         num_pts 3       radius 20      thickness 1
         outline black   fill   white   background gray
         width   400     height 400
     }
     foreach {option value} $args {
         set option [regsub {^-} $option ""]
         if {![info exists demo($option)]} {
             puts "Options: -[join [array names demo] " -"]"
             exit
         } else {
             set demo([regsub {^-} $option ""]) $value
         }
     }

     canvas .c -width $demo(width) -height $demo(height) -highlightthickness 0\
             -background $demo(background)
     pack .c
     wm title . "Round Polygon Demo"
     wm resizable . 0 0

     set 2pi [expr {2 * acos(-1)}]
     set cx [expr {$demo(width)  / 2}]; set sx [expr {$demo(width)  * 3 / 8}]
     set cy [expr {$demo(height) / 2}]; set sy [expr {$demo(height) * 3 / 8}]
     for {set id 0} {$id < $demo(num_pts)} {incr id} {
         set x [expr {$cx + $sx * cos(($id + 0.5) * $2pi / $demo(num_pts))}]
         set y [expr {$cy - $sy * sin(($id + 0.5) * $2pi / $demo(num_pts))}]
         .c create oval [expr {$x - 3}] [expr {$y - 3}]\
                        [expr {$x + 3}] [expr {$y + 3}]\
                        -tags [list vtx vtx#$id] -fill brown
     }

     .c bind vtx <Any-Enter> {.c itemconfigure current -fill red}
     .c bind vtx <Any-Leave> {.c itemconfigure current -fill brown}
     .c bind vtx <ButtonPress-1> {down .c %x %y}
     .c bind vtx <ButtonRelease-1> {.c dtag selected}
     bind .c <B1-Motion> {move .c %x %y}

     focus .c
     draw .c
 }

 main

        """

        self.tk.eval(poly)
        self.tk.eval(demo)

    def create_svg_image(self, x, y, content: str, **kwargs):
        from tempfile import mkstemp
        from tksvg import SvgImage

        _, file = mkstemp(suffix=".svg")
        print(file)
        with open(file, "w") as f:
            f.write(content)
            f.close()
        image = SvgImage(file=file)

        i = self.create_image(x, y, image=image, **kwargs)

        return i

    def draw_copy_icon(self, __x, __y, size=10, padding=10, radius=18):
        _1 = self.create_round_rect4(__x, __y, __x+size*5, __y+size*5, radius)
        _2 = self.create_round_rect4(__x+padding, __y+padding, __x+size*5-padding, __y+size*5-padding, radius/2, fill="white")
        _3 = self.create_round_rect4(__x+size*2, __y+size*2, __x+size*7, __y+size*7, radius)
        _4 = self.create_round_rect4(__x+size*2+padding, __y+size*2+padding, __x+size*7-padding, __y+size*7-padding, radius/2, fill="white")
        return _1, _2, _3, _4

    def create_round_rectangle5(self, __x, __y, __width, __height, fill="black", radius=16, *args, **kwargs):
        from PIL import ImageTk
        img = rounded_rectangle((__width, __height), radius, fill, *args, **kwargs)
        photo = ImageTk.PhotoImage(img)

        return self.create_image(__x, __y, image=photo, anchor='nw')


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    canvas = AdwDrawEngine()

    #canvas.create_round_rect3(10, 15, 15, 150, 150, 50)
    canvas.create_round_rect4(160, 160, 300, 300, 50)

    canvas.create_round_rectangle5(50, 50, 100, 100, radius=16, fill="lightblue")

    #canvas.bind("<Configure>", lambda event: canvas.draw_gradient("#87e9bb", "#d3a6f5", "x"))

    canvas.pack(fill="both", expand="yes")

    root.mainloop()