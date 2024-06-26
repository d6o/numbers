package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
)

type Renderer interface {
	Render() string
}

func main() {
	flag.Usage = func() {
		fmt.Println(`
NAME:
  cistercian - convert base 10 number to equivalent cistercian numeral glyph

USAGE:
  cistercian [options] value

VERSION:
  1.1.0

OPTIONS
    `)

		flag.PrintDefaults()
	}

	flag.Bool("text", true, "Output glyph as text to stdout")
	shouldOutputSVG := flag.Bool("svg", false, "Output glyph as SVG to stdout")
	strokeWidth := flag.Int("stroke-width", 10, "Stroke width (SVG)")
	strokeColor := flag.String("stroke-color", "#000", "Stroke color (SVG)")

	flag.Parse()

	if len(os.Args) == 1 {
		flag.Usage()
		os.Exit(1)
	}

	value, err := strconv.Atoi(flag.Arg(0))
	if err != nil {
		fmt.Println("Failed to parse input as an integer:", os.Args[1])
		os.Exit(1)
	}

	var renderer Renderer

	if *shouldOutputSVG {
		renderer = PNGRenderer{Value: value,
			Stroke: *strokeWidth,
			Color:  *strokeColor,
		}
	} else {
		renderer = TextRenderer{Value: value}
	}

	fmt.Print(renderer.Render())
}
