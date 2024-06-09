package main

import (
	"fmt"
	"image/color"
	"log"
	"os"
	"strconv"

	"github.com/fogleman/gg"
)

// DrawDigit draws a Cistercian digit at a specific quadrant
func DrawDigit(dc *gg.Context, digit, quadrant int) {
	const size = 256
	const half = size / 2
	const quarter = size / 4
	const eighth = size / 8
	dc.SetLineWidth(8)
	dc.SetLineCap(gg.LineCapRound)

	switch quadrant {
	case 1:
		// Top-right quadrant (units)
		if digit == 1 || digit == 2 || digit == 3 {
			dc.DrawLine(half, eighth, half, quarter)
		}
		if digit == 2 || digit == 3 {
			dc.DrawLine(half, eighth, half+eighth, eighth)
		}
		if digit == 4 || digit == 5 || digit == 6 {
			dc.DrawLine(half, quarter, half, half)
		}
		if digit == 5 || digit == 6 {
			dc.DrawLine(half, quarter, half+eighth, quarter)
		}
		if digit == 7 || digit == 8 || digit == 9 {
			dc.DrawLine(half+eighth, eighth, half+eighth, quarter)
		}
		if digit == 8 || digit == 9 {
			dc.DrawLine(half, eighth, half+eighth, quarter)
		}
	case 2:
		// Top-left quadrant (tens)
		if digit == 1 || digit == 2 || digit == 3 {
			dc.DrawLine(half, eighth, half, quarter)
		}
		if digit == 2 || digit == 3 {
			dc.DrawLine(half, eighth, half-eighth, eighth)
		}
		if digit == 4 || digit == 5 || digit == 6 {
			dc.DrawLine(half, quarter, half, half)
		}
		if digit == 5 || digit == 6 {
			dc.DrawLine(half, quarter, half-eighth, quarter)
		}
		if digit == 7 || digit == 8 || digit == 9 {
			dc.DrawLine(half-eighth, eighth, half-eighth, quarter)
		}
		if digit == 8 || digit == 9 {
			dc.DrawLine(half, eighth, half-eighth, quarter)
		}
	case 3:
		// Bottom-right quadrant (hundreds)
		if digit == 1 || digit == 2 || digit == 3 {
			dc.DrawLine(half, size-eighth, half, size-quarter)
		}
		if digit == 2 || digit == 3 {
			dc.DrawLine(half, size-eighth, half+eighth, size-eighth)
		}
		if digit == 4 || digit == 5 || digit == 6 {
			dc.DrawLine(half, size-quarter, half, half)
		}
		if digit == 5 || digit == 6 {
			dc.DrawLine(half, size-quarter, half+eighth, size-quarter)
		}
		if digit == 7 || digit == 8 || digit == 9 {
			dc.DrawLine(half+eighth, size-eighth, half+eighth, size-quarter)
		}
		if digit == 8 || digit == 9 {
			dc.DrawLine(half, size-eighth, half+eighth, size-quarter)
		}
	case 4:
		// Bottom-left quadrant (thousands)
		if digit == 1 || digit == 2 || digit == 3 {
			dc.DrawLine(half, size-eighth, half, size-quarter)
		}
		if digit == 2 || digit == 3 {
			dc.DrawLine(half, size-eighth, half-eighth, size-eighth)
		}
		if digit == 4 || digit == 5 || digit == 6 {
			dc.DrawLine(half, size-quarter, half, half)
		}
		if digit == 5 || digit == 6 {
			dc.DrawLine(half, size-quarter, half-eighth, size-quarter)
		}
		if digit == 7 || digit == 8 || digit == 9 {
			dc.DrawLine(half-eighth, size-eighth, half-eighth, size-quarter)
		}
		if digit == 8 || digit == 9 {
			dc.DrawLine(half, size-eighth, half-eighth, size-quarter)
		}
	}
}

func DrawCistercianNumber(dc *gg.Context, num int) {
	const size = 256
	const half = size / 2

	// Draw the main vertical line
	dc.DrawLine(half, 0, half, size)
	dc.SetLineWidth(10)
	dc.Stroke()

	// Extract digits
	thousands := num / 1000
	hundreds := (num % 1000) / 100
	tens := (num % 100) / 10
	units := num % 10

	// Draw each digit in its respective quadrant
	if thousands > 0 {
		DrawDigit(dc, thousands, 4)
	}
	if hundreds > 0 {
		DrawDigit(dc, hundreds, 3)
	}
	if tens > 0 {
		DrawDigit(dc, tens, 2)
	}
	if units > 0 {
		DrawDigit(dc, units, 1)
	}
}

func main() {
	if len(os.Args) != 2 {
		log.Fatalf("Usage: %s <number>", os.Args[0])
	}

	num, err := strconv.Atoi(os.Args[1])
	if err != nil || num < 0 || num > 9999 {
		log.Fatalf("Please provide a valid number between 0 and 9999.")
	}

	const width = 256
	const height = 256

	dc := gg.NewContext(width, height)
	dc.SetColor(color.White)
	dc.Clear()
	dc.SetColor(color.Black)

	DrawCistercianNumber(dc, num)

	outputFile := "cistercian_number.png"
	if err := dc.SavePNG(outputFile); err != nil {
		log.Fatalf("Could not save PNG: %v", err)
	}

	fmt.Printf("Cistercian numeral image saved to %s\n", outputFile)
}
