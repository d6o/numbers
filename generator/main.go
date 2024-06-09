package main

import (
	"fmt"
	"image/color"
	"log"
	"os"
	"strconv"

	"github.com/fogleman/gg"
)

// DrawCistercianNumber draws a Cistercian numeral on the given context
func DrawCistercianNumber(dc *gg.Context, num int) {
	const size = 256
	const thickness = 10.0

	// Define the coordinates for the parts of the numeral
	var parts [16][4]float64

	parts[0] = [4]float64{size / 2, size / 2, size / 2, 0}     // Vertical center line
	parts[1] = [4]float64{size / 2, size / 2, size / 2, size}  // Vertical center line
	parts[2] = [4]float64{size / 2, size / 2, size, size / 2}  // Horizontal center line
	parts[3] = [4]float64{size / 2, size / 2, 0, size / 2}     // Horizontal center line
	parts[4] = [4]float64{size / 2, size / 2, size, 0}         // Top right
	parts[5] = [4]float64{size / 2, size / 2, 0, 0}            // Top left
	parts[6] = [4]float64{size / 2, size / 2, size, size}      // Bottom right
	parts[7] = [4]float64{size / 2, size / 2, 0, size}         // Bottom left
	parts[8] = [4]float64{size / 2, 0, size, 0}                // Top right short
	parts[9] = [4]float64{size / 2, 0, 0, 0}                   // Top left short
	parts[10] = [4]float64{size / 2, size, size, size}         // Bottom right short
	parts[11] = [4]float64{size / 2, size, 0, size}            // Bottom left short
	parts[12] = [4]float64{size / 2, size / 2, size, size / 2} // Horizontal center short right
	parts[13] = [4]float64{size / 2, size / 2, 0, size / 2}    // Horizontal center short left
	parts[14] = [4]float64{size / 2, 0, size / 2, size / 2}    // Vertical center short top
	parts[15] = [4]float64{size / 2, size, size / 2, size / 2} // Vertical center short bottom

	dc.SetLineWidth(thickness)
	dc.SetLineCap(gg.LineCapRound)

	// Draw the parts of the numeral
	for i := 0; i < 16; i++ {
		if (num>>i)&1 == 1 {
			dc.DrawLine(parts[i][0], parts[i][1], parts[i][2], parts[i][3])
			dc.Stroke()
		}
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
