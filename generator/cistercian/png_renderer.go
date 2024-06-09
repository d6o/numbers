package main

import (
	"fmt"
	"github.com/fogleman/gg"
	"image/color"
)

type PNGRenderer struct {
	Value  int
	Stroke int
	Color  string
}

func parseColor(s string) (color.Color, error) {
	var r, g, b, a uint8
	if _, err := fmt.Sscanf(s, "#%02x%02x%02x", &r, &g, &b); err != nil {
		return nil, err
	}
	a = 255
	return color.RGBA{r, g, b, a}, nil
}

func (p PNGRenderer) Render(filename string) error {
	const width = 200
	const height = 280
	const padding = 10

	dc := gg.NewContext(width, height)

	lineColor, err := parseColor(p.Color)
	if err != nil {
		return err
	}
	dc.SetLineWidth(float64(p.Stroke))
	dc.SetColor(lineColor)

	ones := p.Value % 10
	tens := p.Value / 10 % 10
	hundreds := p.Value / 100 % 10
	thousands := p.Value / 1000 % 10

	// Pre-define anchor points
	p0 := Point{padding, padding}
	p1 := Point{width / 2, padding}
	p2 := Point{width - padding, padding}

	p3 := Point{padding, height / 3}
	p4 := Point{width / 2, height / 3}
	p5 := Point{width - padding, height / 3}

	p6 := Point{padding, height / 3 * 2}
	p7 := Point{width / 2, height / 3 * 2}
	p8 := Point{width - padding, height / 3 * 2}

	p9 := Point{padding, height - padding}
	p10 := Point{width / 2, height - padding}
	p11 := Point{width - padding, height - padding}

	// Draw the vertical line
	dc.DrawLine(float64(p1.x), float64(p1.y), float64(p1.x), float64(p11.y))
	dc.Stroke()

	drawDigit := func(value int, xCoords []int, yCoords []int) {
		if value != 6 && value != 0 {
			dc.NewSubPath()
			for i := 0; i < len(xCoords); i++ {
				if i == 0 {
					dc.MoveTo(float64(xCoords[i]), float64(yCoords[i]))
				} else {
					dc.LineTo(float64(xCoords[i]), float64(yCoords[i]))
				}
			}
			dc.Stroke()
		}
	}

	drawSegment := func(value int, segmentLines map[int][][]Point) {
		for segment, points := range segmentLines {
			if value == segment {
				for _, line := range points {
					dc.DrawLine(float64(line[0].x), float64(line[0].y), float64(line[1].x), float64(line[1].y))
					dc.Stroke()
				}
			}
		}
	}

	segmentLines := map[int][][]Point{
		6:    {{p2, p5}},
		60:   {{p0, p3}},
		600:  {{p8, p11}},
		6000: {{p6, p9}},
	}

	drawSegment(ones, segmentLines)
	drawSegment(tens, segmentLines)
	drawSegment(hundreds, segmentLines)
	drawSegment(thousands, segmentLines)

	digitLines := map[int][][]int{
		1:  {{p10.x, p1.x, p2.x}, {p10.y, p1.y, p2.y}},
		2:  {{p10.x, p1.x, p4.x, p5.x}, {p10.y, p1.y, p4.y, p5.y}},
		3:  {{p10.x, p1.x, p5.x}, {p10.y, p1.y, p5.y}},
		4:  {{p10.x, p1.x, p4.x, p2.x}, {p10.y, p1.y, p4.y, p2.y}},
		5:  {{p10.x, p1.x, p2.x, p4.x}, {p10.y, p1.y, p2.y, p4.y}},
		7:  {{p10.x, p1.x, p2.x, p5.x}, {p10.y, p1.y, p2.y, p5.y}},
		8:  {{p10.x, p1.x, p4.x, p5.x, p2.x}, {p10.y, p1.y, p4.y, p5.y, p2.y}},
		9:  {{p10.x, p1.x, p2.x, p5.x, p4.x}, {p10.y, p1.y, p2.y, p5.y, p4.y}},
		20: {{p1.x, p10.x, p4.x, p3.x}, {p1.y, p10.y, p4.y, p3.y}},
		30: {{p1.x, p10.x, p3.x}, {p1.y, p10.y, p3.y}},
		40: {{p1.x, p10.x, p4.x, p0.x}, {p1.y, p10.y, p4.y, p0.y}},
		50: {{p1.x, p10.x, p0.x, p4.x}, {p1.y, p10.y, p0.y, p4.y}},
		70: {{p1.x, p10.x, p0.x, p3.x}, {p1.y, p10.y, p0.y, p3.y}},
		80: {{p1.x, p10.x, p4.x, p3.x, p0.x}, {p1.y, p10.y, p4.y, p3.y, p0.y}},
		90: {{p1.x, p10.x, p0.x, p3.x, p4.x}, {p1.y, p10.y, p0.y, p3.y, p4.y}},
	}

	if ones > 1 {
		drawDigit(ones, digitLines[ones][0], digitLines[ones][1])
	}
	if tens > 1 {
		drawDigit(tens*10, digitLines[tens*10][0], digitLines[tens*10][1])
	}
	if hundreds > 1 {
		drawDigit(hundreds*100, digitLines[hundreds*100][0], digitLines[hundreds*100][1])
	}
	if thousands > 1 {
		drawDigit(thousands*1000, digitLines[thousands*1000][0], digitLines[thousands*1000][1])
	}

	err = dc.SavePNG("/Users/diegosiqueira/Playground/numbers/aaaaaa.png")
	if err != nil {
		return err
	}

	return nil
}
