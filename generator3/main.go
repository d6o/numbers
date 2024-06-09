package main

import (
	"fmt"
	"image"
	"image/color"
	"image/png"
	"os"
	"path/filepath"
)

// Define the size of each matrix and the final image
const matrixSize = 16
const finalSize = matrixSize * 2

var numeralMap = map[rune][matrixSize][matrixSize]int{
	'0': zero,
	'1': one,
	'2': two,
	'3': three,
	'4': four,
	'5': five,
	'6': six,
	'7': seven,
	'8': eight,
	'9': nine,
}

func parseInteger(n int) ([matrixSize][matrixSize]int, [matrixSize][matrixSize]int, [matrixSize][matrixSize]int, [matrixSize][matrixSize]int) {
	str := fmt.Sprintf("%04d", n) // Ensure the number is at least 4 digits
	runes := []rune(str)

	return numeralMap[runes[0]], numeralMap[runes[1]], numeralMap[runes[2]], numeralMap[runes[3]]
}

func saveImageForNumber(num int, dir string) error {
	thousands, hundreds, tens, units := parseInteger(num)

	// Create a new grayscale image
	img := image.NewGray(image.Rect(0, 0, finalSize, finalSize))

	// Helper function to set the pixels from a matrix into the image
	setPixels := func(matrix [matrixSize][matrixSize]int, startX, startY int, mirrorH, mirrorV bool) {
		for y := 0; y < matrixSize; y++ {
			for x := 0; x < matrixSize; x++ {
				// Determine the actual pixel position after mirroring
				actualX := x
				actualY := y
				if mirrorH {
					actualX = matrixSize - 1 - x
				}
				if mirrorV {
					actualY = matrixSize - 1 - y
				}
				if matrix[actualY][actualX] == 1 {
					img.SetGray(startX+x, startY+y, color.Gray{Y: 0}) // Black pixel
				} else {
					img.SetGray(startX+x, startY+y, color.Gray{Y: 255}) // White pixel
				}
			}
		}
	}

	// Place each matrix in one corner of the image with the required mirroring
	setPixels(tens, 0, 0, true, false)
	setPixels(units, matrixSize, 0, false, false)
	setPixels(thousands, 0, matrixSize, true, true)
	setPixels(hundreds, matrixSize, matrixSize, false, true)

	// Create a file to save the image
	filePath := filepath.Join(dir, fmt.Sprintf("%04d.png", num))
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	// Encode the image to PNG format and save it to the file
	err = png.Encode(file, img)
	if err != nil {
		return err
	}

	return nil
}

func main() {
	// List of integers to process
	numbers := []int{1234, 5678, 9999, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 0001, 0004, 0102, 0505, 1992, 4723, 6859, 7085, 8971, 9938}

	// Directory to save the images
	outputDir := "/Users/diegosiqueira/Playground/numbers/tests"

	// Ensure the output directory exists
	if err := os.MkdirAll(outputDir, os.ModePerm); err != nil {
		panic(err)
	}

	// Process each number and save the corresponding image
	for _, num := range numbers {
		if err := saveImageForNumber(num, outputDir); err != nil {
			fmt.Printf("Failed to save image for number %d: %v\n", num, err)
		} else {
			fmt.Printf("Image for number %d saved successfully.\n", num)
		}
	}
}
